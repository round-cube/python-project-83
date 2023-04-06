from requests import get
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup


class URLFetchError(Exception):
    text = "Произошла ошибка при проверке"


def fetch_url(url):
    try:
        result = get(url)
    except ConnectionError:
        raise URLFetchError
    return result


def parse_html(content_string):
    soup = BeautifulSoup(content_string, 'html.parser')
    first_h1_string = soup.h1.string if soup.h1 else None
    title_string = soup.title.string if soup.title else None
    description_string = None
    for meta in soup.find_all("meta"):
        if meta.get("name") == "description":
            description_string = meta.get("content")
            break
    return first_h1_string, title_string, description_string
