import pytest

from chemchef.engine.indexing.keyword_similarity import parse_assistant_message, \
    SimilarityTestResponseParsingError, TargetCandidatesTuple, construct_user_message, SynonymsHyponymsHypernymsTuple, \
    construct_assistant_message


def test_parse_assistant_message() -> None:
    message = """Synonyms: sport\nHyponyms: football, rugby\nHypernyms:"""

    result = parse_assistant_message(message, {"sport", "football", "rugby"})
    assert result.synonyms == {"sport"}
    assert result.hyponyms == {"football", "rugby"}
    assert result.hypernyms == set()


def test_parse_assistant_message_with_extra_whitespace() -> None:
    message = """Synonyms: sport \n Hyponyms: football,  rugby\nHypernyms: \n"""

    result = parse_assistant_message(message, {"sport", "football", "rugby"})
    assert result.synonyms == {"sport"}
    assert result.hyponyms == {"football", "rugby"}
    assert result.hypernyms == set()


def test_parse_assistant_message_with_wrong_line_headers() -> None:
    message = """Synonyms: sport\nWRONG: football, rugby\nHypernyms:"""

    with pytest.raises(SimilarityTestResponseParsingError) as exc_info:
        parse_assistant_message(message, {"sport", "football", "rugby"})

    assert "Cannot parse" in str(exc_info.value)


def test_parse_assistant_message_with_wrong_number_of_lines() -> None:
    message = """Synonyms: sport\nHyponyms: football, rugby\nHypernyms:foo\nExtra line"""

    with pytest.raises(SimilarityTestResponseParsingError) as exc_info:
        parse_assistant_message(message, {"sport", "football", "rugby"})

    assert "Cannot parse" in str(exc_info.value)


def test_parse_assistant_message_with_synonym_not_in_original_candidates() -> None:
    message = """Synonyms: golf\nHyponyms: football, rugby\nHypernyms:foo"""

    with pytest.raises(SimilarityTestResponseParsingError) as exc_info:
        parse_assistant_message(message, {"sport", "football", "rugby"})

    assert "not among the original candidates" in str(exc_info.value)


def test_construct_user_message() -> None:
    target_candidate_tuple = TargetCandidatesTuple(target="foo", candidates=["bar", "aaa"])
    message = construct_user_message(target_candidate_tuple)
    assert message == "Target: foo\nCandidates: bar, aaa"


def test_construct_assistant_message() -> None:
    result_tuple = SynonymsHyponymsHypernymsTuple(
        synonyms={"foo"}, hyponyms=set(), hypernyms={"bar", "aaa"}
    )
    message = construct_assistant_message(result_tuple)
    assert (message == "Synonyms: foo\nHyponyms: \nHypernyms: bar, aaa"
        or message == "Synonyms: foo\nHyponyms: \nHypernyms: aaa, bar")
