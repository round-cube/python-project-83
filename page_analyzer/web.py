from requests import get
from requests.exceptions import ConnectionError


class URLFetchError(Exception):
    text = "Произошла ошибка при проверке"


def fetch_url(url):
    try:
        result = get(url)
    except ConnectionError:
        raise URLFetchError
    return result.status_code
