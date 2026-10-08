"""Make the site's two-colour images offline; never change the source files."""

import argparse
from pathlib import Path

from PIL import Image, ImageOps

PAPER = (238, 247, 255)
INK = (21, 94, 154)
ROOT = Path(__file__).resolve().parent.parent


def prepare(source: Path, destination: Path, size: tuple[int, int], portrait=False):
    if source.resolve() == destination.resolve():
        raise ValueError("Source and destination must be different files")
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original).convert("RGBA")
        if portrait:
            # Tight head-and-shoulders framing of the supplied 1448×1086 portrait.
            # The proportional crop also works if that source is resized.
            width, height = image.size
            image = image.crop((round(width * 0.19), 0,
                                round(width * 0.81), height))
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        else:
            image = ImageOps.contain(image, size, Image.Resampling.LANCZOS)
        # Transparent pixels represent the light palette entry, so flatten to
        # white before quantization; flattening to PAPER would speckle the void.
        background = Image.new("RGBA", size, (255, 255, 255, 255))
        offset = ((size[0] - image.width) // 2, (size[1] - image.height) // 2)
        background.alpha_composite(image, offset)
        grayscale = background.convert("L")
        monochrome = grayscale.convert("1", dither=Image.Dither.FLOYDSTEINBERG)
        result = monochrome.convert("P")
        result = result.point(lambda pixel: 0 if pixel == 0 else 1)
        result.putpalette(list(INK) + list(PAPER) + [0] * (256 * 3 - 6))
        destination.parent.mkdir(parents=True, exist_ok=True)
        result.save(destination, optimize=True, bits=1)
        colours = {colour for count, colour in result.convert("RGB").getcolors(2)}
        assert colours == {INK, PAPER}, f"Unexpected palette: {colours}"
        print(f"{destination.relative_to(ROOT)}: {size[0]}×{size[1]}, "
              f"2 colours, {destination.stat().st_size:,} bytes")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--portrait", required=True, type=Path)
    parser.add_argument("--logo", required=True, type=Path)
    args = parser.parse_args()
    prepare(args.portrait, ROOT / "assets/robert.png", (480, 560), portrait=True)
    prepare(args.logo, ROOT / "assets/ottershot.png", (192, 192))


if __name__ == "__main__":
    main()
