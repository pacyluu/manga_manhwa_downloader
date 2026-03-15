# https://asuracomic.net/
from scrapling.engines.toolbelt.custom import Response

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
#     "Referer": "https://asuracomic.net/",
#     "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
#     "DNT": "1",
# }

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
    
