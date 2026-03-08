# https://asuracomic.net/
from scrapling.engines.toolbelt.custom import Response
# from webscraper.models.document import Document

#https://asuracomic.net/series?page=1&name=youngest&_rsc=fd029
#get

def search_site(query):
    url =  "https://asuracomic.net/series?page=1&name={query}" 

def parse_chapter(page: Response):
    links = page.css('div.w-full.mx-auto.center img')
    return [link.attrib['src'] for link in links]
