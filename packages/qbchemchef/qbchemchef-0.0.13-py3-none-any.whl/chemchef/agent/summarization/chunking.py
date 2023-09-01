from typing import Iterable


def to_chunks(text: str, chunk_size: int, overlap_size: int, max_chunks: int) -> Iterable[str]:
    total_num_chars = len(text)

    current_chunk_id = 0
    current_chunk_start = 0
    current_chunk_end = chunk_size

    while current_chunk_id < max_chunks:
        yield text[current_chunk_start: current_chunk_end]

        if current_chunk_end >= total_num_chars:
            break

        current_chunk_start += chunk_size - overlap_size
        current_chunk_end += chunk_size - overlap_size
        current_chunk_id += 1
