#!/usr/bin/env python3
"""Game Night Guide v2: produce real-photo images from Pexels originals.

Inputs: /tmp/gng-raw/pexels-<id>.jpg (downloaded from images.pexels.com).
Outputs (all JPG, quality 80 unless noted):
  src/images/photos/hero-home.jpg   1600x900
  src/images/photos/<slug>.jpg      1200x630 centre crops
  src/images/photos/<slug>-thumb.jpg 800x450, 16:9 (home/guide cards, lazy loaded)
  src/images/og-<slug>.jpg          1200x630, photo + deep green band + title
      (same layout as the Canva OG design DAHbn8g9fqM: photo on top,
       #1E4D3B band below, cream serif title, amber eyebrow)

Photo credits: see src/photo-credits.md. All photos are Pexels free licence.
No AI images anywhere.
"""
import os
from PIL import Image, ImageDraw, ImageFont

RAW = "/tmp/gng-raw"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "images")
PHOTOS = os.path.join(OUT, "photos")

GREEN = (30, 77, 59)
CREAM = (251, 249, 244)
AMBER = (232, 163, 23)
INK = (35, 32, 28)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# slug: (pexels id, og title, og subtitle)
GUIDES = {
    "home": ("8111356", "Game Night Guide",
             "Board games for beginners, couples and families."),
    "beginners": ("8111365", "Best Board Games for Beginners",
                  "Ten games you can teach in ten minutes."),
    "couples": ("5649889", "Best Board Games for Couples",
                "Date-night games made for two."),
    "2-players-under-40": ("6218134", "Best Board Games for 2 Players Under $40",
                           "Games made for two, not games that allow two."),
    "under-30": ("3986042", "Best Board Games Under $30",
                 "Small boxes, big fun, honest prices."),
    "solo-beginners": ("6333907", "Best Solo Board Games for Beginners",
                       "Start gentle. Leave the epics for later."),
    "ticket-vs-catan": ("6114957", "Ticket to Ride vs Catan",
                        "Which first game should you buy?"),
    "finder": ("8111299", "Board Game Finder",
               "Four questions. One short list."),
}


def centre_crop(im, tw, th, fx=0.5, fy=0.5):
    w, h = im.size
    scale = max(tw / w, th / h)
    im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    w, h = im.size
    x = round((w - tw) * fx)
    y = round((h - th) * fy)
    return im.crop((x, y, x + tw, y + th))


# Crop focus per slug: the couples photo is landscape, faces upper middle
# and the board along the bottom, so aim slightly above the middle.
FOCUS = {"couples": (0.5, 0.25)}


def fit_font(draw, text, font_path, start, max_w, min_size=28):
    size = start
    while size > min_size:
        f = ImageFont.truetype(font_path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(font_path, min_size)


def wrap_title(draw, text, font_path, start, max_w):
    """Return (lines, font): one or two lines, shrinking until it fits."""
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
        if len(lines) <= 2:
            return lines, f
    return [text], ImageFont.truetype(font_path, 28)


# Focus for the OG photo band: the band is short, so aim near the top
# to keep faces in frame.
OG_FOCUS = {"couples": (0.5, 0.10)}


def make_og(slug, pid, title, subtitle):
    src = Image.open(os.path.join(RAW, f"pexels-{pid}.jpg")).convert("RGB")
    fx, fy = OG_FOCUS.get(slug, (0.5, 0.5))
    photo = centre_crop(src, 1200, 392, fx=fx, fy=fy)
    canvas = Image.new("RGB", (1200, 630), GREEN)
    canvas.paste(photo, (0, 0))
    d = ImageDraw.Draw(canvas)
    # amber eyebrow
    eyebrow = ImageFont.truetype(SANS_BOLD, 22)
    d.text((60, 412), "G A M E   N I G H T   G U I D E", font=eyebrow, fill=AMBER)
    lines, title_font = wrap_title(d, title, SERIF_BOLD, 62, 1080)
    y = 448
    for line in lines:
        d.text((60, y), line, font=title_font, fill=CREAM)
        y += title_font.size + 8
    sub_font = fit_font(d, subtitle, SANS, 26, 1080)
    d.text((60, y + 4), subtitle, font=sub_font, fill=CREAM)
    path = os.path.join(OUT, f"og-{slug}.jpg")
    canvas.save(path, quality=82, optimize=True)
    return path


def main():
    os.makedirs(PHOTOS, exist_ok=True)
    for slug, (pid, title, subtitle) in GUIDES.items():
        src = Image.open(os.path.join(RAW, f"pexels-{pid}.jpg")).convert("RGB")
        fx, fy = FOCUS.get(slug, (0.5, 0.5))
        photo = centre_crop(src, 1200, 630, fx=fx, fy=fy)
        p = os.path.join(PHOTOS, f"{slug}.jpg")
        photo.save(p, quality=80, optimize=True)
        thumb = centre_crop(src, 800, 450, fx=fx, fy=fy)
        t = os.path.join(PHOTOS, f"{slug}-thumb.jpg")
        thumb.save(t, quality=78, optimize=True)
        og = make_og(slug, pid, title, subtitle)
        print(f"{slug}: photo {os.path.getsize(p)//1024}KB, "
              f"thumb {os.path.getsize(t)//1024}KB, og {os.path.getsize(og)//1024}KB")
    hero_src = Image.open(os.path.join(RAW, "pexels-8111356.jpg")).convert("RGB")
    hero = centre_crop(hero_src, 1600, 900)
    hp = os.path.join(PHOTOS, "hero-home.jpg")
    hero.save(hp, quality=80, optimize=True)
    print(f"hero-home: {os.path.getsize(hp)//1024}KB")


if __name__ == "__main__":
    main()
