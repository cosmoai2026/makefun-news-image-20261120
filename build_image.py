"""Render the 20 November 2026 broadsheet (1024x1024) for make.fun's
daily news-image bounty.

Layout, top to bottom: date masthead, hero illustration band, a
figures strip, thirty dated news items in three columns, a DATE CHECK
panel, and the sources line. Everything is drawn with PIL from the
story table below, so the output is byte-for-byte reproducible.

Usage: python3 build_image.py  (writes entry.png beside this file)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
HERO_FILE = ROOT / "hero.png"
OUTPUT_FILE = ROOT / "entry.png"

SIZE = 1024
EDGE = 20
NAVY = (24, 32, 54)
CREAM = (243, 236, 217)
OCHRE = (168, 124, 42)
GREY = (92, 96, 110)
HAIRLINE = (150, 138, 112)

FONT_FILES = {
    "serif_bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "sans_bold": "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "cond": "/usr/share/fonts/truetype/noto/NotoSans-Condensed.ttf",
    "cond_bold": "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf",
}
FALLBACKS = {
    "serif_bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "sans_bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "cond": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "cond_bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}


def font(kind, size):
    try:
        return ImageFont.truetype(FONT_FILES[kind], size)
    except OSError:
        return ImageFont.truetype(FALLBACKS[kind], size)


DATE_LINE = "20 NOVEMBER 2026"
THEMES = "Friday  ·  Kyiv pounded after summit  ·  Cyclone Akvan landfall  ·  COP31 deadlock"
CAPTION = ("Missiles over Kyiv hours after the peace summit, a cyclone ashore in "
           "Odisha and climate talks deadlocked — thirty stories first reported "
           "on 20 November 2026.")
FIGURES = ("100+  missiles   ·   400  drones   ·   300,000  evacuated   ·   "
           "47  trains cancelled   ·   £260m  drone package   ·   71–0  Senate vote")
DATE_CHECK = ("DATE CHECK — all 30 stories above were first reported on Friday "
              "20 November 2026. Left out as earlier news: the Shenzhen peace "
              "declaration (19 Nov), the ICJ genocide ruling (19 Nov), "
              "Anthropic’s debut (19 Nov) and the Pete Rose pardon (19 Nov).")
SOURCES = "Sources: Reuters · AP · AFP · BBC · CNN — 20 Nov 2026"

# tag | headline | summary — every item first reported on 20 Nov 2026.
ITEMS = [
    ("UKRAINE", "Russia pounds Ukraine hours after “peace” summit",
     "100+ missiles and 400 drones overnight; eight killed, 28 hurt, Kyiv bridges hit."),
    ("UKRAINE", "Trump calls Putin “tired” and ready for a deal",
     "Hours later Moscow launches one of the largest strikes of the war."),
    ("INDIA", "Cyclone Akvan makes landfall near Gopalpur",
     "Over 300,000 evacuated in Odisha; 423 rescue teams deployed, 47 trains cancelled."),
    ("CLIMATE", "COP31 draft strips out every mention of fossil fuels",
     "The slimmed text drops the $120bn adaptation target as the Friday deadline looms."),
    ("MARKETS", "Asian equities tumble as AI selloff deepens",
     "Anthropic’s blockbuster IPO fails to staunch the slide in AI stocks."),
    ("ASIA", "North Korea fires ballistic missile toward Sea of Japan",
     "South Korea’s Joint Chiefs of Staff report the Friday launch."),
    ("UK", "Britain and EU set to agree reset on food trade, youth mobility",
     "Burnham’s Brussels summit aims to mend Brexit damage a decade on."),
    ("ASIA", "Prabowo and Xi discuss South China Sea cooperation",
     "Friday talks cover the economy, investment and maritime ties."),
    ("ASIA", "Nepal’s Balendra Shah to make first state visit to India",
     "The prime minister will hold talks with Modi on bilateral ties."),
    ("POLAND", "Poland scrambles jets as objects fall inside its territory",
     "The air-threat warning is lifted at 07:30; the military investigates near the border."),
    ("EU", "Kallas: EU will summon Russian envoy over embassy damage",
     "The announcement follows the November 19 strikes in Kyiv."),
    ("UKRAINE", "UK pledges 1,000+ drones in £260m package",
     "Long-range drones and other capabilities for Kyiv."),
    ("ARGENTINA", "Senate unanimously approves disability framework",
     "71 senators back the permanent law, Friday’s statement records."),
    ("EUROPE", "Youth in 25+ countries strike over living costs",
     "Coordinated action targets housing, education and militarization."),
    ("US", "Court limits agriculture secretary’s religious emails",
     "An interim order sets boundaries on pressure over subordinates."),
    ("SANCTIONS", "US sanctions Comancheros and ’Ndrangheta",
     "Assets under US jurisdiction are blocked."),
    ("AMERICAS", "Bukele launches bid for third term",
     "An unprecedented February reelection bid in El Salvador."),
    ("MYANMAR", "Rohingya welcome verdict, demand to go home",
     "Refugees in Bangladesh greet the genocide ruling but want return."),
    ("CLIMATE", "India slips to 28th in climate performance ranking",
     "CCPI 2027 at COP31 cites coal dependence and solar curtailment."),
    ("EUROPE", "Estonia to close border crossings with Russia",
     "December closures follow an attempted attack on a defense company."),
    ("GERMANY", "Merz warns against waning support for Ukraine",
     "The chancellor urges Europe not to let backing slip."),
    ("GERMANY", "Defense minister announces drone regiment for Bundeswehr",
     "A dedicated drone unit joins the armed forces."),
    ("SPORT", "Germany wins first Chess Olympiad medal in 26 years",
     "The drought ends with a podium finish."),
    ("BRAZIL", "Lula recognizes ancestral land of Chief Raoni",
     "The president visits the 94-year-old chief; Kayapo and Yudja lands recognized."),
    ("ISRAEL", "Mosque set on fire in northern Israel",
     "The al-Dahi mosque is torched; Hebrew revenge graffiti sprayed on its walls."),
    ("ZIMBABWE", "250,000 landmines destroyed, HALO Trust says",
     "The milestone is reached in Zimbabwe’s clearance programme."),
    ("GAZA", "Rescue crews forced to respond on foot",
     "Civil defence vehicle fleet collapses under the strain."),
    ("MALAWI", "Fuel crisis triggers violence and economic strain",
     "Shortages spark unrest as prices climb."),
    ("US", "White House orders journalists to bag phones on China flight",
     "The rule applies to the return flight from China."),
    ("UKRAINE", "Russia and Ukraine agree major prisoner swap",
     "US-brokered talks in Abu Dhabi produce the deal."),
]


def wrap_text(draw, text, fnt, max_w):
    out, line = [], ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if draw.textlength(candidate, font=fnt) <= max_w:
            line = candidate
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def layout_item(draw, item, width, height_budget):
    """Return (fonts, head_lines, sum_lines) that fit the row height."""
    _, headline, summary = item
    for head_px, sum_px in ((15, 11), (14, 11), (13, 10), (12, 10)):
        head_f = font("cond_bold", head_px)
        sum_f = font("cond", sum_px)
        head_lines = wrap_text(draw, headline, head_f, width)
        sum_lines = wrap_text(draw, summary, sum_f, width)
        used = 13 + len(head_lines) * (head_px + 2) + len(sum_lines) * (sum_px + 2)
        if used <= height_budget:
            return head_f, sum_f, head_lines, sum_lines
    head_f, sum_f = font("cond_bold", 12), font("cond", 10)
    return (head_f, sum_f,
            wrap_text(draw, headline, head_f, width)[:2],
            wrap_text(draw, summary, sum_f, width)[:2])


def paint_item(draw, x, y, width, row_h, item):
    tag = item[0]
    head_f, sum_f, head_lines, sum_lines = layout_item(draw, item, width, row_h - 4)
    draw.text((x, y), tag, font=font("sans_bold", 10), fill=OCHRE)
    cursor = y + 13
    for ln in head_lines:
        draw.text((x, cursor), ln, font=head_f, fill=NAVY)
        cursor += head_f.size + 2
    for ln in sum_lines:
        draw.text((x, cursor), ln, font=sum_f, fill=GREY)
        cursor += sum_f.size + 2


def centre(draw, text, fnt, y, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((SIZE - w) / 2, y), text, font=fnt, fill=fill)


def render():
    page = Image.new("RGB", (SIZE, SIZE), CREAM)
    draw = ImageDraw.Draw(page)
    x0, x1 = EDGE, SIZE - EDGE
    span = x1 - x0

    draw.line([(x0, 14), (x1, 14)], fill=NAVY, width=3)
    centre(draw, DATE_LINE, font("serif_bold", 46), 20, NAVY)
    centre(draw, THEMES, font("cond_bold", 16), 76, OCHRE)
    draw.line([(x0, 100), (x1, 100)], fill=NAVY, width=2)

    band_y, band_h = 108, 152
    art = Image.open(HERO_FILE).convert("RGB")
    want = span / band_h
    have = art.width / art.height
    if have > want:
        crop_w = int(art.height * want)
        off = (art.width - crop_w) // 2
        art = art.crop((off, 0, off + crop_w, art.height))
    else:
        crop_h = int(art.width / want)
        off = (art.height - crop_h) // 2
        art = art.crop((0, off, art.width, off + crop_h))
    page.paste(art.resize((span, band_h), Image.LANCZOS), (x0, band_y))
    draw.rectangle([x0, band_y, x1, band_y + band_h], outline=NAVY, width=2)

    cap_f = font("cond", 13)
    cursor = band_y + band_h + 5
    for ln in wrap_text(draw, CAPTION, cap_f, span)[:1]:
        draw.text((x0, cursor), ln, font=cap_f, fill=GREY)
        cursor += 15

    strip_y = cursor + 3
    draw.rectangle([x0, strip_y, x1, strip_y + 24], fill=NAVY)
    centre(draw, FIGURES, font("cond_bold", 13), strip_y + 5, CREAM)

    grid_y, grid_end = strip_y + 32, 892
    rows = 10
    row_h = (grid_end - grid_y) // rows
    gap = 14
    col_w = (span - gap * 2) // 3
    for n, item in enumerate(ITEMS[:30]):
        col, row = divmod(n, rows)
        x = x0 + col * (col_w + gap)
        y = grid_y + row * row_h
        paint_item(draw, x, y, col_w, row_h, item)
        if row < rows - 1:
            draw.line([(x, y + row_h - 3), (x + col_w, y + row_h - 3)],
                      fill=HAIRLINE, width=1)

    panel_y = 900
    draw.rectangle([x0, panel_y, x1, panel_y + 56], outline=OCHRE, width=2)
    dc_f = font("cond_bold", 12)
    cursor = panel_y + 6
    for ln in wrap_text(draw, DATE_CHECK, dc_f, span - 16)[:3]:
        draw.text((x0 + 8, cursor), ln, font=dc_f, fill=NAVY)
        cursor += 15

    draw.line([(x0, 966), (x1, 966)], fill=NAVY, width=2)
    centre(draw, SOURCES, font("cond", 13), 974, GREY)

    page.save(OUTPUT_FILE, format="PNG", optimize=True)
    print(f"wrote {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size} bytes)")


if __name__ == "__main__":
    render()
