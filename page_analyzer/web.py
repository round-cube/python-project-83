from bs4 import BeautifulSoup


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
