#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up
Tuesday 24 November 2026 in six verified stories.

Pure Pillow primitives, no photos, no network, no external assets.
Deterministic: the same input always renders the same bytes.
Run:  python3 draw.py   (writes entry.png beside this file)
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28

PAPER = (248, 244, 233)
INK = (25, 25, 25)
MUTED = (90, 86, 76)
NAVY = (22, 35, 63)
NAVY_LIGHT = (38, 56, 96)
GOLD = (198, 154, 60)
RED = (178, 34, 24)
CARD = (255, 253, 245)
CARD_LINE = (205, 198, 178)
TINT = (238, 232, 214)
GREEN = (30, 122, 52)
BLUE = (36, 84, 138)
ORANGE = (214, 96, 20)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- pictograms
def pic_chart(d, x, y, s):
    """Rising bars and an arrow: the market rally."""
    d.rectangle([x, y, x + s, y + s], fill=(232, 244, 232), outline=CARD_LINE)
    bx, by = x + s * 0.16, y + s * 0.78
    bw = s * 0.16
    heights = (0.22, 0.38, 0.55)
    for i, h in enumerate(heights):
        d.rectangle([bx + i * s * 0.24, by - s * h, bx + i * s * 0.24 + bw,
                     by], fill=GREEN)
    d.line([(x + s * 0.14, y + s * 0.62), (x + s * 0.42, y + s * 0.42),
            (x + s * 0.62, y + s * 0.50), (x + s * 0.86, y + s * 0.18)],
           fill=INK, width=5)
    d.polygon([(x + s * 0.86, y + s * 0.18), (x + s * 0.70, y + s * 0.16),
               (x + s * 0.84, y + s * 0.32)], fill=INK)


def pic_ship(d, x, y, s):
    """A warship on waves."""
    d.rectangle([x, y, x + s, y + s], fill=(226, 236, 246), outline=CARD_LINE)
    d.polygon([(x + s * 0.12, y + s * 0.52), (x + s * 0.88, y + s * 0.52),
               (x + s * 0.76, y + s * 0.70), (x + s * 0.24, y + s * 0.70)],
              fill=NAVY)
    d.rectangle([x + s * 0.30, y + s * 0.34, x + s * 0.62, y + s * 0.52],
                fill=NAVY_LIGHT)
    d.rectangle([x + s * 0.46, y + s * 0.18, x + s * 0.50, y + s * 0.34],
                fill=INK)
    d.polygon([(x + s * 0.50, y + s * 0.18), (x + s * 0.66, y + s * 0.24),
               (x + s * 0.50, y + s * 0.28)], fill=RED)
    for i, wy in enumerate((0.78, 0.86)):
        d.arc([x + s * 0.10 + i * s * 0.08, y + s * wy, x + s * 0.42 + i * s * 0.08,
               y + s * wy + s * 0.10], 0, 180, fill=BLUE, width=3)
        d.arc([x + s * 0.52 + i * s * 0.06, y + s * wy, x + s * 0.84 + i * s * 0.06,
               y + s * wy + s * 0.10], 0, 180, fill=BLUE, width=3)


def pic_globe(d, x, y, s):
    """A globe with a rising sun: the climate talks."""
    d.rectangle([x, y, x + s, y + s], fill=(232, 240, 232), outline=CARD_LINE)
    cx, cy, r = x + s * 0.50, y + s * 0.56, s * 0.32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GREEN, width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=GREEN,
              width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=GREEN, width=3)
    d.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], 0, 180, fill=GREEN,
          width=3)
    d.ellipse([cx - s * 0.30, cy - s * 0.22, cx - s * 0.12, cy - s * 0.04],
              fill=GREEN)
    d.ellipse([cx + s * 0.06, cy + s * 0.02, cx + s * 0.24, cy + s * 0.18],
              fill=GREEN)
    sx, sy = x + s * 0.72, y + s * 0.20
    d.ellipse([sx - s * 0.07, sy - s * 0.07, sx + s * 0.07, sy + s * 0.07],
              fill=ORANGE)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-0.7, -0.7), (0.7, -0.7)):
        d.line([(sx + dx * s * 0.10, sy + dy * s * 0.10),
                (sx + dx * s * 0.16, sy + dy * s * 0.16)], fill=ORANGE, width=3)


