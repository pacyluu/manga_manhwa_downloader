# https://asurascanz.com/
import re
from scrapling.engines.toolbelt.custom import Response

def parse_search_page(page: Response):
    links = page.css("div.bsx a")
    urls = [link.attrib['href'] for link in links]

    links = page.css("div.tt")
    titles = [link.text for link in links]

    return list(zip(titles, urls))

def parse_limit(page: Response):
    links = page.css("span.epcur.epcurlast")
    result = links[0].text
    print(result)
    match = re.search("\d+", str(result))
    return int(match.group())

def parse_chapter(page: Response):
    links = page.css('p img[src*=image]')
    return [link.attrib['src'] for link in links]
