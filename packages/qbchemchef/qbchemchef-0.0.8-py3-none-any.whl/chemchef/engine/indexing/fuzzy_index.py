import logging

from chemchef.clients.chroma import AbstractVectorCollection
from chemchef.clients.chroma.chroma_client import AbstractVectorCollectionFactory
from chemchef.clients.openai import AbstractEmbedder
from chemchef.engine.extraction import ParsedDocument
from chemchef.engine.indexing.keyword_similarity import AbstractKeywordSimilarityTest

MAX_CANDIDATES_LIMIT = 50


class FuzzyIndex:
    """
    An index of keyword-to-document pointers.
    The index is implemented so that it is possible to do a fuzzy search.
    (e.g. if the search query is "apartment", the search may return document with "flat" as a keyword.)

    Data structure:
    - A vector DB collection, storing (keyword embedding vectors -> keyword) pointers
    - A normal Python dict, storing (keyword -> document id) pointers

    Fuzzy queries:

    Terminology: The "target" keyword is the keyword in the search query. We're searching for documents containing
       keywords that mean approximately the same thing as the target keyword.

    - Step 1: Use the vector DB collection to get a shortlist of "candidate" keywords whose embedding vectors
       are similar to the embedding vector of the target keyword.
    - Step 2: Use a keyword similarity test (e.g. an LLM) to determine which of the candidate keywords in this shortlist
       are in fact close in meaning to the target keyword.
    - Step 3: Use the Python dict of (keyword -> document id) pointers to return the relevant documents
    """

    def __init__(self, embedder: AbstractEmbedder,
                 vector_collection: AbstractVectorCollection,
                 keyword_similarity_test: AbstractKeywordSimilarityTest) -> None:
        self._embedder: AbstractEmbedder = embedder
        self._keyword_similarity_test = keyword_similarity_test
        self._embeddings_to_keywords: AbstractVectorCollection = vector_collection
        self._keywords_to_document_ids: dict[str, set[int]] = dict()  # {keyword: {document_ids}}

    def add(self, document_id: int, keywords: set[str]) -> None:
        """
        :param document_id: The document ID for a document
        :param keywords: A set of keywords associated with this document
        :return:
        """
        for keyword in keywords:
            if keyword not in self._keywords_to_document_ids.keys():
                embedding_for_keyword = self._embedder.embed(keyword)
                self._embeddings_to_keywords.add(embedding_for_keyword, keyword)
                self._keywords_to_document_ids[keyword] = set()
            self._keywords_to_document_ids[keyword].add(document_id)

    def exact_query(self, allowed_keywords: set[str]) -> set[int]:
        """
        :param allowed_keywords: The allowed keywords
        :return: The set of document ids that associated with any of these allowed keywords
        """
        document_ids_to_return: set[int] = set()
        for keyword in allowed_keywords:
            if keyword in self._keywords_to_document_ids:
                document_ids_to_return.update(self._keywords_to_document_ids[keyword])
        return document_ids_to_return

    def fuzzy_query(self, target_keyword: str, max_candidates: int) -> set[int]:
        """
        :param target_keyword: The target keyword
        :param max_candidates: Maximum candidate keywords to consider, where each candidate keyword
            is a possible match for the target keyword
        :return: The set of document ids that are associated with keywords that are similar to the target keyword
        """
        if max_candidates <= 0:
            raise ValueError("Max candidates must be at least 1.")
        if max_candidates > MAX_CANDIDATES_LIMIT:
            raise ValueError(f"Max candidates cannot be greater than {MAX_CANDIDATES_LIMIT}")

        embedding_for_target_keyword = self._embedder.embed(target_keyword)
        candidate_keywords: list[str] = self._embeddings_to_keywords.query(
            embedding_for_target_keyword,
            max_results=max_candidates
        )

        candidate_keywords_matching_the_target: set[str] = self._keyword_similarity_test.find_matches(
            target_keyword, candidate_keywords)

        logging.info(
            "Fuzzy query on target keyword: %s. Candidate keywords returned by vector DB: %s. Candidate keywords deemed a good match by LLM: %s",
            target_keyword,
            candidate_keywords,
            candidate_keywords_matching_the_target
        )

        document_ids_to_return: set[int] = set()
        for candidate_keyword in candidate_keywords_matching_the_target:
            document_ids_to_return.update(self._keywords_to_document_ids[candidate_keyword])

        return document_ids_to_return


class FuzzyIndexCollection:
    """A collection of fuzzy indexes: one index per document field"""

    def __init__(self, field_names: set[str],
                 embedder: AbstractEmbedder,
                 vector_collection_factory: AbstractVectorCollectionFactory,
                 keyword_similarity_test: AbstractKeywordSimilarityTest) -> None:
        self._fields_to_fuzzy_indexes: dict[str, FuzzyIndex] = {
            field : FuzzyIndex(
                embedder,
                vector_collection_factory.create_new_collection(),
                keyword_similarity_test
            )
            for field in field_names
        }
        self._all_doc_ids: set[int] = set()

    def add(self, document_id: int, parsed_doc: ParsedDocument) -> None:
        if self._fields_to_fuzzy_indexes.keys() != parsed_doc.field_names:
            raise KeyError(
                "Field names in document do not match field names in index: "
                f"{self._fields_to_fuzzy_indexes.keys()} vs {parsed_doc.field_names}"
            )

        for field in parsed_doc.fields:
            self._fields_to_fuzzy_indexes[field.field_name].add(document_id, field.values)

        self._all_doc_ids.add(document_id)

    def exact_query(self, field_name: str, allowed_keywords: set[str]) -> set[int]:
        """
        :param field_name: name of field to run query on
        :param allowed_keywords: The allowed keywords
        :return: The set of document ids that associated with any of these allowed keywords
        """
        if field_name not in self._fields_to_fuzzy_indexes.keys():
            raise KeyError(f"Field name does not exist in index: {field_name}")

        return self._fields_to_fuzzy_indexes[field_name].exact_query(allowed_keywords)

    def fuzzy_query(self, field_name: str, target_keyword: str, max_candidates: int) -> set[int]:
        """
        :param field_name: name of field to run query on
        :param target_keyword: The target keyword
        :param max_candidates: Maximum candidate keywords to consider, where each candidate keyword
            is a possible match for the target keyword
        :return: The set of document ids that are associated with keywords that are similar to the target keyword
        """
        if field_name not in self._fields_to_fuzzy_indexes.keys():
            raise KeyError(f"Field name does not exist in index: {field_name}")

        return self._fields_to_fuzzy_indexes[field_name].fuzzy_query(target_keyword, max_candidates)

    @property
    def all_doc_ids(self) -> set[int]:
        return set(self._all_doc_ids)
