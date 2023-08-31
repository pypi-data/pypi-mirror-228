import pytest

from chemchef.clients.internet.download import load_page, PageLoadingError


def test_load_page() -> None:
    text = load_page('https://www.bbc.co.uk')
    assert len(text) > 1000
    assert '<p>' not in text  # i.e. the HTML has been parsed


def test_load_page_when_page_doesnt_exist() -> None:
    with pytest.raises(PageLoadingError):
        load_page('https://www.gibberish1234QWERTY.com')

