from validators.url import url as validate_url
from validators import ValidationFailure
from page_analyzer.message_texts import URL_REQUIRED_ERROR, URL_TOO_LONG_ERROR, INCORRECT_URL_ERROR


MAX_URL_LEN = 255


def check_url(url):
    """Return error (string) if url is not correct URL string."""

    if not url:
        return URL_REQUIRED_ERROR

    if len(url) > MAX_URL_LEN:
        return URL_TOO_LONG_ERROR

    result = validate_url(url)
    if isinstance(result, ValidationFailure):
        return INCORRECT_URL_ERROR
