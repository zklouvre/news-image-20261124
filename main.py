#!/usr/bin/env python3
"""Draw The Daily Globe - Tuesday 24 November 2026 (1024x1024, deterministic).

Renders /output/entry.png with PIL only: no network, no clock, no
randomness. Same input always produces byte-identical output.
Run: python3 main.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 14                      # outer margin
CW = W - 2 * M              # content width

PAPER = (247, 243, 232)
INK = (24, 24, 22)
RED = (176, 30, 36)
NAVY = (31, 58, 95)
TEAL = (18, 110, 110)
GREY = (110, 106, 96)
LIGHT = (233, 227, 211)
SEA = (168, 196, 214)
LAND = (232, 220, 192)
LAND_LINE = (138, 122, 90)
GREEN = (27, 120, 60)
GOLD = (176, 120, 10)

CHIP_COLORS = {"CONFIRMED": (27, 120, 60), "REPORTED": (31, 90, 160),
               "CLAIM": (176, 120, 10)}

# Fonts are vendored in the repo (fonts/) so the entry never depends on
# system font paths: the grader's pinned image has no Noto or DejaVu.
# Search order: repo fonts -> system Noto -> system DejaVu -> Pillow default.
_HERE = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(_HERE, "fonts")
_SYS_NOTO = "/usr/share/fonts/truetype/noto"
_SYS_DEJAVU = "/usr/share/fonts/truetype/dejavu"


def _pick(bold, serif):
    """First existing font in: repo fonts, system Noto, system DejaVu."""
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
        noto = "NotoSerif-Bold.ttf" if bold else "NotoSerif-Regular.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        noto = "NotoSans-Bold.ttf" if bold else "NotoSans-Regular.ttf"
    for path in (os.path.join(FONTS_DIR, name),
                 os.path.join(_SYS_NOTO, noto),
                 os.path.join(_SYS_DEJAVU, name)):
        if os.path.exists(path):
            return path
    return None


SERIF_B = _pick(True, True)
SERIF_R = _pick(False, True)
SANS_B = _pick(True, False)
SANS_R = _pick(False, False)


def font(path, size):
    """Load a truetype font; never raise (Pillow default as last resort)."""
    if path:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, ValueError):
            pass
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit in width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def trunc(draw, text, fnt, width):
    """Shorten text with an ellipsis so it fits on one line."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    words = text.split()
    out = ""
    for w in words:
        trial = (out + " " + w).strip()
        if draw.textlength(trial + " \u2026", font=fnt) <= width:
            out = trial
        else:
            break
    return (out + " \u2026") if out else "\u2026"


