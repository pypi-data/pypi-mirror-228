from chemchef.agent.search_critique.search_critique import critique_search_results
from chemchef.clients.internet.google import SearchResult


def test_critique_search_results() -> None:
    search_query = "cheaper alternatives to Alpro soy milk"
    search_results: list[SearchResult] = [
        SearchResult(
            url="https://www.gourmetkava.cz/en/milk-alternatives-alpro-145pk",
            title="Alpro Barista milk alternatives",
            description="The Alpro Barista for professionals range of dairy alternatives offers high and stable quality in the preparation of espresso milk drinks..."
        ),
        SearchResult(
            url="https://www.reddit.com/r/veganuk/comments/u2jse2/anyone_else_hate_soy_milk_cheap_alternatives/",
            title="Anyone else hate soy milk? Cheap alternatives?",
            description="Being the tight fuck I am I always opt for the cheapest plant milk available, which is unsweetened soy milk..."
        )
    ]
    response = critique_search_results(search_query, search_results)
    print(response)
