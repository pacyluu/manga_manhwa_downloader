# https://asurascanz.com/
import re
from scrapling.engines.toolbelt.custom import Response

def parse_search_page(page: Response):
    links = page.css("h3.h4 a")
    urls = [link.attrib['href'] for link in links]
    titles = [link.text for link in links]

    return list(zip(titles, urls))

def parse_limit(page: Response):
    result = page.css("li.wp-manga-chapter     a").get()
    match = re.search(r"\d+", str(result))
    return int(match.group())

def parse_chapter(page: Response):
    links = page.css("div.page-break.no-gaps img")
    return [link.attrib['src'] for link in links]

def get_search_url(query: str):
    return f"https://kunmanga.com/?s={query}&post_type=wp-manga&op=&author=&artist=&release=&adult="

def get_chapter_url(chapter: int, url: str):
    return f"{url}chapter-{chapter}/"