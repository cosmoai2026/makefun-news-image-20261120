#!/usr/bin/env python3
"""Build the 20 November 2026 world-news front page (1024x1024 PNG).

The page is a broadsheet-style collage: masthead, a hero illustration,
a caption, and six short stories in a two-column grid. Everything is
drawn with PIL from files that ship in this repository, so the output
is deterministic and needs no network access.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
HERO_PATH = HERE / "hero.png"
OUTPUT_PATH = HERE / "entry.png"

PAGE = 1024
MARGIN = 32
CONTENT_W = PAGE - 2 * MARGIN

PAPER = (247, 243, 234)
INK = (24, 28, 38)
FAINT = (96, 100, 110)
ACCENT = (176, 116, 28)
RULE = (24, 28, 38)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_BOLD = FONT_DIR / "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR / "DejaVuSerif.ttf"
SANS = FONT_DIR / "DejaVuSans.ttf"
SANS_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"

MASTHEAD = "20 NOVEMBER 2026"
SUBLINE = "Friday  ·  Shenzhen peace declaration  ·  Genocide ruling  ·  Anthropic debut"
CAPTION = ("A peace declaration in Shenzhen, a genocide ruling in The Hague "
           "and a blockbuster AI debut — the world on 20 November 2026.")
FOOTER = "Sources: Reuters · AP · AFP · BBC — 20 Nov 2026"

STORIES = [
    {
        "kicker": "PEACE DEAL",
        "headline": "Trump, Xi and Putin sign peace declaration",
        "summary": ("The three leaders issued a four-point joint declaration "
                    "after their first three-way summit in Shenzhen."),
    },
    {
        "kicker": "COURT",
        "headline": "World Court: Myanmar committed genocide",
        "summary": ("The ICJ ruled 9–6 that Myanmar committed genocide against "
                    "the Rohingya, a first against a state."),
    },
    {
        "kicker": "MARKETS",
        "headline": "Anthropic pops 17% in Nasdaq debut",
        "summary": ("Shares closed near $97, above the $83 offer, while the "
                    "Nikkei slid 4.8% and Asian markets fell."),
    },
    {
        "kicker": "RIYADH",
        "headline": "Houthi missiles hit Riyadh finance tower",
        "summary": ("Missiles damaged the Saudi sovereign wealth fund's PIF "
                    "tower in the capital's financial district."),
    },
    {
        "kicker": "HORMUZ",
        "headline": "Tanker ablaze after mine strike near Hormuz",
        "summary": ("A tanker caught fire east of the strait as the US war "
                    "with Iran entered its ninth month."),
    },
    {
        "kicker": "UKRAINE",
        "headline": "UK sends 1,000 drones to Ukraine",
        "summary": ("London pledged a £260 million package as Kyiv came "
                    "under ballistic missile fire."),
    },
]


def font(path, size):
    return ImageFont.truetype(str(path), size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap against a pixel width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, text, fnt, y, fill):
    width = draw.textlength(text, font=fnt)
    draw.text(((PAGE - width) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def render_masthead(draw):
    draw.rectangle([MARGIN, 30, PAGE - MARGIN, 34], fill=RULE)
    y = draw_centered(draw, MASTHEAD, font(SERIF_BOLD, 58), 46, INK)
    y = draw_centered(draw, SUBLINE, font(SANS, 19), y + 8, FAINT)
    draw.rectangle([MARGIN, y + 14, PAGE - MARGIN, y + 16], fill=RULE)
    return y + 16


def render_hero(page, top):
    hero = Image.open(HERO_PATH).convert("RGB")
    band_h = 250
    scale = max(CONTENT_W / hero.width, band_h / hero.height)
    resized = hero.resize(
        (round(hero.width * scale), round(hero.height * scale)),
        Image.LANCZOS,
    )
    left = (resized.width - CONTENT_W) // 2
    upper = (resized.height - band_h) // 2
    crop = resized.crop((left, upper, left + CONTENT_W, upper + band_h))
    page.paste(crop, (MARGIN, top))
    return top + band_h


def render_caption(draw, top):
    fnt = font(SERIF, 20)
    y = top + 12
    for line in wrap(draw, CAPTION, fnt, CONTENT_W):
        y = draw_centered(draw, line, fnt, y, FAINT) + 4
    return y


def render_story(draw, story, x, y, width):
    """Draw one story block; return the height it used."""
    kicker = font(SANS_BOLD, 16)
    draw.text((x, y), story["kicker"], font=kicker, fill=ACCENT)
    y += 23
    head = font(SERIF_BOLD, 24)
    for line in wrap(draw, story["headline"], head, width):
        draw.text((x, y), line, font=head, fill=INK)
        y += 29
    body = font(SANS, 17)
    for line in wrap(draw, story["summary"], body, width):
        draw.text((x, y), line, font=body, fill=FAINT)
        y += 22
    return y


def render_grid(draw, top):
    col_w = (CONTENT_W - 28) // 2
    y = top
    for row in range(3):
        pair = STORIES[row * 2: row * 2 + 2]
        ends = []
        for col, story in enumerate(pair):
            x = MARGIN + col * (col_w + 28)
            ends.append(render_story(draw, story, x, y, col_w))
        y = max(ends) + 14
    return y


def render_footer(draw, top):
    draw.rectangle([MARGIN, top + 6, PAGE - MARGIN, top + 8], fill=RULE)
    draw_centered(draw, FOOTER, font(SANS, 17), top + 18, FAINT)


def build_front_page():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(page)
    y = render_masthead(draw)
    y = render_hero(page, y + 18)
    draw = ImageDraw.Draw(page)
    y = render_caption(draw, y)
    draw.rectangle([MARGIN, y + 8, PAGE - MARGIN, y + 10], fill=RULE)
    y = render_grid(draw, y + 26)
    render_footer(draw, y)
    page.save(OUTPUT_PATH, optimize=True)
    return OUTPUT_PATH


if __name__ == "__main__":
    out = build_front_page()
    print(f"wrote {out} ({out.stat().st_size} bytes)")
