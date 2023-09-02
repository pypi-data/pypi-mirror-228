"""
Translate extracted binary to ASCII
"""


def translate(encoded: str) -> str:
    list_of_bins = [i for i in encoded.split(" ")]
    translated_text = "".join([chr(int(i, 2)) for i in list_of_bins if i])
    return translated_text
