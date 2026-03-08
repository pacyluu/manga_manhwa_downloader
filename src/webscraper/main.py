from scrapling.engines.toolbelt.custom import Response
from webscraper.scraper.fetch import fetch_chapter
from webscraper.scraper.fetch import fetch_and_write_img
from webscraper.scraper.resolver import resolve_site
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
        choice = input("Enter 1, 2, or 3: ").strip()
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
    print("\nSearch results:")
    for i, result in enumerate(results, start=1):
        print(f"{i}. {result['title']}")

    while True:
        choice = input(f"Select a result (1-{len(results)}): ").strip()

        if not choice.isdigit():
            print("Please enter a number.")
            continue

        index = int(choice)
        if 1 <= index <= len(results):
            return results[index - 1]

        print("Invalid selection.")

def main():

    site = choose_site()
    query = get_user_text()

    filename = "eatbeforeyougochapter1.pdf"
    search_fn, chapter_parser_fn, format, captchas = resolve_site(site)

    results =  search_fn(query)

    if not results:
        print("No results found.")
        return

    selected = choose_result(results)

    # page = fetch(url)
    images = chapter_parser_fn(page)
    raw_images = fetch_and_write_img(images, captchas)
    save_pdf(raw_images, filename, format)
    
if __name__ == "__main__":
    main()

# results = [
#     {"title": "Percy Jackson and the Olympians", "url": "https://..."},
#     {"title": "Percy Jackson: Sea of Monsters", "url": "https://..."},
#     {"title": "Percy Jackson: The Titan's Curse", "url": "https://..."},
# ]