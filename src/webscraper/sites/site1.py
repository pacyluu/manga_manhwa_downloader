# https://asurascanz.com/
from scrapling.engines.toolbelt.custom import Response
# from webscraper.models.document import Document

def parse_search_page(page: Response):
    links = page.css("div.bsx a")
    urls = [link.attrib['href'] for link in links]

    links = page.css("div.tt")
    titles = [link.text for link in links]

    return list(zip(titles, urls))

def parse_range(page: Response):
    links = page.css("span.epcur.epcurlast")
    result = [link.text for link in links]
    return result[1]

def parse_chapter(page: Response):
    links = page.css('p img[src*=image]')
    return [link.attrib['src'] for link in links]