def pic_tanker(d, x, y, s):
    """An oil tanker at sea: the Hormuz blockade."""
    d.rectangle([x, y, x + s, y + s], fill=(240, 234, 222), outline=CARD_LINE)
    d.rectangle([x + s * 0.14, y + s * 0.46, x + s * 0.86, y + s * 0.66],
                fill=INK)
    d.rectangle([x + s * 0.66, y + s * 0.30, x + s * 0.84, y + s * 0.46],
                fill=NAVY_LIGHT)
    for i in range(3):
        d.rectangle([x + s * (0.18 + i * 0.16), y + s * 0.34,
                     x + s * (0.30 + i * 0.16), y + s * 0.46],
                    outline=RED, width=3)
    d.line([(x + s * 0.10, y + s * 0.74), (x + s * 0.90, y + s * 0.74)],
           fill=BLUE, width=3)
    d.line([(x + s * 0.16, y + s * 0.82), (x + s * 0.84, y + s * 0.82)],
           fill=BLUE, width=3)
    d.line([(x + s * 0.10, y + s * 0.20), (x + s * 0.90, y + s * 0.20)],
           fill=RED, width=4)
    d.line([(x + s * 0.10, y + s * 0.20), (x + s * 0.10, y + s * 0.28)],
           fill=RED, width=4)
    d.line([(x + s * 0.90, y + s * 0.20), (x + s * 0.90, y + s * 0.28)],
           fill=RED, width=4)


def pic_chess(d, x, y, s):
    """A chessboard with a king: the world championship."""
    d.rectangle([x, y, x + s, y + s], fill=(238, 236, 228), outline=CARD_LINE)
    bx, by, bs = x + s * 0.14, y + s * 0.30, s * 0.56
    cell = bs / 4
    for r in range(4):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([bx + c * cell, by + r * cell,
                             bx + (c + 1) * cell, by + (r + 1) * cell],
                            fill=INK)
    kx, ky = x + s * 0.62, y + s * 0.16
    d.polygon([(kx, ky), (kx + s * 0.06, ky + s * 0.10),
               (kx + s * 0.12, ky), (kx + s * 0.12, ky + s * 0.12),
               (kx, ky + s * 0.12)], fill=GOLD, outline=INK)
    d.ellipse([kx - s * 0.01, ky - s * 0.05, kx + s * 0.05, ky + s * 0.01],
              fill=GOLD, outline=INK)
    d.ellipse([kx + s * 0.07, ky - s * 0.05, kx + s * 0.13, ky + s * 0.01],
              fill=GOLD, outline=INK)
    d.rectangle([kx - s * 0.02, ky + s * 0.16, kx + s * 0.14, ky + s * 0.22],
                fill=GOLD, outline=INK)


def pic_fire(d, x, y, s):
    """A factory with a flame: the Banten fire."""
    d.rectangle([x, y, x + s, y + s], fill=(246, 232, 226), outline=CARD_LINE)
    d.rectangle([x + s * 0.16, y + s * 0.48, x + s * 0.72, y + s * 0.78],
                fill=NAVY_LIGHT)
    d.polygon([(x + s * 0.16, y + s * 0.48), (x + s * 0.30, y + s * 0.36),
               (x + s * 0.44, y + s * 0.48), (x + s * 0.58, y + s * 0.36),
               (x + s * 0.72, y + s * 0.48)], fill=NAVY)
    d.rectangle([x + s * 0.76, y + s * 0.30, x + s * 0.86, y + s * 0.78],
                fill=INK)
    d.polygon([(x + s * 0.80, y + s * 0.14), (x + s * 0.92, y + s * 0.30),
               (x + s * 0.86, y + s * 0.30), (x + s * 0.78, y + s * 0.34),
               (x + s * 0.72, y + s * 0.26)], fill=ORANGE)
    d.polygon([(x + s * 0.84, y + s * 0.22), (x + s * 0.90, y + s * 0.30),
               (x + s * 0.82, y + s * 0.32)], fill=RED)


# ------------------------------------------------------------------- stories
# Every fact below was checked against at least two independent sources
# (Reuters, CNN, AP, WSJ, Chess.com) on 24 November 2026.
STORIES = [
    dict(tag="MARKETS  ·  TECHNOLOGY", pic=pic_chart, lead=True,
         headline="Huang is back — Nvidia soars 31%",
         summary=("Nvidia reinstates co-founder Jensen Huang as chief "
                  "executive, 11 days after he resigned. Shares jump 31% "
                  "— a $952bn gain — lifting the Nasdaq 6.5%.")),
    dict(tag="CONFLICT  ·  UKRAINE", pic=pic_ship, grid=True,
         headline="Ukraine sinks Russian warship off Libya",
         summary=("Seven sea drones strike the corvette Merkury at Benghazi. "
                  "A helicopter on board is destroyed and the cargo ship "
                  "MV Angara is hit.")),
    dict(tag="CLIMATE  ·  COP31", pic=pic_globe, grid=True,
         headline="Climate summit collapses with no deal",
         summary=("COP31 in Antalya ends after two weeks with no agreement, "
                  "as the EU rejects a draft that omits fossil fuels — the "
                  "longest climate talks on record.")),
    dict(tag="MIDDLE EAST  ·  ENERGY", pic=pic_tanker, grid=True,
         headline="Iran vows to fight US blockade",
         summary=("Tehran says it will use “every means” against the US "
                  "naval blockade, after Trump warns ships that try to "
                  "break it will be sunk.")),
    dict(tag="SPORT  ·  CHESS", pic=pic_chess, grid=True,
         headline="Chess crown on the line in Geneva",
         summary=("Game 1 of the World Championship begins today. Defending "
                  "champion Gukesh, 20, faces challenger Sindarov, 20 — "
                  "the youngest title match ever.")),
    dict(tag="DISASTER  ·  INDONESIA", pic=pic_fire, lead=False, wide=True,
         headline="24 dead in factory fire; 30 still missing",
         summary=("Rescuers keep searching the burned candy factory in Banten, "
                  "Java, after the weekend blaze. The cause is under "
                  "investigation.")),
]


