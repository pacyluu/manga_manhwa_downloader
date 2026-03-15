# https://roliascan.com/
from scrapling.engines.toolbelt.custom import Response

def parse_chapter(page: Response):
    links = page.css('div.manga-child-the-content.my-5 img')
    return [link.attrib['src'] for link in links]
