#!/usr/bin/env python3
"""Draw the b152 numbers-led front page: THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu/"

def f(path, size):
    return ImageFont.truetype(FD + path, size)

SERIF_B = lambda s: f("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: f("DejaVuSans.ttf", s)
SANS_B = lambda s: f("DejaVuSans-Bold.ttf", s)
SANS_I = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf", s)

INK = (18, 18, 18)
PAPER = (255, 255, 255)
GREY = (110, 110, 110)
LINE = (200, 200, 200)
NAVY = (16, 32, 64)
TEAL = (10, 60, 70)
RED = (178, 24, 24)
GOLD = (201, 162, 39)
BLUE = (28, 80, 180)
GREEN = (34, 120, 60)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def chip(x, y, label, claim=False):
    bg = RED if claim else GREEN
    fg = (255, 255, 255)
    ft = SANS_B(8)
    w = d.textlength(label, font=ft) + 10
    d.rectangle([x, y, x + w, y + 14], fill=bg)
    d.text((x + 5, y + 2), label, font=ft, fill=fg)
    return w

# ---------------------------------------------------------------- number grid
text(16, 8, "T H E   D A Y   I N   N U M B E R S", SANS_B(10), fill=GREY)
NUMBERS = [
    ("-3.3%", "KOSPI ROUT"),
    ("5.3", "US-CHINA POWER GAP"),
    ("11,762", "EBOLA CASES, DRC"),
    ("10T WON", "SEOUL RESCUE FUND"),
    ("2%", "BILLIONAIRE TAX"),
    ("$450M", "SKUBAL METS DEAL"),
    ("165", "RUSSIAN MISSILES / WEEK"),
    ("12,000", "CLEARED IN MANCHESTER"),
    ("264 KG", "EXPLOSIVES, LEBANON"),
    ("$107.3B", "ANTHROPIC IPO"),
]
for i, (val, lab) in enumerate(NUMBERS):
    col, row = i % 5, i // 5
    cx = 16 + col * 202
    y0 = 30 + row * 52
    text(cx, y0, val, SANS_B(24), fill=NAVY if row == 0 else INK)
    text(cx, y0 + 30, lab, SANS_B(8), fill=GREY)
    if col:
        d.line([(cx - 8, y0 + 2), (cx - 8, y0 + 44)], fill=LINE, width=1)
d.line([(10, 128), (1014, 128)], fill=INK, width=2)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 136, 1024, 182], fill=INK)
text(16, 144, "THE WORLD TODAY", SERIF_B(34), fill=PAPER)
text(1008, 142, "MONDAY", SANS_B(13), fill=PAPER, anchor="ra")
text(1008, 160, "23 NOVEMBER 2026", SANS_B(13), fill=GOLD, anchor="ra")

# ---------------------------------------------------------------- kicker + region bar
kicker = "AI rout rattles Asia  \u00b7  Guterres urges AI rules  \u00b7  US lead over China at record low"
text(512, 188, kicker, SANS_I(11), fill=INK, anchor="ma")
regions = "ASIA-PACIFIC 7   \u00b7   AMERICAS 8   \u00b7   MIDDLE EAST 6   \u00b7   EUROPE 5   \u00b7   AFRICA 3   \u00b7   WORLD 2"
d.rectangle([0, 206, 1024, 228], fill=(238, 238, 238))
text(512, 210, regions, SANS_B(11), fill=INK, anchor="ma")

# ---------------------------------------------------------------- hero scenes
HX = [10, 352, 694]
HW = [330, 330, 320]
# --- hero 1: Kospi skyline + falling chart
x0, y0, w = HX[0], 234, HW[0]
d.rectangle([x0, y0, x0 + w, y0 + 136], fill=NAVY)
for bx, bh in [(x0 + 14, 52), (x0 + 52, 64), (x0 + 92, 44), (x0 + 132, 58), (x0 + 176, 48), (x0 + 218, 60), (x0 + 262, 54)]:
    d.rectangle([bx, y0 + 136 - bh, bx + 34, y0 + 136], fill=(8, 18, 40))
    for wy in range(y0 + 136 - bh + 8, y0 + 128, 14):
        for wx in range(bx + 6, bx + 30, 10):
            if (wx + wy) % 29 < 18:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
text(x0 + 14, y0 + 8, "-3.3%", SANS_B(30), fill=PAPER)
text(x0 + 14, y0 + 42, "KOSPI 4,708.54  \u00b7  -161 PTS", SANS_B(9), fill=(255, 214, 90))
pts = [(x0 + 170, y0 + 96), (x0 + 205, y0 + 104), (x0 + 240, y0 + 100), (x0 + 275, y0 + 116), (x0 + 310, y0 + 128)]
d.line(pts, fill=(255, 120, 40), width=3)
for px, py in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 120, 40))
# --- hero 2: Guterres globe
x0, y0, w = HX[1], 234, HW[1]
d.rectangle([x0, y0, x0 + w, y0 + 136], fill=TEAL)
text(x0 + 14, y0 + 8, "REGULATE AI", SANS_B(20), fill=GOLD)
text(x0 + 14, y0 + 32, "BEFORE IT'S TOO LATE", SANS_B(13), fill=PAPER)
cx, cy, r = x0 + w // 2, y0 + 96, 34
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 110, 180), outline=GOLD, width=2)
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=None)
d.arc([cx - r + 8, cy - r, cx + r - 8, cy + r], 90, 270, fill=(90, 200, 120), width=3)
d.arc([cx - r + 8, cy - r, cx + r - 8, cy + r], 270, 90, fill=(90, 200, 120), width=3)
d.line([(cx - r, cy), (cx + r, cy)], fill=(90, 200, 120), width=2)
for i, c in enumerate([(200, 60, 60), (60, 120, 200), (240, 200, 60), (60, 160, 90)]):
    fx = x0 + 16 + i * 78
    d.rectangle([fx, y0 + 128, fx + 58, y0 + 134], fill=c)
# --- hero 3: Power Index bars
x0, y0, w = HX[2], 234, HW[2]
d.rectangle([x0, y0, x0 + w, y0 + 136], fill=(244, 244, 240))
text(x0 + 12, y0 + 6, "ASIA POWER INDEX 2026", SANS_B(10), fill=GREY)
bars = [("US", 78.9, BLUE, (255, 255, 255)), ("CHINA", 73.6, RED, (255, 255, 255)), ("INDIA", 40.5, GOLD, INK)]
for i, (name, val, col, fg) in enumerate(bars):
    by = y0 + 30 + i * 34
    bw = int(val / 78.9 * 250)
    d.rectangle([x0 + 12, by, x0 + 12 + bw, by + 22], fill=col)
    lab = f"{val}  {name}"
    tw = d.textlength(lab, font=SANS_B(11))
    d.text((x0 + 12 + bw - tw - 6, by + 4), lab, font=SANS_B(11), fill=fg)

HEROES = [
    ("AI ROUT HITS ASIA", "Kospi sheds 161 points as AI shares slide across the region; Samsung -3.1%, SK Hynix -2.5%.", "AP"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE", "150 delegates in Bridgetown back a risk framework \u2014 a blueprint, not a treaty.", "REUTERS"),
    ("US LEAD OVER CHINA AT RECORD LOW", "Gap narrows to 5.3, the smallest since 2018; US diplomatic influence falls 6 to 76.7.", "LOWY INSTITUTE"),
]
for i, (hl, body, src) in enumerate(HEROES):
    x0, w = HX[i], HW[i]
    lines = wrap(hl, SANS_B(14), w)
    for j, ln in enumerate(lines[:2]):
        text(x0, 376 + j * 17, ln, SANS_B(14))
    blines = wrap(body, SANS(10), w)
    for j, ln in enumerate(blines[:2]):
        text(x0, 412 + j * 13, ln, SANS(10))
    text(x0, 442, src, SANS(8), fill=GREY)
    chip(x0 + w - 62, 440, "REPORTED")

# ---------------------------------------------------------------- cards
CARDS = [
    ("BESSENT DEMANDS NVIDIA ANSWERS", "Treasury chief presses chipmaker over China sales.", "AP", False),
    ("FBI PROBES NCIC HACK", "Agents investigate breach of police database.", "REUTERS", False),
    ("TRUMP: IRAN STRIKES MAY RESUME", "President says strikes could resume in New Year.", "AP", False),
    ("NASDAQ FUTURES JUMP 3%", "Holiday week lifts futures as markets eye gains.", "BLOOMBERG", False),
    ("SKUBAL'S $450M METS DEAL", "Two-time Cy Young winner signs nine-year deal \u2014 largest ever for a pitcher.", "ESPN", False),
    ("TOM JACKSON DIES AT 75", "Former NFL star and broadcaster was 75.", "AP", False),
    ("STATES SUE SPACEX OVER AI CLAIMS", "States challenge AI safety claims in court.", "REUTERS", False),
    ("ANTHROPIC IPO: $107.3B", "Raised at $83/share 19 Nov; debut close $97.17.", "BLOOMBERG", False),
    ("POLAND: 3 RUSSIAN MISSILES CROSSED AIRSPACE", "Warsaw says three Kh-101 missiles crossed airspace.", "AP", True),
    ("INTEL WARNS OF RUSSIAN NUCLEAR SATELLITE", "US intelligence warns of orbital nuclear threat.", "REUTERS", True),
]
for i, (hl, body, src, claim) in enumerate(CARDS):
    col, row = i % 5, i // 5
    cx = 10 + col * 202
    cy = 470 + row * 92
    d.rectangle([cx, cy, cx + 194, cy + 84], outline=LINE, width=1)
    hlines = wrap(hl, SANS_B(11), 182)
    for j, ln in enumerate(hlines[:2]):
        text(cx + 6, cy + 5 + j * 13, ln, SANS_B(11))
    blines = wrap(body, SANS(9), 182)
    for j, ln in enumerate(blines[:2]):
        text(cx + 6, cy + 33 + j * 12, ln, SANS(9))
    text(cx + 6, cy + 66, src, SANS(8), fill=GREY)
    chip(cx + 194 - 68, cy + 64, "CLAIM" if claim else "REPORTED", claim)

# ---------------------------------------------------------------- map + ALSO
text(16, 652, "THE WORLD IN PINS", SANS_B(11), fill=INK)
d.line([(10, 668), (400, 668)], fill=INK, width=1)
d.polygon([(28, 700), (60, 678), (110, 680), (135, 710), (128, 770), (100, 820), (60, 825), (35, 780), (25, 740)], fill=(225, 232, 238), outline=GREY)
d.polygon([(165, 700), (220, 672), (300, 670), (360, 690), (385, 720), (370, 770), (320, 795), (250, 790), (190, 770), (165, 740)], fill=(225, 232, 238), outline=GREY)
d.polygon([(215, 785), (270, 782), (290, 810), (275, 845), (235, 848), (212, 820)], fill=(225, 232, 238), outline=GREY)
PINS = [
    (322, 692, "1"), (75, 795, "2"), (70, 720, "3"), (220, 705, "4"),
    (198, 700, "5"), (270, 688, "6"), (278, 752, "7"), (300, 722, "8"),
    (320, 755, "9"), (258, 800, "10"), (235, 820, "11"), (340, 738, "12"),
    (356, 706, "13"),
]
for px, py, n in PINS:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=PAPER, width=1)
    d.text((px, py), n, font=SANS_B(8), fill=PAPER, anchor="mm")
text(16, 852, "PINS 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Washington \u00b7 4 Paris \u00b7 5 Manchester", SANS(8), fill=GREY)
text(16, 864, "6 Kyiv \u00b7 7 Gaza \u00b7 8 Beirut \u00b7 9 Bahrain \u00b7 10 Khartoum \u00b7 11 Kinshasa \u00b7 12 Dhaka \u00b7 13 Beijing", SANS(8), fill=GREY)

text(416, 652, "ALSO ON MONDAY", SANS_B(11), fill=INK)
d.line([(410, 668), (1014, 668)], fill=INK, width=1)
ALSO = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared after scare",
    "16. Zelenskyy: 165 Russian missiles in a week",
    "17. COP31: the day after Antalya pact rejected",
    "18. Israel unity talks resume",
    "19. Gaza: two killed in Israeli strike",
    "20. West Bank settler attacks",
    "21. Iran war: no deal in sight",
    "22. Lebanon seizes 264 kg explosives",
    "23. Bahrain: Iranian strike hits plant, 2 hurt",
    "24. Benghazi: UN demands probe of port attacks [CLAIM]",
    "25. Sudan: air defences down drones over Khartoum [CLAIM]",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits over AI exam chaos",
    "29. SK Telecom -7.3%",
    "30. China eases margin rules (cuts to 80%)",
    "31. Seoul readies 10T-won stabilisation fund",
]
for i, item in enumerate(ALSO):
    col, row = i // 9, i % 9
    ax = 416 + col * 302
    ay = 676 + row * 22
    red = item.endswith("[CLAIM]")
    if red:
        item = item[:-8].rstrip()
    text(ax, ay, item, SANS(10))
    if red:
        tw = d.textlength(item, font=SANS(10))
        text(ax + tw + 4, ay, "[CLAIM]", SANS_B(9), fill=RED)

# ---------------------------------------------------------------- DATE CHECK
d.rectangle([10, 890, 1014, 978], outline=RED, width=2)
d.rectangle([10, 890, 1014, 912], fill=RED)
text(20, 894, "DATE CHECK \u2014 LEFT OUT: NOT 23 NOVEMBER", SANS_B(12), fill=PAPER)
LEFT = [
    "Democrats reach 258  (22 Nov)",
    "Sparta II fire  (22 Nov)",
    "El Chapo Isidro captured  (22 Nov)",
    "EU\u2013Indonesia pact  (21 Nov)",
    "Nigeria boat  (21 Nov)",
    "ICJ Myanmar ruling  (19 Nov)",
]
for i, item in enumerate(LEFT):
    col, row = i // 3, i % 3
    text(24 + col * 500, 920 + row * 14, "\u2022  " + item, SANS(10))
text(24, 962, "NOT YET: Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating Ebola staff", SANS(9), fill=RED)

# ---------------------------------------------------------------- footer
text(10, 988, "SOURCES: AP \u00b7 REUTERS \u00b7 AFP \u00b7 BLOOMBERG \u00b7 LOWY INSTITUTE", SANS(8), fill=GREY)
text(1014, 988, "REPORTED = confirmed by wires   \u00b7   CLAIM = one side's claim", SANS(8), fill=GREY, anchor="ra")
text(512, 1004, "THE WORLD TODAY \u00b7 MONDAY 23 NOVEMBER 2026 \u00b7 31 STORIES", SANS_B(8), fill=GREY, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