def draw_card(d, box, story):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=CARD, outline=CARD_LINE, width=2)
    pad = 18
    tag_f = font(SANS_BOLD, 17)
    if story.get("grid"):
        # Pictogram tucked in the top-right corner; headline and summary
        # run the full card width underneath, so nothing is clipped.
        pic_s = 88
        story["pic"](d, x1 - pad - pic_s, y0 + 14, pic_s)
        head_f = font(SANS_BOLD, 24)
        sum_f = font(SANS, 18)
        tx = x0 + pad
        ty = y0 + 14
        d.text((tx, ty), story["tag"], font=tag_f, fill=RED)
        ty += 28
        head_w = (x1 - pad - pic_s - 12) - tx
        head_lines = wrap(d, story["headline"], head_f, head_w)
        ty = text_block(d, tx, ty, head_lines, head_f, INK, 29)
        ty += 7
        sum_lines = wrap(d, story["summary"], sum_f, (x1 - pad) - tx)
        text_block(d, tx, ty, sum_lines, sum_f, MUTED, 23)
        return
    head_f = font(SANS_BOLD, 27 if not story.get("lead") else 36)
    sum_f = font(SANS, 19 if not story.get("lead") else 21)
    pic_s = 118 if not story.get("lead") else 150
    pic_x = x1 - pad - pic_s
    pic_y = y0 + (y1 - y0 - pic_s) // 2
    text_w = pic_x - 14 - (x0 + pad)
    tx = x0 + pad
    ty = y0 + pad
    d.text((tx, ty), story["tag"], font=tag_f, fill=RED)
    ty += 30
    head_lines = wrap(d, story["headline"], head_f, text_w)
    lead_h = 44 if story.get("lead") else 33
    ty = text_block(d, tx, ty, head_lines, head_f, INK, lead_h)
    ty += 8
    sum_lines = wrap(d, story["summary"], sum_f, text_w)
    text_block(d, tx, ty, sum_lines, sum_f, MUTED, 25 if not story.get("lead") else 27)
    story["pic"](d, pic_x, pic_y, pic_s)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead ------------------------------------------------------------
    mx0, my0, mx1, my1 = MARGIN, MARGIN, W - MARGIN, 168
    d.rounded_rectangle([mx0, my0, mx1, my1], radius=10, fill=NAVY)
    kicker = font(SANS_BOLD, 19)
    sub_f = font(SANS, 20)
    d.text((mx0 + 30, my0 + 16), "THE WORLD IN ONE PAGE",
           font=kicker, fill=GOLD)
    # Shrink the date until it fits the masthead with room to spare.
    date_size = 54
    date_f = font(SERIF_BOLD, date_size)
    while d.textlength("TUESDAY 24 NOVEMBER 2026", font=date_f) > (mx1 - mx0 - 60):
        date_size -= 1
        date_f = font(SERIF_BOLD, date_size)
    d.text((mx0 + 30, my0 + 44), "TUESDAY 24 NOVEMBER 2026",
           font=date_f, fill=(255, 255, 255))
    d.line([(mx0 + 30, my1 - 38), (mx1 - 30, my1 - 38)], fill=GOLD, width=2)
    d.text((mx0 + 30, my1 - 32),
           "The day's six biggest stories — from Wall Street to Geneva",
           font=sub_f, fill=(210, 216, 232))

    # Lead story, full width ---------------------------------------------
    draw_card(d, (MARGIN, 182, W - MARGIN, 382), STORIES[0])

    # Two rows of two ------------------------------------------------------
    gap = 12
    col_w = (W - 2 * MARGIN - gap) // 2
    rows = [(396, 606), (618, 828)]
    idx = 1
    for (ry0, ry1) in rows:
        for c in range(2):
            cx0 = MARGIN + c * (col_w + gap)
            draw_card(d, (cx0, ry0, cx0 + col_w, ry1), STORIES[idx])
            idx += 1

    # Final story, full width ---------------------------------------------
    draw_card(d, (MARGIN, 842, W - MARGIN, 984), STORIES[5])

    # Footer ---------------------------------------------------------------
    foot_f = font(SANS, 15)
    d.text((MARGIN, 992),
           "Figures as reported by Reuters, CNN, AP, WSJ and Chess.com · 24 November 2026",
           font=foot_f, fill=MUTED)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
