# https://asurascanz.com/
from scrapling.engines.toolbelt.custom import Response
# from webscraper.models.document import Document

def parse(page: Response):
    links = page.css('p img[src*=image]')
    return [link.attrib['src'] for link in links]
