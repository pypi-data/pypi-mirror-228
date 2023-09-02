"""
Functions to extract text from an image.
"""

from PIL import Image
from pytesseract import pytesseract


def extract_from_file(path: str) -> str:
    img = Image.open(path)
    text = "".join(
        [char for char in pytesseract.image_to_string(img) if char in ["1", "0", " "]]
    )
    return text
