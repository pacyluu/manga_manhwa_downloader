# https://roliascan.com/
from scrapling.engines.toolbelt.custom import Response
import re

def parse_search_page(page: Response):
    links = page.css("div.col.py-2 h4 a")
    urls = [link.attrib['href'] for link in links]
    titles = [link.text for link in links]

    return list(zip(titles, urls))

def parse_limit(page: Response):
    result = page.css("div.p-2.d-flex.flex-md-row.item b").get()
    match = re.search(r"\d+", str(result))
    return int(match.group()) 

def parse_chapter(page: Response):
    links = page.css('div.manga-child-the-content.my-5 img')
    return [link.attrib['src'] for link in links]

def get_search_url(query: str):
    return f"https://roliascan.com/?s={query}&asp_active=1&p_asid=1&p_asp_data=1&asp_gen[]=title&asp_gen[]=exact&filters_initial=1&filters_changed=0&qtranslate_lang=0&current_page_id=-1"

def get_chapter_url(chapter: int, url: str):
    return f"{url}chapter/{chapter}"