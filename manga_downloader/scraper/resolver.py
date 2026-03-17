from manga_downloader.sites import site1, site2, site3, site4
   

def resolve_site(site: str):
    if "asurascanz" in site:
        return (site1.parse_search_page, site1.parse_limit, site1.parse_chapter,site1.get_search_url,site1.get_chapter_url, False)
    elif "asuracomic" in site:
        return (site2.parse_search_page, site2.parse_limit, site2.parse_chapter,site2.get_search_url,site2.get_chapter_url, False)
    elif "roliascan" in site:
        return (site3.parse_search_page, site3.parse_limit, site3.parse_chapter,site3.get_search_url,site3.get_chapter_url, True)
    elif "kunmanga" in site:
        return (site4.parse_search_page, site4.parse_limit, site4.parse_chapter,site4.get_search_url,site4.get_chapter_url, True)
    else:
        raise ValueError("Unsupported site")