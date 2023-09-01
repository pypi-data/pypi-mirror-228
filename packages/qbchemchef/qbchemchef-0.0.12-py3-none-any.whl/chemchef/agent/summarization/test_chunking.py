from chemchef.agent.summarization.chunking import to_chunks


def test_to_chunks_when_max_chunks_limit_not_reached() -> None:
    text = 'abcdefghi'
    chunks = list(to_chunks(text, chunk_size=4, overlap_size=1, max_chunks=20))
    assert chunks == ['abcd', 'defg', 'ghi']


def test_to_chunks_when_max_chunks_limit_is_reached() -> None:
    text = 'abcdefghijkl'
    chunks = list(to_chunks(text, chunk_size=3, overlap_size=1, max_chunks=3))
    assert chunks == ['abc', 'cde', 'efg']
