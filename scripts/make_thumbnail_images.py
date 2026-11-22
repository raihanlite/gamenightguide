#!/usr/bin/env python3
"""Game Night Guide: thumbnail-style hero and OG images.

Builds NEW images from the games' original real photos, in the style of
the owner's example thumbnails: a real photo with a dark band across the
bottom and the guide title in gold serif text.

Inputs: the real photos already in src/images/photos/ (Pexels photos and
the two Wikimedia Commons gameplay photos). No AI images, no box art,
no owner-uploaded files.

Outputs (all JPG, quality 80 unless noted):
  src/images/photos/<slug>.jpg        1200x675, 16:9 hero, photo + dark band + gold title
  src/images/photos/<slug>-thumb.jpg  800x450, 16:9 card thumb, plain photo crop, no band
  src/images/og-<slug>.jpg            1200x630, photo + dark band + gold title

The versus hero is a split image: the Catan play photo on the left and
the Ticket to Ride play photo on the right, with a thin gold divider.

Fonts: Noto Serif Display Bold for the title, DejaVu Sans Bold for the
small eyebrow. Both are installed system fonts.
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS = os.path.join(BASE, "src", "images", "photos")
OUT = os.path.join(BASE, "src", "images")
# Pristine plain photos, kept outside src/ so the site never publishes them
# and so this script can be re-run without baking a title band twice.
SOURCE = os.path.join(BASE, "source-photos")

INK = (27, 24, 21)          # dark band, matches the site ink
GOLD = (232, 163, 23)       # gold title text
CREAM = (251, 249, 244)

SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# slug: (source photo file in PHOTOS, title for the band, focus x, focus y)
GUIDES = {
    "beginners": ("beginners.jpg", "Best Board Games for Beginners", 0.5, 0.5),
    "couples": ("couples.jpg", "Best Board Games for Couples", 0.5, 0.35),
    "2-players-under-40": ("2-players-under-40.jpg",
                            "Best Board Games for 2 Players Under $40", 0.5, 0.5),
    "under-30": ("under-30.jpg", "Best Board Games Under $30", 0.5, 0.5),
    "solo-beginners": ("solo-beginners.jpg",
                       "Best Solo Board Games for Beginners", 0.5, 0.5),
}


def cover_crop(im, tw, th, fx=0.5, fy=0.5):
    """Scale the image to cover tw x th, then crop with a focus point."""
    w, h = im.size
    scale = max(tw / w, th / h)
    im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    w, h = im.size
    x = round((w - tw) * fx)
    y = round((h - th) * fy)
    return im.crop((x, y, x + tw, y + th))


def wrap_title(draw, text, font_path, start, max_w, max_lines=2):
    """Return (lines, font): wrap to at most max_lines, shrinking until it fits."""
    words = text.split()
    for size in range(start, 27, -2):
        f = ImageFont.truetype(font_path, size)
        lines, cur = [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=f) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
        if len(lines) <= max_lines:
            return lines, f
    return [text], ImageFont.truetype(font_path, 28)


def measure_band(draw, title, max_w, margin=60):
    """Wrap the title first, then size the band to fit every line.

    One line at 58px needs a 140px band, two lines need 204px.
    The band height is never guessed, so no line is ever cut off.
    """
    lines, font = wrap_title(draw, title, SERIF_BOLD, 58, max_w)
    band_h = 52 + len(lines) * (font.size + 6) + 24
    return lines, font, band_h


def add_band(canvas, title, lines, font, band_h, margin=60):
    """Dark band across the bottom with a gold serif title.

    A soft gradient above the band lets the photo fade into it,
    like the owner's example.
    """
    w, h = canvas.size
    band_top = h - band_h
    # gradient: transparent at band_top - 90, solid ink at band_top
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    fade = 90
    for y in range(band_top - fade, band_top):
        a = int(255 * (y - (band_top - fade)) / fade)
        od.line([(0, y), (w, y)], fill=INK + (a,))
    canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(canvas)
    # solid band
    draw.rectangle([(0, band_top), (w, h)], fill=INK)
    # thin gold rule at the top of the band
    draw.rectangle([(margin, band_top), (margin + 64, band_top + 4)], fill=GOLD)
    # eyebrow
    eyebrow = ImageFont.truetype(SANS_BOLD, 20)
    draw.text((margin, band_top + 18), "G A M E   N I G H T   G U I D E",
              font=eyebrow, fill=GOLD)
    # title, one or two lines, gold serif
    y = band_top + 52
    for line in lines:
        draw.text((margin, y), line, font=font, fill=GOLD)
        y += font.size + 6
    return canvas


def make_photo_title(slug, src_file, title, fx, fy):
    src = Image.open(os.path.join(SOURCE, src_file)).convert("RGB")
    # hero, 1200x675, 16:9
    hero = cover_crop(src, 1200, 675, fx, fy)
    lines, font, band_h = measure_band(ImageDraw.Draw(hero), title, 1200 - 120)
    add_band(hero, title, lines, font, band_h)
    p = os.path.join(PHOTOS, f"{slug}.jpg")
    hero.save(p, quality=80, optimize=True)
    # card thumb, 800x450, plain photo crop, no band
    thumb = cover_crop(src, 800, 450, fx, fy)
    t = os.path.join(PHOTOS, f"{slug}-thumb.jpg")
    thumb.save(t, quality=78, optimize=True)
    # OG, 1200x630
    og = cover_crop(src, 1200, 630, fx, fy)
    lines, font, band_h = measure_band(ImageDraw.Draw(og), title, 1200 - 120)
    add_band(og, title, lines, font, band_h)
    o = os.path.join(OUT, f"og-{slug}.jpg")
    og.save(o, quality=82, optimize=True)
    print(f"{slug}: hero {os.path.getsize(p)//1024}KB, "
          f"thumb {os.path.getsize(t)//1024}KB, og {os.path.getsize(o)//1024}KB")


def make_versus():
    """Split image: Catan play photo left, Ticket to Ride play photo right."""
    catan = Image.open(os.path.join(PHOTOS, "catan-play.jpg")).convert("RGB")
    ttr = Image.open(os.path.join(PHOTOS, "ticket-to-ride-play.jpg")).convert("RGB")
    title = "Catan vs Ticket to Ride"

    def split(w, h):
        lines, font, band_h = measure_band(
            ImageDraw.Draw(Image.new("RGB", (w, h))), title, w - 120)
        photo_h = h - band_h
        left = cover_crop(catan, w // 2, photo_h, 0.5, 0.5)
        right = cover_crop(ttr, w // 2, photo_h, 0.5, 0.5)
        canvas = Image.new("RGB", (w, h), INK)
        canvas.paste(left, (0, 0))
        canvas.paste(right, (w // 2, 0))
        d = ImageDraw.Draw(canvas)
        d.rectangle([(w // 2 - 2, 0), (w // 2 + 2, photo_h)], fill=GOLD)
        add_band(canvas, title, lines, font, band_h)
        return canvas

    hero = split(1200, 675)
    p = os.path.join(PHOTOS, "ticket-vs-catan.jpg")
    hero.save(p, quality=80, optimize=True)
    # thumb: split photo only, no band
    left = cover_crop(catan, 400, 450, 0.5, 0.5)
    right = cover_crop(ttr, 400, 450, 0.5, 0.5)
    thumb = Image.new("RGB", (800, 450), INK)
    thumb.paste(left, (0, 0))
    thumb.paste(right, (400, 0))
    d = ImageDraw.Draw(thumb)
    d.rectangle([(398, 0), (402, 450)], fill=GOLD)
    t = os.path.join(PHOTOS, "ticket-vs-catan-thumb.jpg")
    thumb.save(t, quality=78, optimize=True)
    og = split(1200, 630)
    o = os.path.join(OUT, "og-ticket-vs-catan.jpg")
    og.save(o, quality=82, optimize=True)
    print(f"ticket-vs-catan: hero {os.path.getsize(p)//1024}KB, "
          f"thumb {os.path.getsize(t)//1024}KB, og {os.path.getsize(o)//1024}KB")


def main():
    for slug, (src_file, title, fx, fy) in GUIDES.items():
        make_photo_title(slug, src_file, title, fx, fy)
    make_versus()


if __name__ == "__main__":
    main()
