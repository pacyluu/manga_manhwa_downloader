import logging
from scrapling.engines.toolbelt.custom import Response
from scrapling.fetchers import StealthySession
from webscraper.scraper.fetch import fetch_url
from webscraper.scraper.fetch import fetch_imgs
from webscraper.scraper.resolver import resolve_site, resolve_search, resolve_chapter
from webscraper.scraper.generator import save_pdf
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress

console = Console()

def choose_site() -> str:
    sites = {
        1: "asurascanz",
        2: "asuracomic",
        3: "roliascan",
    }

    table = Table(title="Choose a Site")
    table.add_column("#", justify="right")
    table.add_column("Site", style="cyan")

    for key, value in sites.items():
        table.add_row(str(key), value)

    console.print()
    console.print(table)

    while True:
        choice = IntPrompt.ask("Enter site number")
        if choice in sites:
            console.print(f"[green]Selected site:[/green] {sites[choice]}\n")
            return sites[choice]
        console.print("[red]Please enter 1, 2, or 3.[/red]")


def get_user_text() -> str:
    console.print("\n[bold blue]Search Series[/bold blue]")

    while True:
        text = Prompt.ask("Enter your search text").strip()
        if text:
            console.print(f"[green]Searching for:[/green] {text}\n")
            return text
        console.print("[red]Search text cannot be empty.[/red]")



def choose_result(results):
    if not results:
        console.print("[red]No results found.[/red]")
        return None

    table = Table(title="Search Results")
    table.add_column("#", justify="right")
    table.add_column("Title", style="cyan")

    for i, (title, _) in enumerate(results, start=1):
        table.add_row(str(i), title)

    console.print(table)

    while True:
        choice = IntPrompt.ask("Enter the number of the result you want")
        if 1 <= choice <= len(results):
            title, url = results[choice - 1]
            console.print(f"[green]Selected series:[/green] {title}\n")
            return url
        console.print(f"[red]Please enter a number between 1 and {len(results)}.[/red]")


def choose_range(limit):
    if limit is None:
        raise ValueError("choose_range received None for limit")

    limit = int(limit)

    console.print("\n[bold blue]Choose Chapter Range[/bold blue]")
    console.print(f"[cyan]Available chapters:[/cyan] 1 to {limit}")

    while True:
        start = IntPrompt.ask("Enter starting chapter")
        end = IntPrompt.ask("Enter ending chapter")

        if not (1 <= start <= limit and 1 <= end <= limit):
            console.print(f"[red]Both chapter numbers must be between 1 and {limit}.[/red]")
            continue

        if start > end:
            console.print("[red]Starting chapter must be less than or equal to ending chapter.[/red]")
            continue

        console.print(f"[green]Selected chapters:[/green] {start} to {end}\n")
        return start, end


def main():
    logging.getLogger("scrapling").disabled = True

    site = choose_site()
    query = get_user_text()



    search_parser_fn, limit_parser_fn, chapter_parser_fn, format = resolve_site(site)  
    search_page = resolve_search(site, query)

    with StealthySession(
       headless=True,
        real_chrome=True,
        block_webrtc=True,
        solve_cloudflare=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
    ) as session:

        search_results =  search_parser_fn(fetch_url(session, search_page))                             #List of search results
        selected_url = choose_result(search_results)                                               #Choose one of the results
        limit = limit_parser_fn(fetch_url(session, selected_url))                                           #Fetch the page of the selected title
        
        start, end = choose_range(limit)

        with Progress() as progress:
            task = progress.add_task("Downloading chapters...", total=end - start + 1)

            for i in range(start, end + 1):
                chapter_page = resolve_chapter(site, i, selected_url)
                images = chapter_parser_fn(fetch_url(session, chapter_page))
                raw_images = fetch_imgs(session, images)
                save_pdf(raw_images, i, format)

                progress.update(task, advance=1)
    
if __name__ == "__main__":
    main()
