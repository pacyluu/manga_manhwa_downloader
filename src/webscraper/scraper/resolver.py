from webscraper.sites import site1, site2, site3

def get_parser_and_format_for_url(url: str):
    if "asurascanz" in url:
        return (site1.parse, "webp")
    # elif "site2.com" in url:
    #     return site2.parse
    # elif "site3.com" in url:
    #     return site3.parse
    else:
        raise ValueError("Unsupported site")