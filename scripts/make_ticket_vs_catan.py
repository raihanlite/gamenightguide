#!/usr/bin/env python3
"""Ticket to Ride vs Catan hero, thumb and OG, from the owner-supplied image.

Source: ~/workspace/user/media_library/image/image-6d91c34a.png
  (split image: Catan board left, Ticket to Ride Europe board right,
   title "Catan vs Ticket to Ride" at the bottom, 1600x893, about 16:9).

Outputs (all JPG):
  src/images/photos/ticket-vs-catan.jpg       1200x675, 16:9, resized, not cropped
  src/images/photos/ticket-vs-catan-thumb.jpg  800x450, 16:9, resized, not cropped
  src/images/og-ticket-vs-catan.jpg           1200x630, image fitted with dark
      side bars sampled from the image edge, so the title stays fully visible

The image is never centre-cropped: a crop would cut the title at the bottom
or one of the two boards. The hero is 16:9 because the article hero CSS is
aspect-ratio 16/9. The OG is 1200x630 because base.njk declares og:image
1200x630, so the image is fitted, not cropped.
"""
import os
from PIL import Image, ImageStat

SRC = os.path.expanduser(
    "~/workspace/user/media_library/image/image-6d91c34a.png")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "src", "images")
PHOTOS = os.path.join(OUT, "photos")


def main():
    im = Image.open(SRC).convert("RGB")
    print("source:", im.size)

    hero = im.resize((1200, 675), Image.LANCZOS)
    hp = os.path.join(PHOTOS, "ticket-vs-catan.jpg")
    hero.save(hp, quality=82, optimize=True)

    thumb = im.resize((800, 450), Image.LANCZOS)
    tp = os.path.join(PHOTOS, "ticket-vs-catan-thumb.jpg")
    thumb.save(tp, quality=78, optimize=True)

    # OG: fit the 16:9 image into 1200x630 without cropping the title.
    scale = 630 / im.size[1]
    fitted = im.resize((round(im.size[0] * scale), 630), Image.LANCZOS)
    # Dark bar colour: median of the image border, so the bars blend in.
    border = Image.new("RGB", (im.size[0], im.size[1]), (0, 0, 0))
    edge = ImageStat.Stat(im.crop((0, 0, im.size[0], 6))).median
    bar = tuple(int(v * 0.55) for v in edge)
    canvas = Image.new("RGB", (1200, 630), bar)
    canvas.paste(fitted, ((1200 - fitted.size[0]) // 2, 0))
    og = os.path.join(OUT, "og-ticket-vs-catan.jpg")
    canvas.save(og, quality=82, optimize=True)

    for p in (hp, tp, og):
        print(p, Image.open(p).size, os.path.getsize(p) // 1024, "KB")


if __name__ == "__main__":
    main()
