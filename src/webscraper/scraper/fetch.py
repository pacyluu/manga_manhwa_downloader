from scrapling.engines.toolbelt.custom import Response
from scrapling.fetchers import StealthyFetcher

#return the response.text
def fetch_url(session, url: str) -> Response:
    page = session.fetch(url)
    if page.status == 200:
        return page

    raise ValueError(f"Failed to fetch {url}: {page.status}")

def fetch_imgs(session, images) :
    image_list = []
    for img_url in images:
        page = session.fetch(img_url)
        image_list.append(page.body)
    return image_list
    