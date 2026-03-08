from webscraper.sites import asuracomic, asurascanz, roliascan    

def resolve_site(url: str):
    if "asurascanz" in url:
        return (asurascanz.parse_chapter,"webp", False)
    elif "asuracomic" in url:
        return (asuracomic.parse_chapter,"webp", False)
    elif "roliascan" in url:
        return (roliascan.parse_chapter, "webp", True)
    else:
        raise ValueError("Unsupported site")