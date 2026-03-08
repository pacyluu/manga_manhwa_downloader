from scrapling.engines.toolbelt.custom import Response
from scrapling.fetchers import StealthyFetcher

#return the response.text
def fetch_chapter(url: str) -> Response:
    page = StealthyFetcher.fetch(url, solve_cloudflare=True)
    if page.status == 200:
        return page

    raise ValueError(f"Failed to fetch {url}: {page.status}")

def fetch_and_write_img(images, captchas) :
    image_list = []
    for img in images:
        if captchas:
            page = StealthyFetcher.fetch(img, solve_cloudflare=True)
        else:
            page = StealthyFetcher.fetch(img)
        image_list.append(page.body)
    
    return image_list
    