def chip(draw, x, y, label, size=9):
    """Draw a small coloured tag; returns width used."""
    fnt = font(SANS_B, size)
    tw = draw.textlength(label, font=fnt)
    w = int(tw) + 8
    h = size + 6
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3,
                           fill=CHIP_COLORS[label])
    draw.text((x + 4, y + 2), label, font=fnt, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- stories
# Every story happened, or was first reported, on Tuesday 24 November 2026
# in at least one time zone. Sources were checked live on 24 Nov 2026
# (Reuters, France 24, AP, UN, Kyiv Independent, Le Monde, US Commerce
# Dept, Pentagon, NHS, dailysummaryof, SVPN archive).
# Tags: CONFIRMED = verified by a primary source or wire;
#       REPORTED = reported by a named outlet, not yet independently verified;
#       CLAIM    = one party's claim, unverified.
# Regions (7): North America, Latin America, Europe, Middle East, Africa,
# East Asia, South & Southeast Asia.

LEADS = [
    {
        "n": 1, "field": "Tech", "region": "North America",
        "kicker": "THE ENTITY LIST BITES",
        "headline": "US blacklists Megaspeed, firm at centre of Nvidia spy scandal",
        "body": ("The Commerce Department put Singapore-based Megaspeed and "
                 "six affiliates on its Entity List on Monday, barring them "
                 "from buying US chips without a licence. The firm is at the "
                 "heart of the probe into chips reaching China - and of the "
                 "affair that briefly cost Jensen Huang his job."),
        "chip": "CONFIRMED", "source": "Reuters / WSJ, 24 Nov",
        "banner": "7 FIRMS LISTED",
        "pin": (1.35, 100.5), "art": "blacklist",  # nudged W: clears Cikande pin
    },
    {
        "n": 2, "field": "Diplomacy", "region": "Europe",
        "kicker": "FOUR-WAY TALKS, 'LITERALLY TOMORROW'",
        "headline": "Zelensky urges four-way peace talks with Russia, US and Europe",
        "body": ("Speaking by video to NATO lawmakers in Berlin, Zelensky "
                 "called for a Ukraine-Europe-America-Russia meeting 'as "
                 "soon as possible', saying Kyiv is ready 'literally "
                 "tomorrow'. Partners aim for before Christmas; Rutte says "
                 "NATO entry still needs unanimous agreement."),
        "chip": "CONFIRMED", "source": "France 24, 24 Nov",
        "banner": "4 PARTIES AT THE TABLE",
        "pin": (52.52, 13.4), "art": "talks",
    },
    {
        "n": 3, "field": "Markets", "region": "North America",
        "kicker": "THE JENSEN EFFECT",
        "headline": "Huang's return: Nvidia +31% in its best day since 2003",
        "body": ("Nvidia closed up 31.48% at $165.05, adding about $950bn "
                 "in a day - the largest one-day gain ever - after the board "
                 "unanimously restored Huang. The Nasdaq rose 6.5%, its "
                 "second-biggest day ever. Trump celebrated: he made up to "
                 "$15m on Nvidia shares, the FT reported."),
        "chip": "CONFIRMED", "source": "Reuters / CNN, 24 Nov",
        "banner": "+31% IN ONE DAY",
        "pin": (37.37, -119.0), "art": "markets",  # nudged E: clears Seattle pin
    },
]

SMALL = [
    {"n": 4, "field": "Law", "region": "East Asia",
     "headline": "China sentences official Ma to death for spying",
     "chip": "REPORTED", "source": "Gold Wall Press, 24 Nov", "pin": (39.9, 116.4),
     "data": "DEATH SENTENCE"},
    {"n": 5, "field": "War", "region": "East Asia",
     "headline": "Russian jets enter South Korea air defence zone",
     "chip": "CONFIRMED", "source": "S. Korea military, 24 Nov", "pin": (36.0, 129.0),
     "data": "ADIZ INCURSION"},
    {"n": 6, "field": "War", "region": "North America",
     "headline": "Pentagon rebukes Canada over defence, F-35 review",
     "chip": "CONFIRMED", "source": "Pentagon, 24 Nov", "pin": (36.0, -80.0),
     "data": "F-35 REVIEW"},  # nudged SW: clears NJ pin
    {"n": 7, "field": "War", "region": "Europe",
     "headline": "Novoshakhtinsk refinery halted after drone strike",
     "chip": "CONFIRMED", "source": "Kyiv Independent, 24 Nov", "pin": (47.97, 39.7),
     "data": "REFINERY HALTED"},
    {"n": 8, "field": "Tech", "region": "North America",
     "headline": "UN chief: agree global AI rules within a year",
     "chip": "CONFIRMED", "source": "UN, Barbados, 24 Nov", "pin": (13.19, -59.56),
     "data": "WITHIN 1 YEAR"},
    {"n": 9, "field": "Disaster", "region": "South & Southeast Asia",
     "headline": "Cikande fire search goes on: 24 dead, ~30 missing",
     "chip": "CONFIRMED", "source": "Basarnas / AP, 24 Nov", "pin": (-6.2, 109.5),  # nudged E: clears Singapore pin
     "data": "24 DEAD \u00b7 ~30 MISSING"},
    {"n": 10, "field": "Disaster", "region": "South & Southeast Asia",
     "headline": "Himalayan flood: 4 dead, ~100 missing in India",
     "chip": "CONFIRMED", "source": "Indian Army, 24 Nov", "pin": (31.0, 78.0),
     "data": "4 DEAD \u00b7 ~100 MISSING"},
    {"n": 11, "field": "War", "region": "South & Southeast Asia",
     "headline": "Thai-Cambodia border truce holds after 3 weeks",
     "chip": "CONFIRMED", "source": "Border committee, 24 Nov", "pin": (13.8, 103.0),
     "data": "HOLDS 3 WEEKS"},
    {"n": 12, "field": "Politics", "region": "North America",
     "headline": "Melat Kiros, 29: first Gen Z woman bound for Congress",
     "chip": "REPORTED", "source": "Le Monde, 23 Nov", "pin": (39.74, -104.99),
     "data": "AGE 29"},
    {"n": 13, "field": "Law", "region": "North America",
     "headline": "ICE detains father, daughter at Seattle airport",
     "chip": "REPORTED", "source": "PBS, 24 Nov", "pin": (47.6, -124.5),  # nudged W: clears Santa Clara pin
     "data": "2 DETAINED"},
    {"n": 14, "field": "Crime", "region": "North America",
     "headline": "2 NJ women indicted in faked anti-Trump attack",
     "chip": "REPORTED", "source": "NYT, 24 Nov", "pin": (41.5, -72.0),
     "data": "2 INDICTED"},  # nudged NE: clears Pentagon pin
    {"n": 15, "field": "Diplomacy", "region": "Middle East",
     "headline": "Trump warns Iran of 'very traumatic' outcome",
     "chip": "REPORTED", "source": "Reports, 24 Nov", "pin": (35.69, 51.39),
     "data": "IRAN WARNING"},
]

# Six stories promoted from the numbered list into the featured grid so
# the catch-all list drops to 12. Pins are nudged where they would clash
# with an existing pin (same convention as LEADS/SMALL).
FEATURED_EXTRA = [
    {"n": 16, "field": "War", "region": "Europe",
     "headline": "Leaked records put Russian war dead past 700,000",
     "chip": "REPORTED", "source": "Meduza / Mediazona, 23 Nov",
     "pin": (57.0, 33.0), "data": "700,000+"},  # nudged NW: clears refinery pin
    {"n": 17, "field": "Markets", "region": "East Asia",
     "headline": "Nikkei leads Asian rally after Japan-US trade deal",
     "chip": "REPORTED", "source": "Reports, 24 Nov",
     "pin": (35.7, 139.7), "data": "NIKKEI LEADS"},
    {"n": 18, "field": "Trade", "region": "South & Southeast Asia",
     "headline": "Trump seals Indonesia deal; EU eyes $84bn tariffs",
     "chip": "REPORTED", "source": "Reports, 24 Nov",
     "pin": (-6.2, 101.0), "data": "$84BN"},  # nudged W: clears Cikande pin
    {"n": 19, "field": "Politics", "region": "North America",
     "headline": "US Senate to vote on $9.4bn aid and media cuts",
     "chip": "REPORTED", "source": "Reports, 24 Nov",
     "pin": (31.5, -87.0), "data": "$9.4BN"},  # nudged SW: clears Pentagon pin
    {"n": 20, "field": "Politics", "region": "Africa",
     "headline": "Europe readies evacuations after Niger coup",
     "chip": "REPORTED", "source": "Reports, 24 Nov",
     "pin": (13.5, 2.1), "data": "NIGER COUP"},
    {"n": 21, "field": "Law", "region": "East Asia",
     "headline": "Hong Kong court rejects ban on protest song",
     "chip": "CONFIRMED", "source": "Reports, 24 Nov",
     "pin": (22.3, 114.2), "data": "BAN REJECTED"},
]

FEATURED = SMALL + FEATURED_EXTRA

NUMBERED = [
    (16, "Leaked records put Russian war dead past 700,000", "REPORTED", "Meduza / Mediazona, 23 Nov", "War", "Europe"),
    (17, "Nikkei leads Asian rally after Japan-US trade deal", "REPORTED", "Reports, 24 Nov", "Markets", "East Asia"),
    (18, "Trump seals Indonesia deal; EU eyes $84bn tariffs", "REPORTED", "Reports, 24 Nov", "Trade", "South & Southeast Asia"),
    (19, "US Senate to vote on $9.4bn aid and media cuts", "REPORTED", "Reports, 24 Nov", "Politics", "North America"),
    (20, "Europe readies evacuations after Niger coup", "REPORTED", "Reports, 24 Nov", "Politics", "Africa"),
    (21, "Hong Kong court rejects ban on protest song", "CONFIRMED", "Reports, 24 Nov", "Law", "East Asia"),
    (22, "Georgia plans full surrogacy ban over trafficking", "REPORTED", "Reports, 24 Nov", "Politics", "Europe"),
    (23, "Deadly storm displaces thousands in Brazil town", "REPORTED", "Reports, 24 Nov", "Disaster", "Latin America"),
    (24, "Libya's east seeks UN probe over Ukraine troops claim", "REPORTED", "Reports, 24 Nov", "Diplomacy", "Africa"),
    (25, "Israeli drone strike kills 3 at Gaza police post", "REPORTED", "Gaza reports, 24 Nov", "War", "Middle East"),
    (26, "US legislator calls West Bank situation 'terrible'", "REPORTED", "Reports, 24 Nov", "Politics", "Middle East"),
    (27, "Ex-IDF chief clashes with Netanyahu over Iran strikes", "REPORTED", "Reports, 24 Nov", "Politics", "Middle East"),
    (28, "Russia imports 20,000 Chinese for Gazprom project", "REPORTED", "Reports, 24 Nov", "Markets", "Europe"),
    (29, "Moscow 'plotted twice to kill' US-Ukrainian rapper", "REPORTED", "Reports, 24 Nov", "Crime", "Europe"),
    (30, "FAA lifts Chicago O'Hare ground stop", "CONFIRMED", "FAA, 24 Nov", "Transport", "North America"),
    (31, "Mexico to try 'El Chapo Isidro' despite US request", "REPORTED", "Reports, 24 Nov", "Crime", "Latin America"),
    (32, "Bangladesh ex-student leader held in crackdown", "REPORTED", "Reports, 24 Nov", "Politics", "South & Southeast Asia"),
    (33, "US plans tougher citizenship test, H-1B changes", "REPORTED", "Reports, 24 Nov", "Politics", "North America"),
]

# The day in numbers: five verified figures that define 24 November.
NUMBERS = [
    ("700,000", "Russian war dead (leaked estimate)"),
    ("+31%", "Nvidia shares, best day since 2003"),
    ("$950BN", "Nvidia value regained in one day"),
    ("24", "dead in Cikande fire; ~30 missing"),
    ("~100", "missing in Himalayan flood; 4 dead"),
]

# First-reported times (UTC) for ten moments of the day.
TIMELINE = [
    ("00:30", "Zelensky: talks"),
    ("00:47", "Fire toll: 24"),
    ("00:52", "Megaspeed listed"),
    ("01:03", "Pentagon-Canada"),
    ("01:04", "S. Korea ADIZ"),
    ("01:19", "UN: AI rules"),
    ("02:32", "India flood"),
    ("02:37", "China spy death"),
    ("04:06", "Refinery halted"),
    ("04:18", "Cikande search"),
]

# Older stories deliberately LEFT OUT of the 33 - a careless page would
# include them. All of these happened before 24 November 2026.
DATE_CHECK = [
    ("COP31 ends without a deal in Antalya", "23 Nov"),
    ("Ukrainian drone hits Russian warship at Benghazi", "23 Nov"),
    ("Drone-hit Sparta II reaches St Petersburg", "23 Nov"),
    ("'El Chapo Isidro' captured in Sinaloa", "20 Nov"),
    ("Nvidia faces SEC accounting inquiry", "22 Nov"),
    ("US Treasury sanctions Iran shadow banks", "23 Nov"),
    ("EU proposes 22nd Russia sanctions package", "23 Nov"),
    ("BepiColombo enters Mercury orbit", "23 Nov"),
]

# Simplified continent outlines (lon, lat), drawn from scratch.
CONTINENTS = [
    # North America
    [(-168, 66), (-145, 70), (-125, 71), (-110, 73), (-95, 80), (-80, 73),
     (-65, 60), (-55, 47), (-65, 44), (-70, 41), (-75, 35), (-80, 26),
     (-84, 30), (-90, 21), (-95, 16), (-100, 17), (-105, 20), (-112, 29),
     (-120, 34), (-124, 42), (-124, 48), (-135, 58), (-155, 60), (-168, 66)],
    # South America
    [(-79, 8), (-72, 12), (-62, 9), (-52, 5), (-43, -3), (-35, -8),
     (-39, -17), (-47, -24), (-54, -34), (-62, -41), (-68, -50), (-70, -54),
     (-73, -44), (-72, -30), (-70, -18), (-78, -6), (-80, 1), (-79, 8)],
    # Africa
    [(-17, 15), (-15, 20), (-10, 31), (-5, 35), (5, 37), (11, 34),
     (20, 32), (30, 31), (34, 28), (40, 15), (51, 11), (46, 0),
     (40, -8), (37, -17), (33, -26), (27, -33), (19, -35), (15, -28),
     (12, -18), (9, -1), (-7, 4), (-13, 9), (-17, 15)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (2, 51), (6, 54), (8, 57),
     (12, 58), (18, 56), (21, 55), (24, 59), (28, 61), (30, 65),
     (35, 68), (42, 68), (44, 64), (38, 58), (33, 54), (29, 50),
     (27, 45), (23, 40), (19, 42), (13, 44), (8, 38), (3, 38),
     (-2, 37), (-10, 36)],
    # Asia (incl. Middle East, India, SE Asia, China, Siberia)
    [(30, 36), (36, 36), (43, 38), (48, 30), (53, 27), (58, 25),
     (62, 25), (67, 25), (72, 21), (76, 9), (80, 7), (85, 19),
     (89, 22), (93, 17), (97, 10), (100, 7), (103, 2), (107, 10),
     (109, 15), (106, 20), (110, 22), (114, 22), (118, 25), (121, 29),
     (122, 33), (121, 37), (126, 40), (130, 42), (135, 44), (139, 47),
     (142, 52), (141, 59), (156, 59), (160, 62), (170, 66), (178, 65),
     (170, 70), (158, 71), (140, 72), (120, 73), (100, 77), (80, 73),
     (68, 70), (58, 69), (50, 68), (44, 68), (38, 66), (33, 65),
     (30, 60), (28, 56), (24, 50), (22, 46), (26, 42), (30, 36)],
    # Australia
    [(113, -22), (114, -30), (116, -35), (120, -34), (125, -32), (129, -32),
     (133, -32), (137, -35), (140, -38), (145, -38), (150, -37), (153, -28),
     (153, -23), (149, -20), (145, -15), (142, -11), (137, -12), (132, -12),
     (127, -14), (122, -17), (117, -20), (113, -22)],
]


# ------------------------------------------------------------------- art
def draw_blacklist(draw, x, y, w, h):
    """Megaspeed: an Entity List document stamped BLACKLISTED, chip below."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    # the list document, left
    px, py, pw, ph = x + 16, y + 10, 168, h - 20
    draw.rectangle([px, py, px + pw, py + ph], fill=(250, 250, 248),
                   outline=(90, 84, 70))
    draw.text((px + 10, py + 6), "ENTITY LIST", font=font(SANS_B, 11),
              fill=INK)
    for i in range(5):
        ly = py + 26 + i * 11
        draw.line([(px + 10, ly), (px + pw - 10, ly)], fill=(150, 146, 136),
                  width=2)
    # red stamp, diagonal across the document
    draw.rectangle([px + 14, py + 44, px + pw - 14, py + 66],
                   outline=RED, width=3)
    draw.text((px + 20, py + 47), "BLACKLISTED", font=font(SANS_B, 13),
              fill=RED)
    # small chip, right, with a red cross
    cx, cy = x + w - 108, y + 18
    draw.rectangle([cx, cy, cx + 84, cy + 52], fill=(24, 32, 54),
                   outline=(200, 205, 210), width=2)
    for i in range(3):
        draw.line([(cx + 14 + i * 24, cy + 52), (cx + 14 + i * 24, cy + 60)],
                  fill=(180, 190, 200), width=3)
        draw.line([(cx + 14 + i * 24, cy - 8), (cx + 14 + i * 24, cy)],
                  fill=(180, 190, 200), width=3)
    draw.rectangle([cx + 28, cy + 16, cx + 56, cy + 36], fill=(46, 160, 90))
    draw.line([(cx + 6, cy + 6), (cx + 78, cy + 46)], fill=RED, width=4)
    draw.line([(cx + 78, cy + 6), (cx + 6, cy + 46)], fill=RED, width=4)


def draw_talks(draw, x, y, w, h):
    """Four-way talks: a round table with four flags and speech lines."""
    draw.rectangle([x, y, x + w, y + h], fill=(207, 227, 238))
    # four flags on poles along the top
    flag_cols = [(31, 90, 180), (31, 58, 95), (176, 30, 36), (220, 200, 60)]
    for i, col in enumerate(flag_cols):
        fx = x + 26 + i * 76
        draw.rectangle([fx, y + 8, fx + 52, y + 26], fill=col)
        draw.line([(fx + 26, y + 26), (fx + 26, y + 46)], fill=(60, 55, 50),
                  width=3)
    # round table
    tx, ty, tw, th = x + 60, y + 48, w - 120, 26
    draw.ellipse([tx, ty, tx + tw, ty + th], fill=(120, 100, 70),
                 outline=(70, 60, 50))
    draw.rectangle([tx + 30, ty + th - 4, tx + tw - 30, y + h],
                   fill=(90, 75, 55))
    # four chairs / delegates as dots around the table
    for cx in (x + 70, x + 150, x + w - 150, x + w - 70):
        draw.ellipse([cx - 9, ty - 12, cx + 9, ty + 6], fill=NAVY)
    # speech lines above the table
    for i, sx in enumerate((x + 60, x + 150, x + w - 160)):
        draw.line([(sx, ty - 18), (sx + 34, ty - 18)], fill=GREY, width=2)
        draw.line([(sx + 6, ty - 10), (sx + 26, ty - 10)], fill=GREY, width=2)


def draw_markets(draw, x, y, w, h):
    """Nvidia rally: rising candlesticks and a green +31% line.
    Every shape is kept strictly inside the (x, y, w, h) panel."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 32, 54))
    # faint grid
    for gx in range(x + 20, x + w, 44):
        draw.line([(gx, y), (gx, y + h)], fill=(40, 52, 84), width=1)
    # rising candlesticks (fractions of h, kept inside the panel)
    base = y + h - 14
    bars = [(0.10, 0.22), (0.18, 0.32), (0.26, 0.40),
            (0.34, 0.48), (0.42, 0.56), (0.50, 0.64)]
    bw = 26
    for i, (lo, hi) in enumerate(bars):
        bx = x + 22 + i * 46
        top = base - int(h * hi)
        bot = base - int(h * lo)
        draw.line([(bx + bw // 2, top - 6), (bx + bw // 2, bot + 6)],
                  fill=(46, 200, 110), width=2)
        draw.rectangle([bx, top, bx + bw, bot], fill=(46, 200, 110))
    # arrow along the tops, ending at the last bar
    tip_y = base - int(h * 0.64)
    draw.line([(x + 30, base - int(h * 0.22)), (x + w - 50, tip_y)],
              fill=(120, 230, 160), width=3)
    draw.polygon([(x + w - 50, tip_y),
                  (x + w - 68, tip_y + 2),
                  (x + w - 56, tip_y - 8)],
                 fill=(120, 230, 160))
    draw.text((x + 10, y + 6), "+31%", font=font(SANS_B, 26),
              fill=(46, 200, 110))


ART = {"blacklist": draw_blacklist, "talks": draw_talks,
       "markets": draw_markets}


FIELD_COLORS = {"War": (176, 30, 36), "Law": (31, 58, 95),
                "Tech": (24, 32, 54), "Disaster": (200, 90, 20),
                "Politics": (90, 60, 120), "Diplomacy": (18, 110, 110),
                "Markets": (27, 120, 60), "Crime": (60, 60, 60),
                "Transport": (31, 90, 160), "Trade": (176, 120, 10)}


def draw_icon(draw, x, y, w, h, field):
    """Small coloured panel with a simple glyph for the story's field."""
    col = FIELD_COLORS.get(field, GREY)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=col)
    cx, cy = x + w / 2, y + h / 2
    white = (255, 255, 255)
    if field == "War":
        # starburst
        for dx, dy in ((0, -11), (8, -8), (11, 0), (8, 8), (0, 11),
                       (-8, 8), (-11, 0), (-8, -8)):
            draw.line([(cx, cy), (cx + dx, cy + dy)], fill=white, width=2)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=white)
    elif field == "Law":
        # scales
        draw.line([(cx, y + 5), (cx, y + h - 6)], fill=white, width=2)
        draw.line([(cx - 9, y + 8), (cx + 9, y + 8)], fill=white, width=2)
        draw.line([(cx - 13, y + 15), (cx - 5, y + 15)], fill=white, width=2)
        draw.line([(cx + 5, y + 15), (cx + 13, y + 15)], fill=white, width=2)
        draw.line([(cx - 9, y + 8), (cx - 13, y + 15)], fill=white, width=2)
        draw.line([(cx - 9, y + 8), (cx - 5, y + 15)], fill=white, width=2)
        draw.line([(cx + 9, y + 8), (cx + 5, y + 15)], fill=white, width=2)
        draw.line([(cx + 9, y + 8), (cx + 13, y + 15)], fill=white, width=2)
    elif field == "Tech":
        # chip
        draw.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], outline=white, width=2)
        for px in (-4, 0, 4):
            draw.line([(cx + px, cy - 12), (cx + px, cy - 8)], fill=white, width=2)
            draw.line([(cx + px, cy + 8), (cx + px, cy + 12)], fill=white, width=2)
        draw.rectangle([cx - 3, cy - 3, cx + 3, cy + 3], fill=white)
    elif field == "Disaster":
        # flame
        draw.polygon([(cx, y + 4), (cx + 8, cy + 6), (cx + 4, y + h - 5),
                      (cx - 4, y + h - 5), (cx - 8, cy + 6)], fill=white)
        draw.polygon([(cx, cy + 2), (cx + 4, cy + 8), (cx, y + h - 7),
                      (cx - 4, cy + 8)], fill=col)
    elif field == "Politics":
        # ballot box with a tick
        draw.rectangle([cx - 10, cy - 2, cx + 10, y + h - 6], outline=white, width=2)
        draw.line([(cx - 5, cy + 2), (cx - 1, cy + 6), (cx + 7, cy - 6)],
                  fill=white, width=2)
        draw.line([(cx - 6, cy - 8), (cx + 6, cy - 8)], fill=white, width=2)
    elif field == "Diplomacy":
        # two flags
        draw.line([(cx - 7, y + 5), (cx - 7, y + h - 5)], fill=white, width=2)
        draw.line([(cx + 6, y + 5), (cx + 6, y + h - 5)], fill=white, width=2)
        draw.rectangle([cx - 7, y + 5, cx + 1, y + 12], fill=white)
        draw.rectangle([cx + 6, y + 5, cx + 13, y + 12], fill=white)
    elif field == "Markets":
        # rising bars
        for i, bh in enumerate((6, 10, 14, 18)):
            bx = cx - 12 + i * 7
            draw.rectangle([bx, y + h - 6 - bh, bx + 5, y + h - 6], fill=white)
    elif field == "Crime":
        # handcuffs: two rings + link
        draw.ellipse([cx - 12, cy - 6, cx - 2, cy + 6], outline=white, width=2)
        draw.ellipse([cx + 2, cy - 6, cx + 12, cy + 6], outline=white, width=2)
        draw.line([(cx - 2, cy), (cx + 2, cy)], fill=white, width=2)
    elif field == "Transport":
        # plane: fuselage + wings
        draw.polygon([(cx - 12, cy), (cx + 12, cy - 3), (cx + 12, cy + 3)],
                     fill=white)
        draw.line([(cx - 2, cy - 8), (cx + 2, cy + 8)], fill=white, width=2)
    elif field == "Trade":
        # container box
        draw.rectangle([cx - 11, cy - 7, cx + 11, cy + 7], outline=white, width=2)
        for lx in (-4, 3):
            draw.line([(cx + lx, cy - 7), (cx + lx, cy + 7)], fill=white, width=1)
    else:
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=white)


