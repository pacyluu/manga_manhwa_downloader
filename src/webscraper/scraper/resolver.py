from webscraper.sites import site1, site2, site3
   

def resolve_site(site: str):
    if "asurascanz" in site:
        return (site1.parse_search_page, site1.parse_range, site1.parse_chapter,"webp", False)
    elif "asuracomic" in site:
        return (site2.parse_search_page, site2.parse_range, site2.parse_chapter,"webp", False)
    elif "roliascan" in site:
        return (site3.parse_chapter, "webp", True)
    else:
        raise ValueError("Unsupported site")

def resolve_search(site: str, query: str):
    if "asurascanz" in site:
        return f"https://asurascanz.com/?s={query}"
    elif "asuracomic" in site:
        return f"https://asuracomic.net/series?page=1&name={query}"
    elif "roliascan" in site:
        return 
    else:
        raise ValueError("Unsupported site")
    
def resolve_chapter(site: str, chapter: int, url: str):
    if "asurascanz" in site:
        url = url[:-1]
        return f"{url}-chapter-{chapter}"
    elif "asuracomic" in site:
        return f"{url}/chapter/{chapter}"
    elif "roliascan" in site:
        return 
    else:
        raise ValueError("Unsupported site")