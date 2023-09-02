"""
Tool for grabbing screenshot
"""


def grab_screen(
    xstart: int = 0, ystart: int = 0, xend: int = 1920, yend: int = 1080
) -> str:
    from PIL import ImageGrab
    from tempfile import mkstemp

    _, temp_filename = mkstemp(suffix=".png")
    img = ImageGrab.grab(bbox=(xstart, ystart, xend, yend))
    img.save(temp_filename)
    return temp_filename
