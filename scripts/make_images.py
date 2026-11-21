#!/usr/bin/env python3
"""Generate simple, clean 1200x630 OG images with PIL. No photos, no box art.
Run: python3 scripts/make_images.py  (or npm run images)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "src", "images")
os.makedirs(OUT, exist_ok=True)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# (slug, headline lines, accent colour)
IMAGES = [
    ("og-home", ["Game Night Guide", "Board games for beginners,", "couples and families."], "#1f5c46"),
    ("og-couples", ["Best Board Games", "for Couples"], "#1f5c46"),
    ("og-beginners", ["Best Board Games", "for Beginners"], "#1f5c46"),
    ("og-under-30", ["Best Board Games", "Under $30"], "#1f5c46"),
    ("og-solo-beginners", ["Best Solo Board Games", "for Beginners"], "#1f5c46"),
    ("og-ticket-vs-catan", ["Ticket to Ride", "vs Catan"], "#1f5c46"),
    ("og-2-players-under-40", ["Best Board Games for", "2 Players Under $40"], "#1f5c46"),
    ("og-finder", ["Board Game Finder", "Find your next game"], "#1f5c46"),
]


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make(slug, lines, accent):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#f6f7f8")
    d = ImageDraw.Draw(img)
    # left accent bar + dice motif (simple squares with pips, drawn by hand)
    d.rectangle([0, 0, 24, H], fill=accent)
    d.rectangle([W - 24, 0, W, H], fill=accent)
    # dice: two rounded squares
    for (x, y, s) in [(880, 180, 150), (1000, 330, 120)]:
        d.rounded_rectangle([x, y, x + s, y + s], radius=24, fill="#ffffff", outline=accent, width=4)
        cx, cy = x + s // 2, y + s // 2
        r = 11
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    f_title = ImageFont.truetype(BOLD, 64)
    f_small = ImageFont.truetype(REG, 30)
    y = 170
    for line in lines:
        for part in wrap(d, line, f_title, 780):
            d.text((80, y), part, font=f_title, fill="#1d2430")
            y += 78
    d.text((80, H - 110), "Game Night Guide  ·  gamenightguide.com", font=f_small, fill="#5b6472")
    img.save(os.path.join(OUT, slug + ".png"))
    print("wrote", slug + ".png")


for slug, lines, accent in IMAGES:
    make(slug, lines, accent)
