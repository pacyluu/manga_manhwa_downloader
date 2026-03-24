import logging
from pathlib import Path
from scrapling.fetchers import StealthySession
from manga_downloader.config import OUTPUT_DIR
from manga_downloader.scraper.fetch import fetch_url, fetch_imgs
from manga_downloader.scraper.resolver import resolve_site
from manga_downloader.scraper.generator import save_pdf
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress

console = Console()

def sanitize_folder_name(name: str) -> str:
    invalid_chars = '<>:"/\\|?*'
    cleaned = "".join("_" if ch in invalid_chars else ch for ch in name).strip()
    return cleaned or "download"

def choose_site() -> str:
    sites = {
        1: "asurascanz",
        2: "asurascans",
        3: "roliascan",
        4: "kunmanga"
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
            return text.strip()
        console.print("[red]Search text cannot be empty.[/red]")


def choose_result(results):
    if not results:
        console.print("[red]No results found.[/red]")
        return None, None

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
            return title, url
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

def choose_output_folder(output_dir: Path, default_name: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    folders = sorted([p for p in output_dir.iterdir() if p.is_dir()], key=lambda p: p.name.lower())
    default_folder_name = sanitize_folder_name(default_name)

    table = Table(title="Choose Output Folder")
    table.add_column("#", justify="right")
    table.add_column("Option", style="cyan")

    option_map = {}
    option_num = 1

    table.add_row(str(option_num), f"Use default folder: {default_folder_name}")
    option_map[option_num] = ("default", default_folder_name)
    option_num += 1

    for folder in folders:
        table.add_row(str(option_num), f"Use existing folder: {folder.name}")
        option_map[option_num] = ("existing", folder)
        option_num += 1

    table.add_row(str(option_num), "Create a new folder")
    option_map[option_num] = ("new", None)

    console.print(table)

    while True:
        choice = IntPrompt.ask("Enter folder option")
        if choice not in option_map:
            console.print("[red]Invalid selection.[/red]")
            continue

        option_type, value = option_map[choice]

        if option_type == "default":
            selected_folder = output_dir / value
            selected_folder.mkdir(parents=True, exist_ok=True)
            console.print(f"[green]Using folder:[/green] {selected_folder.name}\n")
            return selected_folder

        if option_type == "existing":
            console.print(f"[green]Using folder:[/green] {value.name}\n")
            return value

        folder_name = Prompt.ask("Enter new folder name").strip()
        folder_name = sanitize_folder_name(folder_name)
        selected_folder = output_dir / folder_name
        selected_folder.mkdir(parents=True, exist_ok=True)
        console.print(f"[green]Created and using folder:[/green] {selected_folder.name}\n")
        return selected_folder

def main():
    logging.getLogger("scrapling").disabled = True

    site = choose_site()
    query = get_user_text()

    search_parser_fn, limit_parser_fn, chapter_parser_fn, search_url_fn, chapter_url_fn, head = resolve_site(site)
    search_page = search_url_fn(query)

    with StealthySession(
        headless=head,
        real_chrome=True,
        block_webrtc=True,
        solve_cloudflare=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
    ) as session:
        
        search_results = search_parser_fn(fetch_url(session, search_page))
        selected_title, selected_url = choose_result(search_results)

        output_folder = choose_output_folder(OUTPUT_DIR, selected_title)

        limit = limit_parser_fn(fetch_url(session, selected_url))
        start, end = choose_range(limit)

        with Progress() as progress:
            task = progress.add_task("Downloading chapters...", total=end - start + 1)

            for i in range(start, end + 1):
                chapter_page = chapter_url_fn(i, selected_url)
                images = chapter_parser_fn(fetch_url(session, chapter_page))
                print(images)
                raw_images = fetch_imgs(session, images)
                save_pdf(raw_images, i, output_folder)

                progress.update(task, advance=1)

if __name__ == "__main__":
    main()
