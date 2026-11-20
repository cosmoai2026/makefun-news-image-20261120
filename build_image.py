#!/usr/bin/env python3
"""Compose the 20 November 2026 world-news front page as a 1024x1024 PNG.

The page is laid out like a broadsheet: a masthead block, a wide hero
illustration, a one-line caption, then six short stories arranged in a
two-column grid above a source footer. Everything is drawn with PIL
from assets that ship in this repository (the hero illustration and the
system DejaVu fonts), so the result is fully deterministic and needs
no network access.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
HERO_FILE = ROOT / "hero.png"
ENTRY_FILE = ROOT / "entry.png"

CANVAS = 1024
EDGE = 32
INNER_W = CANVAS - 2 * EDGE
GUTTER = 28
HERO_BAND = 250

COLOURS = {
    "paper": (247, 243, 234),
    "ink": (24, 28, 38),
    "faint": (96, 100, 110),
    "accent": (176, 116, 28),
}

FONT_HOME = Path("/usr/share/fonts/truetype/dejavu")
FONT_FILES = {
    "serif_bold": FONT_HOME / "DejaVuSerif-Bold.ttf",
    "serif": FONT_HOME / "DejaVuSerif.ttf",
    "sans": FONT_HOME / "DejaVuSans.ttf",
    "sans_bold": FONT_HOME / "DejaVuSans-Bold.ttf",
}

TITLE_LINE = "20 NOVEMBER 2026"
STRAP_LINE = "Friday  ·  Shenzhen peace declaration  ·  Genocide ruling  ·  Anthropic debut"
CAPTION_TEXT = (
    "A peace declaration in Shenzhen, a genocide ruling in The Hague "
    "and a blockbuster AI debut — the world on 20 November 2026."
)
FOOTER_TEXT = "Sources: Reuters · AP · AFP · BBC — 20 Nov 2026"

# (kicker, headline, summary) for the six stories on the page.
STORIES = [
    (
        "PEACE DEAL",
        "Trump, Xi and Putin sign peace declaration",
        "The three leaders issued a four-point joint declaration "
        "after their first three-way summit in Shenzhen.",
    ),
    (
        "COURT",
        "World Court: Myanmar committed genocide",
        "The ICJ ruled 9–6 that Myanmar committed genocide against "
        "the Rohingya, a first against a state.",
    ),
    (
        "MARKETS",
        "Anthropic pops 17% in Nasdaq debut",
        "Shares closed near $97, above the $83 offer, while the "
        "Nikkei slid 4.8% and Asian markets fell.",
    ),
    (
        "RIYADH",
        "Houthi missiles hit Riyadh finance tower",
        "Missiles damaged the Saudi sovereign wealth fund's PIF "
        "tower in the capital's financial district.",
    ),
    (
        "HORMUZ",
        "Tanker ablaze after mine strike near Hormuz",
        "A tanker caught fire east of the strait as the US war "
        "with Iran entered its ninth month.",
    ),
    (
        "UKRAINE",
        "UK sends 1,000 drones to Ukraine",
        "London pledged a £260 million package as Kyiv came "
        "under ballistic missile fire.",
    ),
]


def load_font(face, size):
    return ImageFont.truetype(str(FONT_FILES[face]), size)


def wrap_text(draw, text, face, limit):
    """Split text into lines that each fit within `limit` pixels."""
    lines = []
    current = ""
    for word in text.split():
        candidate = word if not current else f"{current} {word}"
        if draw.textlength(candidate, font=face) <= limit:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, text, face, y, colour):
    """Draw one horizontally centred line; return the y below it."""
    x = (CANVAS - draw.textlength(text, font=face)) / 2
    draw.text((x, y), text, font=face, fill=colour)
    return y + face.size


def rule(draw, y, thickness=2):
    draw.rectangle([EDGE, y, CANVAS - EDGE, y + thickness], fill=COLOURS["ink"])


def draw_masthead(draw):
    rule(draw, 30, 4)
    y = centred(draw, TITLE_LINE, load_font("serif_bold", 58), 46, COLOURS["ink"])
    y = centred(draw, STRAP_LINE, load_font("sans", 19), y + 8, COLOURS["faint"])
    rule(draw, y + 14, 2)
    return y + 16


def paste_hero(page, top):
    hero = Image.open(HERO_FILE).convert("RGB")
    scale = max(INNER_W / hero.width, HERO_BAND / hero.height)
    resized = hero.resize(
        (round(hero.width * scale), round(hero.height * scale)),
        Image.LANCZOS,
    )
    left = (resized.width - INNER_W) // 2
    upper = (resized.height - HERO_BAND) // 2
    band = resized.crop((left, upper, left + INNER_W, upper + HERO_BAND))
    page.paste(band, (EDGE, top))
    return top + HERO_BAND


def draw_caption(draw, top):
    face = load_font("serif", 20)
    y = top + 12
    for line in wrap_text(draw, CAPTION_TEXT, face, INNER_W):
        y = centred(draw, line, face, y, COLOURS["faint"]) + 4
    return y


def draw_story(draw, story, x, y, width):
    """Draw one story block starting at (x, y); return the y below it."""
    kicker, headline, summary = story
    draw.text((x, y), kicker, font=load_font("sans_bold", 16), fill=COLOURS["accent"])
    y += 23
    head_face = load_font("serif_bold", 24)
    for line in wrap_text(draw, headline, head_face, width):
        draw.text((x, y), line, font=head_face, fill=COLOURS["ink"])
        y += 29
    body_face = load_font("sans", 17)
    for line in wrap_text(draw, summary, body_face, width):
        draw.text((x, y), line, font=body_face, fill=COLOURS["faint"])
        y += 22
    return y


def draw_story_grid(draw, top):
    column_w = (INNER_W - GUTTER) // 2
    y = top
    for row in range(3):
        bottoms = []
        for column in range(2):
            x = EDGE + column * (column_w + GUTTER)
            bottoms.append(draw_story(draw, STORIES[row * 2 + column], x, y, column_w))
        y = max(bottoms) + 14
    return y


def draw_footer(draw, top):
    rule(draw, top + 6, 2)
    centred(draw, FOOTER_TEXT, load_font("sans", 17), top + 18, COLOURS["faint"])


def compose_page():
    page = Image.new("RGB", (CANVAS, CANVAS), COLOURS["paper"])
    draw = ImageDraw.Draw(page)
    y = draw_masthead(draw)
    y = paste_hero(page, y + 18)
    draw = ImageDraw.Draw(page)
    y = draw_caption(draw, y)
    rule(draw, y + 8, 2)
    y = draw_story_grid(draw, y + 26)
    draw_footer(draw, y)
    page.save(ENTRY_FILE, optimize=True)
    return ENTRY_FILE


if __name__ == "__main__":
    written = compose_page()
    print(f"wrote {written} ({written.stat().st_size} bytes)")
