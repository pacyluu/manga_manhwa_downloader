# https://asurascanz.com/
import re
from urllib.parse import quote_plus
from scrapling.engines.toolbelt.custom import Response

def parse_search_page(page: Response):
    links = page.css("div.bsx a")
    urls = [link.attrib['href'] for link in links]

    links = page.css("div.tt")
    titles = [link.text for link in links]

    return list(zip(titles, urls))

def parse_limit(page: Response):
    result = page.css("span.epcur.epcurlast").get()
    match = re.search(r"\d+", str(result))
    return int(match.group())

def parse_chapter(page: Response):
    links = page.css('p img[src*=image]')
    return [link.attrib['src'] for link in links]

def get_search_url(query: str):
    return f"https://asurascanz.com/?s={quote_plus(query)}"

def get_chapter_url(chapter: int, url: str):
    url = url[:-1]  
    x = url.split('/')
    del x[3]
    url = "/".join(x)
    return f"{url}-chapter-{chapter}"