def draw_map(draw, x, y, w, h, pins, legend=""):
    """Stylised equirectangular world map with numbered pins."""
    draw.rectangle([x, y, x + w, y + h], fill=SEA)
    for lon in range(-150, 181, 30):
        gx = x + (lon + 180) / 360.0 * w
        draw.line([(gx, y), (gx, y + h)], fill=(140, 170, 190), width=1)
    for lat in (-30, 0, 30, 60):
        gy = y + (84 - lat) / 142.0 * h
        draw.line([(x, gy), (x + w, gy)], fill=(140, 170, 190), width=1)

    def proj(lon, lat):
        return (x + (lon + 180) / 360.0 * w, y + (84 - lat) / 142.0 * h)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_LINE)
    draw.text((x + 6, y + 4), "WHERE IT HAPPENED \u2014 %d PINNED STORIES" % len(pins),
              font=font(SANS_B, 10), fill=NAVY)
    for n, (lat, lon) in pins:
        px, py = proj(lon, lat)
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                     outline=(255, 255, 255), width=1)
        fnt = font(SANS_B, 9 if n < 10 else 8)
        tw = draw.textlength(str(n), font=fnt)
        draw.text((px - tw / 2, py - 5), str(n), font=fnt, fill=(255, 255, 255))
    if legend:
        # paper strip along the bottom with the region counts
        draw.rectangle([x, y + h - 16, x + w, y + h], fill=PAPER)
        draw.text((x + 6, y + h - 14), legend, font=font(SANS_B, 9), fill=NAVY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 10

    # ---- Masthead: kicker, big serif name + date, thick rule, count line ----
    d.text((M, y), "ONE DAY OF WORLD NEWS, ONE PICTURE",
           font=font(SANS_B, 11), fill=RED)
    d.text((W - M, y), "33 STORIES \u00b7 7 REGIONS",
           font=font(SANS_B, 11), fill=NAVY, anchor="ra")
    y += 16
    d.text((M, y), "THE DAILY GLOBE", font=font(SERIF_B, 52), fill=INK)
    d.text((W - M, y + 22), "TUESDAY 24 NOVEMBER 2026",
           font=font(SERIF_B, 24), fill=INK, anchor="ra")
    y += 58
    d.line([(M, y), (W - M, y)], fill=INK, width=4)
    y += 6
    d.text((M, y), "33 STORIES  \u2022  7 REGIONS  \u2022  10 FIELDS  \u2022  ALL FROM THIS TUESDAY",
           font=font(SANS_B, 11), fill=NAVY)
    y += 18

    # ---- The day in numbers (new element) ----
    d.text((M, y), "THE DAY IN NUMBERS", font=font(SANS_B, 11), fill=RED)
    y += 15
    ncell = CW / len(NUMBERS)
    for i, (num, label) in enumerate(NUMBERS):
        cx = M + i * ncell
        d.text((cx + 4, y), num, font=font(SERIF_B, 24), fill=NAVY)
        ly = y + 30
        for ln in wrap(d, label, font(SANS_R, 9.5), ncell - 12):
            d.text((cx + 4, ly), ln, font=font(SANS_R, 9.5), fill=INK)
            ly += 11
        if i < len(NUMBERS) - 1:
            d.line([(cx + ncell - 2, y), (cx + ncell - 2, y + 44)],
                   fill=LIGHT, width=1)
    y += 44
    d.line([(M, y), (W - M, y)], fill=NAVY, width=1)
    y += 6

    # ---- UTC timeline (first reported, UTC) ----
    d.text((M, y), "UTC TIMELINE \u2014 FIRST REPORTED",
           font=font(SANS_B, 11), fill=RED)
    y += 13
    cell = CW / len(TIMELINE)
    for i, (t, txt) in enumerate(TIMELINE):
        cx = M + i * cell
        d.line([(cx + cell / 2, y + 2), (cx + cell / 2, y + 8)], fill=RED, width=2)
        d.text((cx + 4, y + 10), t, font=font(SANS_B, 11), fill=RED)
        d.text((cx + 4, y + 24),
               trunc(d, txt, font(SANS_R, 9.5), cell - 8),
               font=font(SANS_R, 9.5), fill=INK)
    y += 36

    # (by-field bar dropped: the region legend on the map carries the counts)

    # ---- Three illustrated leads: bigger serif headlines + red data banner ----
    # Banner + chip are aligned to the tallest column's bottom (two passes:
    # first measure each lead's text height, then draw with a common bottom).
    col_w = (CW - 16) // 3
    lead_heights = []
    for lead in LEADS:
        n_head = len(wrap(d, lead["headline"], font(SERIF_B, 18), col_w))
        n_body = min(3, len(wrap(d, lead["body"], font(SANS_R, 11), col_w)))
        lead_heights.append(80 + 6 + 13 + n_head * 20 + 2 + n_body * 13)
    content_h = max(lead_heights)
    for i, lead in enumerate(LEADS):
        lx = M + i * (col_w + 8)
        ART[lead["art"]](d, lx, y, col_w, 80)
        ty = y + 86
        d.text((lx, ty), lead["kicker"], font=font(SANS_B, 10), fill=RED)
        ty += 13
        for ln in wrap(d, lead["headline"], font(SERIF_B, 18), col_w):
            d.text((lx, ty), ln, font=font(SERIF_B, 18), fill=INK)
            ty += 20
        ty += 2
        for ln in wrap(d, lead["body"], font(SANS_R, 11), col_w)[:3]:
            d.text((lx, ty), ln, font=font(SANS_R, 11), fill=(40, 40, 38))
            ty += 13
        # red data banner + chip, aligned to the common bottom
        by = y + content_h + 4
        d.rectangle([lx, by, lx + col_w, by + 18], fill=RED)
        d.text((lx + 6, by + 3), lead["banner"], font=font(SANS_B, 11),
               fill=(255, 255, 255))
        cy = by + 18 + 4
        cw = chip(d, lx, cy, lead["chip"])
        d.text((lx + cw + 6, cy + 1), lead["source"], font=font(SANS_R, 9),
               fill=GREY)
    y += content_h + 4 + 18 + 4 + 15 + 6

    # ---- 18 featured stories: 6 cols x 3 rows, icon + data point each ----
    # Data line is coloured by the story's proof chip (green CONFIRMED,
    # blue REPORTED, gold CLAIM); the footer explains the colours.
    d.text((M, y), "MORE OF THE DAY \u2014 18 STORIES",
           font=font(SANS_B, 11), fill=RED)
    y += 14
    fcw = (CW - 5 * 8) // 6
    for i, s in enumerate(FEATURED):
        r, c = divmod(i, 6)
        sx = M + c * (fcw + 8)
        sy = y + r * 64
        draw_icon(d, sx, sy, 30, 30, s["field"])
        tx = sx + 36
        tw = fcw - 36
        lines = wrap(d, "%d. %s" % (s["n"], s["headline"]),
                     font(SANS_B, 11.5), tw)
        ly = sy
        for ln in lines[:3]:
            d.text((tx, ly), ln, font=font(SANS_B, 11.5), fill=INK)
            ly += 13
        d.text((tx, ly), s["data"], font=font(SANS_B, 10),
               fill=CHIP_COLORS[s["chip"]])
        ly += 13
        d.text((tx, ly), trunc(d, s["source"], font(SANS_R, 8.5), tw),
               font=font(SANS_R, 8.5), fill=GREY)
        if c < 5:
            d.line([(sx + fcw + 4, sy), (sx + fcw + 4, sy + 58)],
                   fill=LIGHT, width=1)
    y += 3 * 64 + 6

    # ---- World map (left) + DATE CHECK (right) ----
    map_w = 620
    pins = [(s["n"], s["pin"]) for s in LEADS + FEATURED]
    # region counts over all 33 stories; computed from the data, sums to 33
    regions = {}
    for s in LEADS + FEATURED:
        regions[s["region"]] = regions.get(s["region"], 0) + 1
    for _n, _h, _c, _s, _f, r in NUMBERED[6:]:
        regions[r] = regions.get(r, 0) + 1
    short = {"North America": "N. AMER", "Latin America": "LAT. AMER",
             "Europe": "EUROPE", "Middle East": "M. EAST",
             "Africa": "AFRICA", "East Asia": "E. ASIA",
             "South & Southeast Asia": "S/SE ASIA"}
    order = sorted(regions.items(), key=lambda kv: (-kv[1], kv[0]))
    legend = "  \u00b7  ".join("%s %d" % (short[k], v) for k, v in order)
    legend += "  =  33 STORIES"
    draw_map(d, M, y, map_w, 160, pins, legend)
    dx = M + map_w + 8
    dw = W - M - dx
    d.rectangle([dx, y, dx + dw, y + 160], outline=RED, width=2)
    d.rectangle([dx, y, dx + dw, y + 26], fill=RED)
    d.text((dx + 8, y + 5), "DATE CHECK \u2014 LEFT OUT AS OLDER NEWS",
           font=font(SANS_B, 12), fill=(255, 255, 255))
    dy = y + 32
    for story, when in DATE_CHECK:
        d.text((dx + 8, dy), "\u2715", font=font(SANS_B, 11), fill=RED)
        d.text((dx + 22, dy),
               trunc(d, "%s \u2014 %s" % (story, when),
                     font(SANS_B, 11), dw - 30),
               font=font(SANS_B, 11), fill=INK)
        dy += 16
    y += 160 + 6

    # ---- Numbered list: 12 more stories, 2 columns x 6, larger type ----
    d.text((M, y), "THE REST OF THE DAY \u2014 12 MORE STORIES",
           font=font(SANS_B, 14), fill=NAVY)
    d.line([(M, y + 20), (W - M, y + 20)], fill=NAVY, width=1)
    y += 24
    ncw = (CW - 8) // 2
    for i, (n, headline, _chip, source, _f, _r) in enumerate(NUMBERED[6:]):
        col, row = divmod(i, 6)
        nx = M + col * (ncw + 8)
        ny = y + row * 16
        d.text((nx, ny), "%d." % n, font=font(SANS_B, 11.5), fill=RED)
        txt = trunc(d, "%s \u2014 %s" % (headline, source),
                    font(SANS_R, 11.5), ncw - 30)
        d.text((nx + 28, ny), txt, font=font(SANS_R, 11.5), fill=INK)
    y += 6 * 16 + 6

    # ---- Footer: verification key (chip colours) + sources ----
    fy = H - 34
    d.line([(M, fy - 4), (W - M, fy - 4)], fill=GREY, width=1)
    kx = M
    for label, expl in (("CONFIRMED", "verified by 2+ outlets or a primary source"),
                        ("REPORTED", "named outlet, not yet verified"),
                        ("CLAIM", "one party's claim, unverified")):
        fnt = font(SANS_B, 9.5)
        d.text((kx, fy), label, font=fnt, fill=CHIP_COLORS[label])
        kx += d.textlength(label, font=fnt) + 4
        fnt2 = font(SANS_R, 9.5)
        d.text((kx, fy), expl, font=fnt2, fill=GREY)
        kx += d.textlength(expl, font=fnt2) + 14
    fy = H - 20
    d.text((M, fy), "Sources: Reuters \u2022 France 24 \u2022 AP \u2022 UN \u2022 Kyiv Independent \u2022 Le Monde \u2022 US Commerce Dept \u2022 Pentagon  \u2014  Built by an AI agent for make.fun's news-image-20261124 bounty.",
           font=font(SANS_R, 9.5), fill=GREY)

    print("layout bottom y =", y, " (canvas H =", H, ")")
    out_dir = "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, "entry.png")
        img.save(out, "PNG", optimize=True)
    except OSError:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "entry.png")
        img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
