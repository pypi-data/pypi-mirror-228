import requests
import html2text


class PageLoadingError(Exception):
    pass


def load_page(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
    except:
        raise PageLoadingError("Page failed to load")

    if response.status_code != 200:
        raise PageLoadingError(f"Status code is {response.status_code}")

    content_type = response.headers.get('Content-Type')
    if content_type is None or 'text/html' not in content_type:
        raise PageLoadingError(f"Content type is {content_type} rather than HTML")

    html_content = response.text

    html_handler = html2text.HTML2Text()
    try:
        text = html_handler.handle(html_content)
    except:
        raise PageLoadingError(f"Cannot parse the HTML in web page")

    return text
