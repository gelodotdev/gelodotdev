"""Turn photo.jpg into the ASCII portrait used by build.py."""
import sys
from PIL import Image, ImageFilter, ImageOps

RAMP = " .`',:;i!|jkl*+rnmHKX8$#M@"
CROP = (860, 290, 1240, 740)    # head and shoulders
COLS, ROWS = 60, 36             # cells are ~2x taller than wide
FLOOR = 60                      # anything darker is night background
GAMMA = 2.6


def portrait(path="photo.jpg"):
    im = ImageOps.autocontrast(Image.open(path).convert("L").crop(CROP), cutoff=1)
    im = im.filter(ImageFilter.UnsharpMask(radius=30, percent=350, threshold=0))
    im = im.point(lambda v: 0 if v < FLOOR else round(255 * ((v - FLOOR) / (255 - FLOOR)) ** GAMMA))
    px = im.resize((COLS, ROWS), Image.LANCZOS).load()
    return ["".join(RAMP[px[x, y] * (len(RAMP) - 1) // 255] for x in range(COLS)).rstrip() for y in range(ROWS)]


if __name__ == "__main__":
    sys.stdout.write("\n".join(portrait()) + "\n")
