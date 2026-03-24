# https://asurascans.com/
from scrapling.engines.toolbelt.custom import Response
from urllib.parse import quote
import re

def parse_search_page(page: Response):
    links = page.css("div.p-3 a")
    urls = [link.attrib['href'] for link in links]
    print(urls)
    for i in range(len(urls)):
        urls[i] = "https://asurascans.com" + urls[i]

    links = page.css("h3.text-sm.font-semibold.text-white.line-clamp-1.group-hover\\:text-\\[\\#913FE2\\].transition-colors")
    titles = [link.text for link in links]

    results = list(zip(titles, urls))
    return results[:len(results)//2]

def parse_limit(page: Response):
    result = page.css("h2.text-lg.font-bold")[0].text
    match = re.search(r"\d+", str(result))
    return int(match.group()) 

def parse_chapter(page: Response):
    links = page.css('img[src^="https://cdn.asurascans.com/asura-images/chapters/"]')
    return [link.attrib['src'] for link in links]
    
def get_search_url(query: str):
    return f"https://asurascans.com/browse?search={quote(query)}"

def get_chapter_url(chapter: int, url: str):
    return f"{url}/chapter/{chapter}"
