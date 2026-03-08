from scrapling.engines.toolbelt.custom import Response
from scrapling.fetchers import StealthyFetcher

#return the response.text
def fetch(url: str) -> Response:
    page = StealthyFetcher.fetch(url)
    if page.status == 200:
        return page

    raise ValueError(f"Failed to fetch {url}: {page.status}")

def fetch_and_write_img(images) :
    image_list = []
    for img in images:
        page = StealthyFetcher.fetch(img)
        image_list.append(page.body)
    
    return image_list
    