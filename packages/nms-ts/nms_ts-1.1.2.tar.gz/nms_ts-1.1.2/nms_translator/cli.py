import click
from pathlib import Path
from nms_translator import __version__

LORE_PATH = Path().home() / "nms_lore.txt"


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--xstart",
    type=click.INT,
    help="Horizontal start of bounding box, defaults to top-left of screen",
    default=0,
)
@click.option(
    "--ystart",
    type=click.INT,
    help="Vertical start of bounding box, defaults to top-left of screen",
    default=0,
)
@click.option(
    "--xend",
    type=click.INT,
    help="Horizontal end of bounding box, defaults to bottom right of a 1920x1080 display",
    default=1920,
)
@click.option(
    "--yend",
    type=click.INT,
    help="Vertical end of bounding box, defaults to bottom right of a 1920x1080 display",
    default=1080,
)
def ts(xstart: int, ystart: int, xend: int, yend: int):
    from nms_translator.grabber import grab_screen
    from nms_translator.textract import extract_from_file
    from nms_translator.translator import translate

    screen = grab_screen(xstart=xstart, xend=xend, ystart=ystart, yend=yend)
    encoded_str = extract_from_file(screen)
    final = translate(encoded_str)
    with open(LORE_PATH, "a+") as f:
        f.write(f"{final}\n")


cli.add_command(ts)

if __name__ == "__main__":
    cli()
