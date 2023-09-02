"""
Functions to extract text from an image.
"""

from PIL import Image
from pytesseract import pytesseract


def extract_from_file(path: str) -> str:
    img = Image.open(path)
    text = pytesseract.image_to_string(img).replace("\n", " ").strip()
    return text
