# https://asurascanz.com/
from scrapling.engines.toolbelt.custom import Response
# from webscraper.models.document import Document

def search_site(query):
    url = f"https://asurascanz.com/?s={query}" #get
    

def parse_chapter(page: Response):
    links = page.css('p img[src*=image]')
    return [link.attrib['src'] for link in links]
