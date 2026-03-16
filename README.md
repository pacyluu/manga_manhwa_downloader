# Manga & Manhwa Downloader

A command-line manga/manhwa downloader that lets users search titles, browse available chapters, choose what to download, and save chapters locally in pdf format.

This project is designed to make downloading manga/manhwa from supported sources more organized and convenient through an interactive CLI workflow.

> [!WARNING]
> This project is still in development. Some sources and features may be incomplete or subject to change.

## Features

- Search manga/manhwa titles from supported sources
- Browse matching results directly in the terminal
- View available chapters for a selected title
- Select individual chapters or a range of chapters to download
- Simple interactive CLI flow
- Clean local saving/downloading workflow
- Extensible structure for adding more sources later

## How It Works

The application follows a straightforward pipeline:

1. The user launches the CLI program
2. A website is selected
3. The user searches for a manga/manhwa title
5. Matching series are fetched and displayed
6. The user selects a series
7. The user selects a directory location for downloads
8. Available chapters are retrieved
9. The user chooses which chapters to download
10. The downloader fetches the chapter images
11. The content is saved locally in pdf format

## Supported Sources

- Asurascanz
- Asuracomic
- Roliascan (WIP)

## Tech Stack

- **Language:** Python
- **Interface:** CLI / terminal-based UI
- **Libraries:** [Scrapling](https://github.com/D4Vinci/Scrapling)

## Getting Started

Follow the steps below to set up the project locally.

### Prerequisites

Make sure you have the following installed:

- Python 3.10 or newer
- `pip`
- `venv`
- Google Chrome

### Installation

Clone the repository:
```  
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```
### Next Steps

Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Usage

From the project root, start the CLI with:
```
python -m manga_downloader.main
```

### Demo

![Image](https://github.com/user-attachments/assets/68903c70-e494-4476-88c2-6a6e988ab525)
