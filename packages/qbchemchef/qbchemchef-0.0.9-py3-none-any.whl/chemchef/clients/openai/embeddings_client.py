from typing import Any

import openai
import numpy as np
from abc import ABC, abstractmethod


class AbstractEmbedder(ABC):

    @abstractmethod
    def embed(self, text: str) -> np.ndarray[np.float64, Any]:
        raise NotImplementedError


class OpenAIEmbedder(AbstractEmbedder):

    def embed(self, text: str) -> np.ndarray[np.float64, Any]:
        response = openai.Embedding.create(input=text, model="text-embedding-ada-002")  # type: ignore
        return np.array(response["data"][0]["embedding"], dtype=np.float64)
