#!/usr/bin/env python3
"""Draw the news-23 b152 heroes-scene front page (1024x1024)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

INK = (17, 17, 17)
PAPER = (255, 255, 255)
GRAY = (85, 85, 85)
LGRAY = (232, 232, 232)
RED = (176, 0, 32)
NAVY = (14, 42, 71)
TEAL = (11, 61, 58)
GOLD = (201, 162, 39)
GREEN = (27, 122, 61)
CREAM = (250, 246, 235)
MAPBLUE = (203, 216, 228)
MAPLINE = (150, 170, 190)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def chip(d, x, y, text, fill):
    f = font(SANS_B, 8)
    tw = f.getlength(text)
    d.rounded_rectangle([x, y, x + tw + 10, y + 13], radius=3, fill=fill)
    d.text((x + 5, y + 2), text, font=f, fill=PAPER)


def hero_scene_kospi(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY)
    # buildings with lit windows
    import random
    rnd = random.Random(23)
    bx = x0 + 8
    while bx < x0 + w - 30:
        bw = rnd.randint(26, 44)
        bh = rnd.randint(55, 105)
        by = y0 + h - bh
        d.rectangle([bx, by, bx + bw, y0 + h], fill=(24, 58, 92))
        for wy in range(by + 6, y0 + h - 6, 12):
            for wx in range(bx + 4, bx + bw - 4, 10):
                if rnd.random() < 0.45:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
        bx += bw + 6
    # falling orange chart line
    pts = [(x0 + 185, y0 + 26), (x0 + 220, y0 + 44), (x0 + 255, y0 + 40),
           (x0 + 290, y0 + 66), (x0 + 318, y0 + 88)]
    d.line(pts, fill=(255, 140, 40), width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 140, 40))
    d.text((x0 + 12, y0 + 14), "-3.3%", font=font(SANS_B, 36), fill=PAPER)
    d.text((x0 + 12, y0 + 58), "KOSPI 4,708.54", font=font(SANS_B, 13), fill=(255, 214, 90))
    d.text((x0 + 12, y0 + 78), "-161 PTS - INTRADAY -5.8%", font=font(SANS, 10), fill=(200, 210, 225))
    d.text((x0 + 12, y0 + h - 22), "SAMSUNG -3.1% - SK HYNIX -2.5%",
           font=font(SANS_B, 10), fill=PAPER)


def hero_scene_guterres(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=TEAL)
    # globe, masked circle
    cx, cy, r = x0 + 78, y0 + 72, 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(28, 110, 102))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    for k in range(-2, 3):
        d.arc([cx - r + abs(k) * 18, cy - r, cx + r - abs(k) * 18, cy + r],
              90, 270, fill=(180, 220, 215), width=1)
        d.arc([cx - r + abs(k) * 18, cy - r, cx + r - abs(k) * 18, cy + r],
              270, 90, fill=(180, 220, 215), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(180, 220, 215), width=1)
    d.arc([cx - r, cy - 26, cx + r, cy + 26], 0, 360, fill=(180, 220, 215), width=1)
    d.text((x0 + 148, y0 + 30), "REGULATE AI", font=font(SANS_B, 20), fill=(255, 214, 90))
    d.text((x0 + 148, y0 + 56), "BEFORE IT'S", font=font(SANS_B, 20), fill=(255, 214, 90))
    d.text((x0 + 148, y0 + 82), "TOO LATE", font=font(SANS_B, 20), fill=(255, 214, 90))
    d.text((x0 + 12, y0 + h - 40), "BRIDGETOWN SUMMIT - BARBADOS",
           font=font(SANS_B, 11), fill=PAPER)
    d.text((x0 + 12, y0 + h - 22), "150 DELEGATES BACK A RISK FRAMEWORK",
           font=font(SANS, 10), fill=(200, 225, 220))
    # small flags row, top-right corner (clear of the summit text below)
    fx = x0 + w - 118
    for col in [(0, 90, 160), (200, 30, 40), (255, 215, 0), (30, 140, 60), (120, 60, 140)]:
        d.rectangle([fx, y0 + 10, fx + 18, y0 + 20], fill=col)
        fx += 22


def hero_scene_power(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=CREAM)
    d.text((x0 + 12, y0 + 10), "ASIA POWER INDEX 2026", font=font(SANS_B, 12), fill=INK)
    d.text((x0 + 12, y0 + 28), "GAP 5.3 - NARROWEST SINCE 2018",
           font=font(SANS, 10), fill=GRAY)
    rows = [("US", 78.9, NAVY, PAPER), ("CHINA", 73.6, (178, 34, 34), PAPER),
            ("INDIA", 40.5, GOLD, INK)]
    y = y0 + 44
    for label, val, col, txt in rows:
        d.text((x0 + 12, y), label, font=font(SANS_B, 12), fill=INK)
        d.text((x0 + 78, y), "%.1f" % val, font=font(SANS_B, 12), fill=INK)
        bar_w = int((w - 24) * val / 100.0)
        d.rectangle([x0 + 12, y + 16, x0 + 12 + bar_w, y + 30], fill=col)
        y += 24
    d.text((x0 + 12, y0 + 128), "US DIPLOMATIC INFLUENCE -6 TO 76.7",
           font=font(SANS, 10), fill=GRAY)


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # top accent
    d.rectangle([0, 0, W, 6], fill=RED)
    # masthead
    d.text((10, 10), "THE WORLD TODAY", font=font(SERIF_B, 52), fill=INK)
    d.text((W - 10 - font(SANS_B, 16).getlength("MONDAY"), 14), "MONDAY",
           font=font(SANS_B, 16), fill=INK)
    dt = "23 NOVEMBER 2026"
    d.text((W - 10 - font(SANS_B, 16).getlength(dt), 34), dt,
           font=font(SANS_B, 16), fill=INK)
    d.text((10, 64), "SUM UP 23 NOVEMBER'S WORLD NEWS IN ONE IMAGE  -  31 STORIES, ONE DAY",
           font=font(SANS_B, 12), fill=GRAY)
    d.line([10, 82, W - 10, 82], fill=INK, width=2)
    # number strip: 2 rows x 5
    nums = [("-3.3%", "KOSPI"), ("5.3", "US-CHINA GAP"),
            ("11,762", "EBOLA CASES DRC"), ("10T WON", "SEOUL FUND"),
            ("2%", "BILLIONAIRE TAX"),
            ("$450M", "SKUBAL DEAL"), ("165", "MISSILES / WEEK"),
            ("12,000", "CLEARED MANCHESTER"), ("264 KG", "LEBANON SEIZURE"),
            ("$107.3B", "ANTHROPIC IPO")]
    cell = (W - 20) / 5.0
    for i, (val, lab) in enumerate(nums):
        row, col = divmod(i, 5)
        cx = 10 + col * cell
        vy = 86 + row * 32
        d.text((cx + 4, vy), val, font=font(SANS_B, 20), fill=RED if row == 0 else INK)
        d.text((cx + 4, vy + 21), lab, font=font(SANS, 9), fill=GRAY)
    # region bar
    d.rectangle([10, 150, W - 10, 168], fill=NAVY)
    reg = "ASIA-PACIFIC 7  -  AMERICAS 8  -  MIDDLE EAST 6  -  EUROPE 5  -  AFRICA 3  -  WORLD 2    |    31 STORIES IN ALL"
    f = font(SANS_B, 12)
    d.text(((W - f.getlength(reg)) / 2, 154), reg, font=f, fill=PAPER)
    # UTC strip
    utc = "THE DAY IN UTC  ~  00:00 KOSPI OPENS  -  05:00 GUTERRES SUMMIT  -  09:00 POWER INDEX  -  13:00 NASDAQ FUTURES  -  18:00 COP31 DAY AFTER  -  TIMES ~ APPROX"
    f = font(SANS, 10)
    d.text(((W - f.getlength(utc)) / 2, 172), utc, font=f, fill=GRAY)
    # heroes
    heroes = [
        ("AI ROUT HITS ASIA: KOSPI -3.3%",
         "Seoul's benchmark sheds 161 points as chip stocks lead a regional sell-off.",
         "REUTERS - 23 NOV", hero_scene_kospi),
        ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief warns in Bridgetown as 150 delegates back a risk framework.",
         "AP - 23 NOV", hero_scene_guterres),
        ("US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026 puts the US at 78.9 and China at 73.6, gap 5.3.",
         "LOWY INSTITUTE - 23 NOV", hero_scene_power),
    ]
    hx = [10, 347, 684]
    hw = [330, 330, 330]
    for (headline, body, src, scene), x0, w in zip(heroes, hx, hw):
        scene(d, x0, 192, w, 146)
        lines = wrap(headline, font(SANS_B, 17), w - 8)
        y = 344
        for ln in lines[:2]:
            d.text((x0 + 2, y), ln, font=font(SANS_B, 17), fill=INK)
            y += 19
        blines = wrap(body, font(SANS, 11), w - 8)
        y = 386
        for ln in blines[:2]:
            d.text((x0 + 2, y), ln, font=font(SANS, 11), fill=GRAY)
            y += 13
        d.text((x0 + 2, 414), src, font=font(SANS, 9), fill=GRAY)
        chip(d, x0 + w - 72, 412, "REPORTED", GREEN)
    d.line([10, 432, W - 10, 432], fill=INK, width=1)
    # 10 cards: 5 cols x 2 rows
    cards = [
        ("BESSENT DEMANDS NVIDIA ANSWERS",
         "Treasury chief presses the chipmaker over China sales.", "REUTERS", "REPORTED"),
        ("FBI PROBES NCIC POLICE-DATABASE HACK",
         "Bureau opens inquiry into a breach of the law-enforcement system.", "AP", "REPORTED"),
        ("TRUMP: IRAN STRIKES MAY RESUME IN NEW YEAR",
         "President says military action is back on the table.", "REUTERS", "REPORTED"),
        ("NASDAQ FUTURES JUMP 3% IN HOLIDAY WEEK",
         "Tech leads a short-week rally into Thanksgiving.", "BLOOMBERG", "REPORTED"),
        ("SKUBAL'S $450M METS DEAL",
         "Two-time Cy Young winner signs a nine-year pact, a pitcher record.", "AP", "REPORTED"),
        ("TOM JACKSON DIES AT 75",
         "Broncos great and broadcaster remembered by the NFL.", "AP", "REPORTED"),
        ("STATES SUE SPACEX OVER AI SAFETY CLAIMS",
         "Attorneys general challenge Grok safety assertions.", "REUTERS", "REPORTED"),
        ("ANTHROPIC IPO: $107.3B AT $83 A SHARE",
         "AI firm debuts at $97.17 after pricing on 19 Nov.", "BLOOMBERG", "REPORTED"),
        ("POLAND: 3 RUSSIAN KH-101 MISSILES CROSSED AIRSPACE",
         "Warsaw says cruise missiles entered its skies.", "AP", "CLAIM"),
        ("INTEL WARNS OF RUSSIAN NUCLEAR SATELLITE",
         "US assessment flags a space-based weapon risk.", "REUTERS", "CLAIM"),
    ]
    cw = 200
    for i, (hl, body, src, tag) in enumerate(cards):
        row, col = divmod(i, 5)
        x0 = 10 + col * 203
        y0 = 438 + row * 90
        d.rectangle([x0, y0, x0 + cw, y0 + 86], outline=LGRAY, width=1)
        hl_lines = wrap(hl, font(SANS_B, 12), cw - 10)
        y = y0 + 5
        for ln in hl_lines[:2]:
            d.text((x0 + 5, y), ln, font=font(SANS_B, 12), fill=INK)
            y += 14
        blines = wrap(body, font(SANS, 10), cw - 10)
        y = y0 + 34
        for ln in blines[:2]:
            d.text((x0 + 5, y), ln, font=font(SANS, 10), fill=GRAY)
            y += 12
        d.text((x0 + 5, y0 + 70), src, font=font(SANS, 8), fill=GRAY)
        chip(d, x0 + cw - 68, y0 + 68, tag, GREEN if tag == "REPORTED" else RED)
    # map + ALSO
    d.text((10, 630), "THE WORLD IN 13 PINS", font=font(SANS_B, 13), fill=INK)
    d.text((364, 630), "ALSO ON MONDAY - 18 MORE", font=font(SANS_B, 13), fill=INK)
    # blobs
    d.ellipse([18, 656, 112, 792], fill=MAPBLUE, outline=MAPLINE)
    d.ellipse([138, 652, 338, 748], fill=MAPBLUE, outline=MAPLINE)
    d.ellipse([150, 744, 240, 802], fill=MAPBLUE, outline=MAPLINE)
    pins = [(320, 690, "1"), (60, 775, "2"), (70, 690, "3"), (295, 680, "4"),
            (92, 682, "5"), (225, 675, "6"), (178, 692, "7"), (165, 680, "8"),
            (258, 712, "9"), (228, 724, "10"), (218, 758, "11"),
            (198, 782, "12"), (172, 786, "13")]
    for px, py, n in pins:
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=PAPER, width=1)
        f = font(SANS_B, 8)
        tw = f.getlength(n)
        d.text((px - tw / 2, py - 5), n, font=f, fill=PAPER)
    legend = ["PINS 1-13: 1 SEOUL - 2 BRIDGETOWN - 3 WASHINGTON",
              "4 BEIJING - 5 NEW YORK - 6 KYIV - 7 PARIS - 8 MANCHESTER",
              "9 BEIRUT - 10 GAZA - 11 BENGHAZI - 12 KHARTOUM - 13 KINSHASA"]
    y = 806
    for ln in legend:
        d.text((10, y), ln, font=font(SANS, 9), fill=GRAY)
        y += 12
    also = [
        "14. Paris: 100+ back 2% billionaire tax",
        "15. Manchester: 12,000 cleared after scare",
        "16. Zelenskyy: 165 Russian missiles in a week",
        "17. COP31: the day after Antalya pact rejected",
        "18. Israel unity talks resume",
        "19. Gaza: two killed in Israeli strike",
        "20. West Bank settler attacks",
        "21. Iran war: no deal in sight",
        "22. Lebanon seizes 264 kg explosives",
        "23. Bahrain Sat: Iranian strike hits plant, 2 hurt",
        "24. Benghazi: UN demands probe of port attacks [CLAIM]",
        "25. Sudan: air defences down drones over Khartoum [CLAIM]",
        "26. DRC: fighting traps Ebola teams",
        "27. Bangladesh: Hasina jailed if she returns",
        "28. Seoul minister quits over AI exam chaos",
        "29. SK Telecom -7.3%",
        "30. China eases margin rules to 80%",
        "31. Seoul readies 10T-won stabilisation fund",
    ]
    # 18 items: 2 cols x 9 rows
    for i, item in enumerate(also):
        col, row = divmod(i, 9)
        ax = 364 + col * 326
        ay = 652 + row * 16
        f = font(SANS, 10)
        lines = wrap(item, f, 318)
        d.text((ax, ay), lines[0], font=f, fill=INK)
        if len(lines) > 1:
            d.text((ax + 14, ay + 11), lines[1], font=f, fill=INK)
    # DATE CHECK box
    d.rectangle([10, 904, W - 10, 982], outline=RED, width=2, fill=(253, 240, 240))
    d.text((20, 910), "DATE CHECK - THESE ARE NOT 23 NOVEMBER",
           font=font(SANS_B, 13), fill=RED)
    d.text((20, 930), "LEFT OUT:", font=font(SANS_B, 11), fill=INK)
    left = ["Democrats reach 258 - 22 Nov", "Sparta II fire - 22 Nov",
            "El Chapo Isidro captured - 22 Nov", "EU-Indonesia pact - 21 Nov",
            "Nigeria boat - 21 Nov", "ICJ Myanmar ruling - 19 Nov"]
    for i, t in enumerate(left):
        col, row = divmod(i, 3)
        d.text((20 + col * 245, 946 + row * 12), "- " + t,
               font=font(SANS, 10), fill=INK)
    d.text((530, 930), "NOT YET:", font=font(SANS_B, 11), fill=INK)
    right = ["Dymer search continues - 14 missing", "4 House races uncalled",
             "COP32 venue not set", "WHO evacuating trapped Ebola staff"]
    for i, t in enumerate(right):
        col, row = divmod(i, 2)
        d.text((530 + col * 240, 946 + row * 12), "- " + t,
               font=font(SANS, 10), fill=INK)
    # footer
    d.text((10, 990), "SOURCES: REUTERS - AP - AFP - BLOOMBERG - YONHAP - 23 NOV 2026",
           font=font(SANS, 9), fill=GRAY)
    d.text((10, 1004), "THE WORLD TODAY - MAKE.FUN NEWS-IMAGE-20261123",
           font=font(SANS, 9), fill=GRAY)
    leg = "REPORTED = CONFIRMED BY WIRES  -  CLAIM = ONE SIDE'S CLAIM"
    f = font(SANS_B, 9)
    d.text((W - 10 - f.getlength(leg), 990), leg, font=f, fill=GRAY)
    img.save(OUT, "PNG")
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    draw()
