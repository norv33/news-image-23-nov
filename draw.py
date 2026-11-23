#!/usr/bin/env python3
"""Draw "The World - 23 November 2026": a morning-broadsheet poster.

One 1024x1024 PNG summing up Monday 23 November 2026 in world news.
Layout: crimson masthead, one full-width lead story, four story cards in
two columns, a slim sixth-story row, an ALSO TODAY strip, and a sources
footer. All art is drawn from PIL primitives; no external images.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
OUT = "entry.png"

# ---- palette: warm morning paper, crimson masthead, ink, gold ----
PAPER = (246, 241, 229)
CARD = (255, 253, 246)
INK = (30, 27, 22)
CRIMSON = (158, 24, 30)
GOLD = (198, 152, 52)
GOLD_LIGHT = (232, 205, 130)
MUTED = (107, 101, 90)
RULE = (216, 205, 180)
BLUE_TAG = (36, 68, 128)
BODY = (58, 52, 44)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SERIF, 118)
F_DATE = font(SANS_B, 34)
F_LEAD_HEAD = font(SERIF, 44)
F_HEAD = font(SERIF, 28)
F_FACT = font(SANS, 20)
F_LEAD_FACT = font(SANS, 22)
F_TAG = font(SANS_B, 18)
F_ALSO_HEAD = font(SANS_B, 21)
F_ALSO = font(SANS, 18)
F_FOOT = font(SANS, 19)
F_FIFTH_HEAD = font(SERIF, 28)
F_FIFTH_FACT = font(SANS, 19)


def wrap(draw, text, fnt, width):
    """Greedy word wrap using real glyph widths."""
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


def draw_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- pictograms
def pic_globe_thermo(d, x, y, s):
    """Globe with a thermometer: COP31 climate talks."""
    cx, cy, r = x + s // 2 - 8, y + s // 2 - 4, s // 2 - 10
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=CRIMSON, width=5)
    d.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r],
              outline=CRIMSON, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=CRIMSON, width=3)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340,
          fill=CRIMSON, width=3)
    tx = x + s - 28
    d.rounded_rectangle([tx, y + 10, tx + 16, y + s - 28], radius=8,
                        outline=CRIMSON, width=4, fill=GOLD_LIGHT)
    d.ellipse([tx - 6, y + s - 40, tx + 22, y + s - 12], fill=CRIMSON)
    d.line([tx + 8, y + 24, tx + 8, y + s - 32], fill=CRIMSON, width=5)


def pic_house_drone(d, x, y, s):
    """House under a drone: Kyiv region strike."""
    hx, hy = x + 6, y + s - 60
    d.polygon([(hx, hy), (hx + 52, hy - 34), (hx + 104, hy)],
              outline=INK, width=5)
    d.rectangle([hx + 8, hy, hx + 96, hy + 56], outline=INK, width=5,
                fill=CARD)
    d.rectangle([hx + 42, hy + 22, hx + 62, hy + 56], fill=INK)
    # small red starburst at the roof corner: the strike
    cx, cy = hx + 92, hy - 30
    pts = []
    for i in range(10):
        ang = i * math.pi / 5
        r = 13 if i % 2 == 0 else 6
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=CRIMSON)
    # drone above
    dx, dy = x + 22, y + 14
    d.ellipse([dx - 11, dy, dx + 11, dy + 11], fill=INK)
    d.line([dx - 30, dy + 2, dx - 11, dy + 4], fill=INK, width=4)
    d.line([dx + 11, dy + 4, dx + 30, dy + 2], fill=INK, width=4)
    d.ellipse([dx - 40, dy - 3, dx - 22, dy + 4], outline=INK, width=3)
    d.ellipse([dx + 22, dy - 3, dx + 40, dy + 4], outline=INK, width=3)
    d.line([dx, dy + 11, dx, dy + 24], fill=INK, width=4)


def pic_factory_flame(d, x, y, s):
    """Factory with flame: Indonesia candy-factory fire."""
    fx, fy = x + 4, y + s - 56
    d.rectangle([fx, fy, fx + 104, fy + 52], outline=INK, width=5,
                fill=CARD)
    d.polygon([(fx, fy), (fx + 26, fy - 22), (fx + 52, fy),
               (fx + 78, fy - 22), (fx + 104, fy)], outline=INK, width=4)
    d.rectangle([fx + 78, fy - 44, fx + 96, fy - 20], outline=INK, width=4,
                fill=GOLD_LIGHT)
    for wx in (fx + 12, fx + 44, fx + 76):
        d.rectangle([wx, fy + 12, wx + 16, fy + 28], outline=INK, width=3)
    cx = x + s // 2
    d.polygon([(cx - 26, y + 34), (cx - 8, y + 6), (cx + 2, y + 22),
               (cx + 14, y + 2), (cx + 26, y + 34)], fill=CRIMSON)
    d.polygon([(cx - 12, y + 34), (cx, y + 18), (cx + 12, y + 34)],
              fill=GOLD)


def pic_ship_blast(d, x, y, s):
    """Ship with an explosion starburst: Libya port blast."""
    sx, sy = x + 4, y + s - 44
    d.polygon([(sx, sy), (sx + 108, sy), (sx + 94, sy + 30),
               (sx + 16, sy + 30)], outline=INK, width=5, fill=CARD)
    d.rectangle([sx + 30, sy - 22, sx + 78, sy], outline=INK, width=4)
    d.line([sx + 54, sy - 40, sx + 54, sy - 22], fill=INK, width=4)
    for i in range(3):
        wx = x + 8 + i * 36
        d.arc([wx, y + s - 12, wx + 28, y + s + 4], 180, 360,
              fill=BLUE_TAG, width=4)
    cx, cy = x + s // 2, y + 22
    pts = []
    for i in range(12):
        ang = i * math.pi / 6
        r = 26 if i % 2 == 0 else 12
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=GOLD, outline=CRIMSON)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=CRIMSON)


def pic_robot(d, x, y, s):
    """Robot head: UN talks on lethal autonomous weapons."""
    rx, ry = x + 22, y + 18
    d.line([rx + 34, ry, rx + 34, ry - 12], fill=INK, width=4)
    d.ellipse([rx + 27, ry - 20, rx + 41, ry - 6], fill=CRIMSON)
    d.rounded_rectangle([rx, ry, rx + 68, ry + 62], radius=12,
                        outline=INK, width=5, fill=CARD)
    d.ellipse([rx + 12, ry + 18, rx + 26, ry + 32], fill=INK)
    d.ellipse([rx + 42, ry + 18, rx + 56, ry + 32], fill=INK)
    d.line([rx + 12, ry + 46, rx + 56, ry + 46], fill=INK, width=4)
    d.rectangle([rx - 10, ry + 22, rx, ry + 40], fill=GOLD)
    d.rectangle([rx + 68, ry + 22, rx + 78, ry + 40], fill=GOLD)
    d.line([x + 30, y + s - 12, x + s - 30, y + s - 12], fill=(31, 92, 84),
           width=4)


def pic_exam_chip(d, x, y, s):
    """Exam paper with an AI chip: Seoul cheating scandal."""
    px, py = x + 4, y + 6
    d.rectangle([px, py, px + 34, py + 48], outline=INK, width=3,
                fill=CARD)
    for ln in (py + 9, py + 18, py + 27):
        d.line([px + 6, ln, px + 28, ln], fill=MUTED, width=2)
    d.line([px + 6, py + 36, px + 20, py + 36], fill=CRIMSON, width=3)
    cx, cy = x + s - 32, y + s - 32
    d.rectangle([cx, cy, cx + 28, cy + 28], outline=INK, width=3,
                fill=GOLD_LIGHT)
    d.rectangle([cx + 8, cy + 8, cx + 20, cy + 20], fill=CRIMSON)
    for i in range(3):
        d.line([cx + 5 + i * 9, cy - 5, cx + 5 + i * 9, cy],
               fill=INK, width=2)
        d.line([cx + 5 + i * 9, cy + 28, cx + 5 + i * 9, cy + 33],
               fill=INK, width=2)


# ---------------------------------------------------------------- stories
LEAD = {
    "tag": "CLIMATE  •  ANTALYA, TURKEY  —  BBC / REUTERS / AP",
    "head": "COP31 collapses with no deal",
    "fact": ("UN climate talks end in failure — the first collapse since "
             "Copenhagen in 2009 — after the EU and others reject a final "
             "text that never mentions fossil fuels."),
    "pic": pic_globe_thermo,
}

CARDS = [
    {
        "tag": "UKRAINE  •  KYIV REGION  —  BBC",
        "head": "Drone hits home; 14 missing",
        "fact": ("A Russian drone flattens a home near Kyiv; a 7-year-old "
                 "boy is pulled alive from the rubble."),
        "pic": pic_house_drone,
    },
    {
        "tag": "INDONESIA  •  BANTEN  —  BBC / REUTERS",
        "head": "Factory fire: 24 body bags",
        "fact": ("Police remove 24 body bags from the burnt candy factory "
                 "as the search for missing workers resumes."),
        "pic": pic_factory_flame,
    },
    {
        "tag": "LIBYA  •  BENGHAZI  —  BBC",
        "head": "Blast on Russian ship in port",
        "fact": ("An explosion rocks a Russian ship at Benghazi; officials "
                 "blame a suspected drone attack."),
        "pic": pic_ship_blast,
    },
    {
        "tag": "UNITED NATIONS  •  GENEVA  —  AP / AFP",
        "head": "Killer-robot talks go on — no ban",
        "fact": ("States agree to keep talking on lethal autonomous "
                 "weapons — but promise no binding ban."),
        "pic": pic_robot,
    },
]

EXTRA = {
    "tag": "SOUTH KOREA  •  SEOUL  —  AFP / AP",
    "head": "Minister quits in AI exam scandal",
    "fact": "Seoul's education minister quits over an AI exam-cheating scandal.",
    "pic": pic_exam_chip,
}

ALSO = ("WASHINGTON: Democrats take a 258-seat House majority"
        "  •  NEW DELHI: Nepal PM meets Modi"
        "  •  WELLINGTON: India post record 720/9")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # faint paper rules, like newsprint columns
    for yy in range(8, H, 46):
        d.line([(0, yy), (W, yy)], fill=(238, 231, 214), width=1)

    # ---- masthead ----
    d.rectangle([0, 0, W, 148], fill=CRIMSON)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    title = "THE WORLD"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 6), title, font=F_TITLE, fill=(250, 244, 230))
    d.text((36, 108), "MONDAY, 23 NOVEMBER 2026", font=F_DATE,
           fill=GOLD_LIGHT)
    d.text((W - 36 - d.textlength("ONE DAY  •  SIX STORIES", font=F_DATE),
            108), "ONE DAY  •  SIX STORIES", font=F_DATE, fill=(250, 244, 230))

    # ---- lead story: full-width panel, 170-366 ----
    lx, ly, lw, lh = 36, 170, W - 72, 196
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD, outline=RULE, width=2)
    d.rectangle([lx, ly, lx + 10, ly + lh], fill=GOLD)
    d.text((lx + 28, ly + 12), LEAD["tag"], font=F_TAG, fill=CRIMSON)
    head_lines = wrap(d, LEAD["head"], F_LEAD_HEAD, lw - 250)
    draw_block(d, (lx + 28, ly + 40), head_lines, F_LEAD_HEAD, INK, 50)
    fact_lines = wrap(d, LEAD["fact"], F_LEAD_FACT, lw - 250)
    draw_block(d, (lx + 28, ly + 40 + len(head_lines) * 50 + 6),
               fact_lines, F_LEAD_FACT, BODY, 29)
    LEAD["pic"](d, lx + lw - 168, ly + 24, 140)

    # ---- four story cards: 2 columns x 2 rows, 382-806 ----
    cw, ch, gap = 466, 212, 20
    for i, c in enumerate(CARDS):
        col, row = i % 2, i // 2
        x = 36 + col * (cw + gap)
        y = 382 + row * (ch + 12)
        d.rectangle([x, y, x + cw, y + ch], fill=CARD, outline=RULE, width=2)
        d.rectangle([x, y, x + cw, y + 5], fill=CRIMSON if col == 0
                    else BLUE_TAG)
        d.text((x + 18, y + 16), c["tag"], font=F_TAG, fill=CRIMSON)
        head_lines = wrap(d, c["head"], F_HEAD, cw - 150)
        end = draw_block(d, (x + 18, y + 44), head_lines, F_HEAD, INK, 33)
        fact_lines = wrap(d, c["fact"], F_FACT, cw - 150)
        draw_block(d, (x + 18, end + 4), fact_lines, F_FACT, BODY, 25)
        c["pic"](d, x + cw - 128, y + 56, 112)

    # ---- sixth story: slim full-width row, 822-906 ----
    ex, ey, ew, eh = 36, 822, W - 72, 84
    d.rectangle([ex, ey, ex + ew, ey + eh], fill=(233, 224, 200),
                outline=RULE, width=2)
    d.text((ex + 18, ey + 8), EXTRA["tag"], font=F_TAG, fill=CRIMSON)
    d.text((ex + 18, ey + 32), EXTRA["head"], font=F_FIFTH_HEAD, fill=INK)
    d.text((ex + 18, ey + 62), EXTRA["fact"], font=F_FIFTH_FACT, fill=BODY)
    EXTRA["pic"](d, ex + ew - 96, ey + 8, 68)

    # ---- also today strip, 922-978 ----
    ax, ay, aw, ah = 36, 922, W - 72, 56
    d.rectangle([ax, ay, ax + aw, ay + ah], fill=INK)
    d.text((ax + 16, ay + 17), "ALSO TODAY", font=F_ALSO_HEAD,
           fill=GOLD_LIGHT)
    ax0 = ax + 16 + d.textlength("ALSO TODAY", font=F_ALSO_HEAD) + 18
    items = wrap(d, ALSO, F_ALSO, aw - (ax0 - ax) - 16)
    draw_block(d, (ax0, ay + 6), items[:2], F_ALSO,
               (250, 244, 230), 22)

    # ---- footer ----
    d.text((36, 990), "Sources: BBC News • Reuters • AP • AFP — drawn for "
           "make.fun news-image-20261123", font=F_FOOT, fill=MUTED)
    d.text((W - 36 - d.textlength("23 NOV 2026", font=F_FOOT), 990),
           "23 NOV 2026", font=F_FOOT, fill=MUTED)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {img.size}")


if __name__ == "__main__":
    main()
