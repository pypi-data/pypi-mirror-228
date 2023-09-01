from chemchef.clients.openai.embeddings_client import OpenAIEmbedder
import numpy as np


def test_embed() -> None:
    embedder = OpenAIEmbedder()
    embedding_vec = embedder.embed("The integral of x^2 is x^3/3.")
    assert embedding_vec.shape == (1536,)
    assert type(embedding_vec[0]) == np.float64
