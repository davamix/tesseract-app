import os
import tesserocr
from pdf2image import convert_from_path, convert_from_bytes
from pathlib import Path

def convert_pdf(document_path):
    images = convert_from_path(document_path)

    if len(images) > 0:
        print(tesserocr.image_to_text(images[0]))

def run():
    # print(tesserocr.tesseract_version())
    # print(tesserocr.get_languages())
    document_path = Path(Path.cwd(), "src", "documents", "doc1.pdf")
    convert_pdf(document_path)
    
    
if __name__ == "__main__":
    run()