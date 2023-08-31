import logging
from typing import Optional, NamedTuple

from pydantic import BaseModel

from chemchef.clients.chroma.chroma_client import AbstractVectorCollectionFactory, ChromaVectorCollectionFactory
from chemchef.clients.openai import AbstractEmbedder, OpenAIEmbedder
from chemchef.engine.extraction import DocumentSchema, AbstractDocumentParser, ParsedDocument, OpenAIDocumentParser
from chemchef.engine.generation import AbstractDocumentGenerator, OpenAIDocumentGenerator
from chemchef.engine.indexing import AbstractKeywordSimilarityTest, FuzzyIndexCollection, OpenAIKeywordSimilarityTest, \
    AbstractQueryExpression, All


class Document(BaseModel):
    id: int
    text: str
    parsed_data: ParsedDocument

    def __repr__(self) -> str:
        text_words = self.text.split()  # This also removes newline characters.
        if len(text_words) < 30:
            opening_text = ' '.join(text_words)
        else:
            opening_text = ' '.join(text_words[:30]) + '...'

        return f"Document(id={self.id}, text={opening_text}, parsed_data={self.parsed_data})"

    def __str__(self) -> str:
        return repr(self)


class DocumentTable:
    """A collection of unstructured documents that can be queried."""

    def __init__(self,
                 format_description: str,
                 document_schema: DocumentSchema,
                 subject_field: str,
                 document_parser: AbstractDocumentParser = OpenAIDocumentParser(),
                 document_auto_generator: AbstractDocumentGenerator = OpenAIDocumentGenerator(),
                 embedder: AbstractEmbedder = OpenAIEmbedder(),
                 vector_collection_factory: AbstractVectorCollectionFactory = ChromaVectorCollectionFactory(),
                 keyword_similarity_test: AbstractKeywordSimilarityTest = OpenAIKeywordSimilarityTest()) -> None:
        """
        :param format_description: A brief description of what each document should contain
            e.g. "Recipe", "Ingredient factsheet"
        :param document_schema: A definition of the fields to extract from each document at ingestion time.
        :param subject_field: The field that is the name of the thing being described in each document
           e.g. format_description="Recipe" => subject_field = "Dish"
           e.g. format_description="Ingredient factsheet" => subject_field = "Ingredient"
           Note: subject_field should be one of the field names in doc_schema.
        """
        self._validate_constructor_arguments(document_schema, subject_field)

        self._format_description = format_description
        self._document_schema = document_schema

        self._all_fields = self._get_all_field_names(document_schema)
        self._subject_field = subject_field
        self._non_subject_fields = self._get_non_subject_field_names(document_schema, subject_field)

        self._document_parser = document_parser
        self._document_auto_generator = document_auto_generator

        self._indexes = FuzzyIndexCollection(self._all_fields, embedder,
                                             vector_collection_factory, keyword_similarity_test)
        self._documents: dict[int, Document] = dict()  # {document id: document}
        self._next_document_id = 0

    @staticmethod
    def _validate_constructor_arguments(doc_schema: DocumentSchema, subject_field: str) -> None:
        all_field_names = {field.field_name for field in doc_schema.fields}

        if len(all_field_names) == 0:
            raise ValueError("The document schema must contain at least one field.")

        if len(all_field_names) != len(doc_schema.fields):
            raise ValueError("The field names in the document schema must be distinct.")

        if subject_field not in all_field_names:
            raise ValueError("The subject field must be one of the field names in the document schema.")

    @staticmethod
    def _get_all_field_names(doc_schema: DocumentSchema) -> set[str]:
        return {field.field_name for field in doc_schema.fields}

    @staticmethod
    def _get_non_subject_field_names(doc_schema: DocumentSchema, subject_field: str) -> set[str]:
        return {field.field_name for field in doc_schema.fields if field.field_name != subject_field}

    def insert(self, document: str, subject: Optional[str] = None) -> Document:
        """
        Inserts the document into the collection.

        Under the hood, our implementation will extract structured information from the document using an LLM.
        This structured info will be used to index the document.

        :param document: The document to insert. Should be unstructured text.
        :param subject: The intended value of the subject field.
           (If not populated, then the LLM will infer this.)
        :return: the stored document (together with the structured info extracted from it)
        """
        parsed_doc = self._document_parser.parse(document, self._document_schema)

        if subject is not None:
            # Deterministically set the subject to be the intended one.
            parsed_doc[self._subject_field] = {subject}

        logging.info("Parsed fields: %s", parsed_doc)

        document_id = self._next_document_id
        self._next_document_id += 1

        stored_doc = Document(id=document_id, text=document, parsed_data=parsed_doc)

        self._indexes.add(document_id, parsed_doc)
        self._documents[document_id] = stored_doc

        return stored_doc

    def auto_insert(self, subject: str) -> Optional[Document]:
        """
        Automatically generates a document on a given subject using an LLM, and inserts the generated document.

        We only generate a new document if no document currently exists for this subject. If a document already exists,
        then we return the existing document.

        :param subject: the subject to generate a document on.
           This will be the value for subject field in the newly generated document.
           e.g. if format="Ingredient factsheet" and subject_field="Ingredient", then subject can be "Chickpeas"
        :return: the generated document (together with the structured information it contains)
           OR the None pointer, if the subject and expected document format are incompatible
        """
        ids_of_existing_documents_for_subject = self._indexes.exact_query(self._subject_field, {subject})

        if len(ids_of_existing_documents_for_subject) == 0:
            # No existing document => Generate new one
            generated_document = self._document_auto_generator.generate(
                subject, self._subject_field, self._non_subject_fields)

            if generated_document is not None:  # succeeded
                logging.info("Auto-generated document for subject %s: %s", subject, generated_document)
                return self.insert(generated_document, subject=subject)
            else:  # failed, since subject is deemed incompatible with the expected format
                logging.info("No auto-generated document for subject %s: subject incompatible with intended format", subject)
                return None
        else:
            # Return existing document.
            # In normal usage, there would be precisely one existing document.
            # But the code must handle the edge-case where there are multiple existing documents.
            randomly_selected_existing_doc_id = next(iter(ids_of_existing_documents_for_subject))
            return self._documents[randomly_selected_existing_doc_id]

    def query(self, query_expression: AbstractQueryExpression = All()) -> list[Document]:
        """
        Performs a search query on the document collection.

        Note that fuzzy queries will be performed by:
          - Looking for keywords in the index whose embedding vectors are similar to the embedding vector of the
            target keyword in the query.
          - Determining which of these keywords are really synonymous with the target keyword, using the help
            of an LLM.
          - Returning documents associated with the keywords deemed to be relevant.

        :param query_expression: the query expression. (Default = return all documents)
        :return: a list of documents returned by the query
        """
        relevant_document_ids = query_expression.to_query().run(self._indexes)
        sorted_relevant_document_ids = sorted(relevant_document_ids)
        return [self._documents[doc_id] for doc_id in sorted_relevant_document_ids]


class AutoGenerationRule(NamedTuple):
    join_field: str
    other_table: DocumentTable
