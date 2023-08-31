from chemchef.clients.internet.google import google_search


def test_google_search() -> None:
    counter = 0
    for result in google_search('Donald Trump', max_results=5):
        assert isinstance(result.url, str)
        assert 'https' in result.url
        assert isinstance(result.title, str)
        assert isinstance(result.description, str)
        assert 'url=' in repr(result)
        assert 'url=' in str(result)
        counter += 1
    assert counter == 5
