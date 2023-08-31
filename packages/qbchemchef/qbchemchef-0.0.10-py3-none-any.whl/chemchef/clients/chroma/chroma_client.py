from abc import ABC, abstractmethod
from typing import Any, Sequence, TypeVar, Generic
import warnings
import numpy as np
from chromadb import EphemeralClient


class AbstractVectorCollection(ABC):

    @abstractmethod
    def add(self, embedding: np.ndarray[np.float64, Any], text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def query(self, embedding: np.ndarray[np.float64, Any], max_results: int) -> list[str]:
        raise NotImplementedError


class AbstractVectorCollectionFactory():
    """A factory that creates empty, newly-initialised vector collections"""

    @abstractmethod
    def create_new_collection(self) -> AbstractVectorCollection:
        raise NotImplementedError


class ChromaVectorCollection(AbstractVectorCollection):

    def __init__(self) -> None:
        client = EphemeralClient()
        # TODO: make sure these collection names are guaranteed to be unique
        collection_name = '{:08X}'.format(np.random.randint(0, 2 ** 32))
        self._collection = client.create_collection(name=collection_name)
        self._num_documents = 0

    def add(self, embedding: np.ndarray[np.float64, Any], text: str) -> None:
        current_id = str(self._num_documents)
        embedding_as_list: Sequence[float] = list(embedding)
        self._collection.add(
            ids=[current_id],
            embeddings=[embedding_as_list],
            documents=[text]
        )
        self._num_documents += 1

    def query(self, embedding: np.ndarray[np.float64, Any], max_results: int) -> list[str]:
        embedding_as_list: Sequence[float] = list(embedding)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            results = self._collection.query(
                query_embeddings=[embedding_as_list],
                n_results=max_results
            )
        assert results["documents"] is not None
        return results["documents"][0]


class ChromaVectorCollectionFactory(AbstractVectorCollectionFactory):

    def create_new_collection(self) -> ChromaVectorCollection:
        return ChromaVectorCollection()
