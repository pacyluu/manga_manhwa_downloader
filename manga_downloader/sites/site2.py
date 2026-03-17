# https://asuracomic.net/
from scrapling.engines.toolbelt.custom import Response

def parse_search_page(page: Response):
    links = page.css("div.grid.grid-cols-2.sm\\:grid-cols-2.md\\:grid-cols-5.gap-3.p-4 a")
    urls = [link.attrib['href'] for link in links]
    for i in range(len(urls)):
        urls[i] = "https://asuracomic.net/" + urls[i]

    links = page.css("span.block.text-\\[13\\.3px\\].font-bold")
    titles = [link.text for link in links]

    return list(zip(titles, urls))

def parse_limit(page: Response):
    links = page.css("span.pl-\\[1px\\]")
    result = [link.text for link in links]
    return result[1]

def parse_chapter(page: Response):
    links = page.css('div.w-full.mx-auto.center img')
    return [link.attrib['src'] for link in links]
    
def get_search_url(query: str):
    return f"https://asuracomic.net/series?page=1&name={query}"


def get_chapter_url(chapter: int, url: str):
    return f"{url}/chapter/{chapter}"