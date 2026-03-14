from PIL import Image
from io import BytesIO

from webscraper.config import OUTPUT_DIR

def save_pdf(raw_images, chapter: int, format: str):

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = OUTPUT_DIR / chapter

    if format == "webp":
        images = [Image.open(BytesIO(b)).convert("RGB") for b in raw_images]

    images[0].save(
        pdf_path,
        save_all=True,
        append_images=images[1:]
    )

    return pdf_path
