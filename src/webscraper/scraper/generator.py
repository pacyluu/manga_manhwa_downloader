from PIL import Image
from io import BytesIO

from webscraper.config import OUTPUT_DIR

def save_pdf(raw_images, chapter: int, format: str):
    chapter = str(chapter)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = OUTPUT_DIR / f"chapter{chapter}.pdf"

    for idx, b in enumerate(raw_images):
        print(idx, type(b), len(b) if isinstance(b, (bytes, bytearray)) else "not-bytes")
        if isinstance(b, (bytes, bytearray)):
            print(b[:30])

    print(raw_images[1][:500].decode("utf-8", errors="ignore"))

    images = [Image.open(BytesIO(b)).convert("RGB") for b in raw_images]

    images[0].save(
        pdf_path,
        save_all=True,
        append_images=images[1:]
    )

    return pdf_path
