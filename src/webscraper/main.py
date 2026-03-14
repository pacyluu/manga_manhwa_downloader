from scrapling.engines.toolbelt.custom import Response
from webscraper.scraper.fetch import fetch_url
from webscraper.scraper.fetch import fetch_imgs
from webscraper.scraper.resolver import resolve_site, resolve_search, resolve_chapter
from webscraper.scraper.generator import save_pdf

def choose_site() -> str:
    sites = {
        "1": "asurascanz",
        "2": "asuracomic",
        "3": "roliascan",
    }

    print("Choose a site:")
    for key, value in sites.items():
        print(f"{key}. {value}")

    while True:
        choice = input("Enter number: ").strip()
        if choice in sites:
            return sites[choice]
        print("Invalid choice. Please enter 1, 2, or 3.")


def get_user_text() -> str:
    while True:
        text = input("Enter your search text: ").strip()
        if text:
            return text
        print("Input cannot be empty.")

def choose_result(results):
    if not results:
        print("No results found.")
        return None

    for i, (title, _) in enumerate(results, start=1):
        print(f"{i}. {title}")

    while True:
        choice = input("Enter the number of the result you want: ").strip()

        if not choice.isdigit():
            print("Please enter a valid number.")
            continue

        choice = int(choice)

        if 1 <= choice <= len(results):
            return results[choice - 1][1]

        print(f"Please enter a number between 1 and {len(results)}.")

def choose_range(limit):
    while True:
        start = input(f"Enter the starting chapter (1-{limit}): ").strip()
        end = input(f"Enter the ending chapter ({start if start.isdigit() else '1'}-{limit}): ").strip()

        if not start.isdigit() or not end.isdigit():
            print("Please enter valid integers.")
            continue

        start = int(start)
        end = int(end)

        if not (1 <= start <= limit and 1 <= end <= limit):
            print(f"Both chapter numbers must be between 1 and {limit}.")
            continue

        if start > end:
            print("The starting chapter must be less than or equal to the ending chapter.")
            continue

        return (start, end)

def main():

    site = choose_site()
    query = get_user_text()

    search_parser_fn, range_parser_fn, chapter_parser_fn, format, captchas = resolve_site(site)  
    search_page = resolve_search(site, query)
    search_results =  search_parser_fn(fetch_url(search_page))                             #List of search results
    selected = choose_result(search_results)                                               #Choose one of the results
    range = range_parser_fn(fetch_url(selected))                                           #Fetch the page of the selected title
    
    start, end = choose_range(range)

    for i in range(start, end+1):
        chapter_page = resolve_chapter(site, i, selected)
        images = chapter_parser_fn(chapter_page)
        raw_images = fetch_imgs(images, captchas)
        save_pdf(raw_images, i, format)
    
    
if __name__ == "__main__":
    main()
