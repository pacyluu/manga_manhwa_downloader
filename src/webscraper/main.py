from scrapling.engines.toolbelt.custom import Response
from webscraper.scraper.fetch import fetch
from webscraper.scraper.fetch import fetch_and_write_img
from webscraper.scraper.resolver import get_parser_and_format_for_url
from webscraper.scraper.generator import save_pdf

def main():
    url = "https://asurascanz.com/swordmasters-youngest-son-chapter-1/"
    filename = "chapter1.pdf"

    page = fetch(url)
    parser, format = get_parser_and_format_for_url(url)
    images = parser(page)
    raw_images = fetch_and_write_img(images)
    save_pdf(raw_images, filename, format)
    
if __name__ == "__main__":
    main()