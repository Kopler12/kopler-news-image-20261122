"""Draw the front page for Sunday, 22 November 2026.

Newspaper-style 1024x1024 image, drawn with Pillow. Run:
    python3 draw.py
Writes entry.png next to this file.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 24, 38)
RED = (178, 34, 28)
NAVY = (24, 52, 96)
TEAL = (18, 92, 96)
GOLD = (198, 142, 28)
SEA = (46, 98, 140)
SKY = (214, 230, 240)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, width=width) or [""])
    out = []
    for line in lines:
        while draw.textlength(line, font=fnt) > width and " " in line:
            cut = line.rfind(" ", 0, len(line) // 2 + 8)
            if cut <= 0:
                break
            out.append(line[:cut])
            line = line[cut + 1:]
        out.append(line)
    return out


def center(draw, x0, x1, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def panel(draw, x, y, w, h, kicker, headline, body, art):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 30], fill=NAVY)
    center(draw, x, x + w, y + 5, kicker, font(SANS_B, 17), fill=(255, 255, 255))
    art(x + 8, y + 38, w - 16, 78)
    yy = y + 124
    for line in wrap(draw, headline, font(SANS_B, 22), w - 20):
        draw.text((x + 10, yy), line, font=font(SANS_B, 22), fill=INK)
        yy += 26
    yy += 4
    for line in wrap(draw, body, font(SANS, 18), w - 20):
        draw.text((x + 10, yy), line, font=font(SANS, 18), fill=(52, 58, 70))
        yy += 21


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)

    # ---- masthead (auto-fit so nothing is clipped) ----
    msize = 88
    while (d.textlength("THE WORLD TODAY", font=font(SERIF_B, msize))
           > W - 60 and msize > 40):
        msize -= 2
    center(d, 0, W, 22, "THE WORLD TODAY", font(SERIF_B, msize), fill=INK)
    d.line([40, 128, W - 40, 128], fill=INK, width=3)
    center(d, 0, W, 138, "SUNDAY, 22 NOVEMBER 2026", font(SANS_B, 40), fill=RED)
    d.line([40, 196, W - 40, 196], fill=INK, width=3)

    # ---- lead story: Gulf escalation ----
    ly, lh = 210, 258
    d.rectangle([24, ly, W - 24, ly + lh], outline=INK, width=2)
    d.rectangle([24, ly, W - 24, ly + 44], fill=RED)
    center(d, 24, W - 24, ly + 8, "LEAD  •  THE GULF", font(SANS_B, 22),
           fill=(255, 255, 255))
    center(d, 24, W - 24, ly + 54, "GULF IN FLAMES",
           font(SERIF_B, 58), fill=INK)
    center(d, 24, W - 24, ly + 122,
           "Iran strikes a US base in Kuwait, targets Bahrain;",
           font(SANS, 25), fill=(40, 46, 60))
    center(d, 24, W - 24, ly + 152,
           "tankers hit off Oman; ADNOC ship attacked in Hormuz —",
           font(SANS, 25), fill=(40, 46, 60))
    center(d, 24, W - 24, ly + 182,
           "one crew member missing.",
           font(SANS_B, 25), fill=INK)
    # sea scene strip at the bottom of the lead panel
    sx, sy, sw, sh = 40, ly + 214, W - 80, 36
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=SEA)
    for tx in (sx + 60, sx + 300, sx + 560):
        d.rectangle([tx, sy + 12, tx + 130, sy + 26], fill=(30, 30, 34))
        d.rectangle([tx + 40, sy + 2, tx + 52, sy + 12], fill=(30, 30, 34))
    for ex, ey, r in ((sx + 130, sy + 4, 12), (sx + 430, sy + 6, 10),
                      (sx + 700, sy + 2, 13)):
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(255, 140, 40))
        d.ellipse([ex - r // 2, ey - r // 2, ex + r // 2, ey + r // 2],
                  fill=(255, 220, 90))

    # ---- story grid: 4 + 3 panels ----
    gx, gy = 24, 484
    pw, ph, gap = 236, 246, 8
    stories = [
        ("PERU", "QUAKE ROCKS\nTHE ANDES",
         "Magnitude 6.9\nNo casualties\nreported yet.", "quake"),
        ("BALTIC SEA", "DRONES HIT\nRUSSIAN SHIP",
         "Finland tightens\nsecurity; Estonia\nto shut border.", "baltic"),
        ("MEXICO", "'EL CHAPO\nISIDRO' HELD",
         "Cartel boss\ncaptured; 11 killed\nin Sinaloa.", "mexico"),
        ("SUMMIT", "TRUMP LANDS\nIN SHENZHEN",
         "APEC: Xi, Putin\ntalks planned;\nZelensky hits back.", "summit"),
        ("CLIMATE", "COP31\nDEADLOCK",
         "Antalya talks stall\nover fossil fuels.", "climate"),
        ("UKRAINE", "400 DRONES,\n110 MISSILES",
         "Russia's huge air\nassault; debris\nfalls in Poland.", "ukraine"),
        ("BRAZIL", "BOLSONARO\nIN ICU",
         "Ex-president\nadmitted with acute\nbowel obstruction.", "brazil"),
    ]

    def art_quake(x, y, w, h):
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        d.polygon([(x, y + h), (x + w * 0.3, y + 12), (x + w * 0.55, y + h)],
                  fill=(110, 96, 78))
        d.polygon([(x + w * 0.4, y + h), (x + w * 0.7, y + 4),
                   (x + w, y + h)], fill=(88, 76, 62))
        d.polygon([(x + w * 0.62, y + 22), (x + w * 0.7, y + 4),
                   (x + w * 0.78, y + 22)], fill=(255, 255, 255))
        d.line([x + 8, y + 30, x + w - 8, y + 52], fill=RED, width=4)
        d.line([x + 20, y + 52, x + 40, y + 38], fill=RED, width=3)

    def art_baltic(x, y, w, h):
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        d.rectangle([x, y + h - 26, x + w, y + h], fill=SEA)
        d.polygon([(x + 30, y + h - 26), (x + 90, y + h - 26),
                   (x + 70, y + 40), (x + 50, y + 40)], fill=(60, 60, 66))
        d.rectangle([x + 52, y + 26, x + 68, y + 40], fill=(60, 60, 66))
        d.ellipse([x + w - 52, y + 8, x + w - 28, y + 32], fill=RED)
        d.ellipse([x + w - 46, y + 14, x + w - 34, y + 26], fill=(255, 220, 90))
        d.rectangle([x + w - 90, y + 30, x + w - 70, y + 38], fill=INK)
        d.line([x + w - 80, y + 38, x + w - 80, y + 46], fill=INK, width=2)

    def art_mexico(x, y, w, h):
        d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
        d.rounded_rectangle([x + w // 2 - 58, y + 14, x + w // 2 + 58, y + 58],
                            radius=10, outline=NAVY, width=4)
        t = "POLICE"
        tw = d.textlength(t, font=font(SANS_B, 22))
        d.text((x + w // 2 - tw / 2, y + 24), t, font=font(SANS_B, 22),
               fill=NAVY)
        d.ellipse([x + 52, y + 66, x + 92, y + h - 6], outline=INK, width=5)
        d.ellipse([x + w - 92, y + 66, x + w - 52, y + h - 6], outline=INK,
                  width=5)
        d.line([x + 92, y + 78, x + w - 92, y + 78], fill=INK, width=4)

    def art_summit(x, y, w, h):
        d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
        d.rectangle([x + 18, y + 58, x + w - 18, y + 66], fill=(120, 84, 40))
        d.line([x + 30, y + 58, x + 30, y + 14], fill=INK, width=3)
        d.line([x + w // 2, y + 58, x + w // 2, y + 14], fill=INK, width=3)
        d.line([x + w - 30, y + 58, x + w - 30, y + 14], fill=INK, width=3)
        d.polygon([(x + 30, y + 14), (x + 62, y + 24), (x + 30, y + 34)],
                  fill=RED)
        d.polygon([(x + w // 2, y + 14), (x + w // 2 + 32, y + 24),
                   (x + w // 2, y + 34)], fill=RED)
        d.polygon([(x + w - 30, y + 14), (x + w - 62, y + 24),
                   (x + w - 30, y + 34)], fill=NAVY)
        d.ellipse([x + 52, y + 70, x + 78, y + h - 4], fill=GOLD)
        d.ellipse([x + w // 2 - 13, y + 70, x + w // 2 + 13, y + h - 4],
                  fill=NAVY)
        d.ellipse([x + w - 78, y + 70, x + w - 52, y + h - 4], fill=RED)

    def art_climate(x, y, w, h):
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        d.ellipse([x + w // 2 - 42, y + 6, x + w // 2 + 42, y + 90],
                  fill=(70, 140, 90))
        d.ellipse([x + w // 2 - 30, y + 14, x + w // 2 + 6, y + 40],
                  fill=(120, 190, 130))
        d.ellipse([x + w // 2 - 8, y + 48, x + w // 2 + 30, y + 76],
                  fill=(120, 190, 130))
        for cx in (x + 26, x + w - 46):
            d.ellipse([cx, y + 62, cx + 22, y + 84], fill=(120, 120, 120))
            d.ellipse([cx + 6, y + 50, cx + 28, y + 72], fill=(150, 150, 150))

    def art_ukraine(x, y, w, h):
        d.rectangle([x, y, x + w, y + h], fill=(30, 38, 58))
        for dx, dy in ((x + 24, y + 16), (x + 90, y + 34), (x + 160, y + 12),
                       (x + 60, y + 58), (x + 130, y + 66)):
            d.ellipse([dx, dy, dx + 7, dy + 7], fill=(255, 220, 90))
        d.ellipse([x + w - 58, y + 52, x + w - 18, y + 92], fill=(255, 140, 40))
        d.ellipse([x + w - 48, y + 62, x + w - 28, y + 82], fill=(255, 220, 90))
        d.polygon([(x + 10, y + h), (x + 60, y + h - 22), (x + 110, y + h)],
                  fill=(70, 70, 78))

    def art_brazil(x, y, w, h):
        d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        d.rectangle([x + w // 2 - 34, y + 8, x + w // 2 + 34, y + 84],
                    fill=RED)
        d.rectangle([x + w // 2 - 10, y + 8, x + w // 2 + 10, y + 84],
                    fill=(255, 255, 255))
        d.rectangle([x + w // 2 - 34, y + 38, x + w // 2 + 34, y + 54],
                    fill=(255, 255, 255))

    arts = {"quake": art_quake, "baltic": art_baltic, "mexico": art_mexico,
            "summit": art_summit, "climate": art_climate,
            "ukraine": art_ukraine, "brazil": art_brazil}

    for i, (kicker, headline, body, key) in enumerate(stories):
        row, col = divmod(i, 4)
        x = gx + col * (pw + gap)
        y = gy + row * (ph + gap)
        panel(d, x, y, pw, ph, kicker, headline, body, arts[key])

    # ---- last cell: the day in one line ----
    x = gx + 3 * (pw + gap)
    y = gy + 1 * (ph + gap)
    d.rectangle([x, y, x + pw, y + ph], outline=INK, width=2)
    d.rectangle([x, y, x + pw, y + 30], fill=TEAL)
    center(d, x, x + pw, y + 5, "THE DAY", font(SANS_B, 17),
           fill=(255, 255, 255))
    yy = y + 48
    for line in ["Eight stories,",
                 "one Sunday —",
                 "from the Gulf",
                 "to the Andes,",
                 "the Baltic",
                 "to Brazil."]:
        center(d, x, x + pw, yy, line, font(SERIF_B, 24), fill=INK)
        yy += 30

    # ---- footer ----
    center(d, 0, W, 992,
           "All stories as reported on 22 November 2026",
           font(SANS, 19), fill=(90, 88, 80))

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
