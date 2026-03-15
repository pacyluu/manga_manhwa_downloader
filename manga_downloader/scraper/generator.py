from pathlib import Path
from io import BytesIO
from PIL import Image


def save_pdf(raw_images, chapter: int, output_folder: Path):
    chapter = str(chapter)
    output_folder.mkdir(parents=True, exist_ok=True)
    pdf_path = output_folder / f"chapter{chapter}.pdf"

    images = [Image.open(BytesIO(b)).convert("RGB") for b in raw_images]

    images[0].save(
        pdf_path,
        save_all=True,
        append_images=images[1:]
    )

    return pdf_path