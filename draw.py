"""Draw the front page: one 1024x1024 image summing up the world news of
Monday 23 November 2026. Pure Pillow, no network, deterministic output.
Run: python3 draw.py  ->  writes entry.png next to this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 33, 61)
NAVY = (20, 33, 61)
RED = (185, 28, 28)
TEAL = (13, 116, 128)
AMBER = (180, 83, 9)
GREEN = (21, 101, 52)
SLATE = (71, 85, 105)
LINE = (20, 33, 61)
TINTS = [(232, 238, 245), (252, 231, 231), (254, 243, 226), (231, 245, 233),
         (238, 232, 245), (252, 244, 214)]

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, max_w, fill, leading=1.25):
    """Draw wrapped paragraph; return y just below the last line."""
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def kicker(draw, xy, text, fnt, color):
    draw.text(xy, text, font=fnt, fill=color)


def icon_globe(d, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = (x1 - x0) // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=color, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340, fill=color, width=3)
    d.line([cx - r + 6, cy + r - 6, cx + r - 6, cy - r + 6], fill=RED, width=6)


def icon_tanker(d, box, color):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # hull
    d.polygon([(x0 + 6, y0 + h * 0.45), (x0 + w - 6, y0 + h * 0.45),
               (x0 + w - 18, y0 + h * 0.75), (x0 + 18, y0 + h * 0.75)],
              fill=color)
    # containers
    d.rectangle([x0 + w * 0.2, y0 + h * 0.18, x0 + w * 0.42, y0 + h * 0.45],
                fill=color)
    d.rectangle([x0 + w * 0.48, y0 + h * 0.18, x0 + w * 0.70, y0 + h * 0.45],
                fill=color)
    # funnel
    d.rectangle([x0 + w * 0.74, y0 + h * 0.22, x0 + w * 0.86, y0 + h * 0.45],
                fill=RED)
    # waves
    for yy in (y0 + h * 0.84, y0 + h * 0.94):
        for k in range(3):
            xx = x0 + 8 + k * (w // 3)
            d.arc([xx, yy - 6, xx + w // 3 - 12, yy + 6], 180, 360,
                  fill=color, width=3)


def icon_quake(d, box, color):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    pts = [(x0 + 4, y0 + h * 0.55), (x0 + w * 0.25, y0 + h * 0.55),
           (x0 + w * 0.35, y0 + h * 0.25), (x0 + w * 0.45, y0 + h * 0.75),
           (x0 + w * 0.55, y0 + h * 0.30), (x0 + w * 0.65, y0 + h * 0.55),
           (x0 + w - 4, y0 + h * 0.55)]
    d.line(pts, fill=color, width=5, joint="curve")
    # cracked ground
    d.line([x0 + w * 0.15, y0 + h * 0.88, x0 + w * 0.4, y0 + h * 0.78],
           fill=color, width=4)
    d.line([x0 + w * 0.4, y0 + h * 0.78, x0 + w * 0.55, y0 + h * 0.88],
           fill=color, width=4)
    d.line([x0 + w * 0.62, y0 + h * 0.88, x0 + w * 0.85, y0 + h * 0.80],
           fill=color, width=4)


def icon_flame(d, box, color):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    w, h = x1 - x0, y1 - y0
    # outer flame: teardrop built from a pieslice + triangle
    d.pieslice([cx - w * 0.32, y0 + h * 0.28, cx + w * 0.32, y0 + h * 0.92],
               0, 180, fill=color)
    d.polygon([(cx - w * 0.32, y0 + h * 0.60), (cx, y0 + h * 0.05),
               (cx + w * 0.32, y0 + h * 0.60)], fill=color)
    # inner flame, paper coloured
    d.pieslice([cx - w * 0.15, y0 + h * 0.55, cx + w * 0.15, y0 + h * 0.92],
               0, 180, fill=PAPER)
    d.polygon([(cx - w * 0.15, y0 + h * 0.72), (cx, y0 + h * 0.45),
               (cx + w * 0.15, y0 + h * 0.72)], fill=PAPER)


def icon_burst(d, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = (x1 - x0) // 2 - 6
    # building
    d.rectangle([x0 + 8, y0 + (y1 - y0) * 0.45, x0 + (x1 - x0) * 0.55,
                 y1 - 8], fill=color)
    for row in range(3):
        for col in range(2):
            bx = x0 + 16 + col * 18
            by = y0 + (y1 - y0) * 0.52 + row * 16
            d.rectangle([bx, by, bx + 8, by + 8], fill=PAPER)
    # starburst above the roof
    import math
    bx, by = x0 + (x1 - x0) * 0.62, y0 + (y1 - y0) * 0.30
    for k in range(8):
        ang = math.pi * k / 4
        d.line([bx, by, bx + int(math.cos(ang) * r * 0.62),
                by + int(math.sin(ang) * r * 0.62)], fill=RED, width=5)
    d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED)


def icon_flags(d, box, color):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cols = [RED, NAVY, TEAL]
    for i, c in enumerate(cols):
        px = x0 + 10 + i * (w // 3)
        d.line([px, y0 + 6, px, y1 - 6], fill=INK, width=4)
        d.rectangle([px, y0 + 8, px + w // 3 - 14, y0 + h * 0.42], fill=c)
    # table line
    d.line([x0 + 6, y1 - 6, x1 - 6, y1 - 6], fill=color, width=4)


ICONS = {
    "globe": icon_globe,
    "tanker": icon_tanker,
    "quake": icon_quake,
    "flame": icon_flame,
    "burst": icon_burst,
    "flags": icon_flags,
}


def story_panel(d, box, tag, headline, body, icon, tint, accent,
                head_size=32, body_size=21):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=(255, 255, 255),
                        outline=LINE, width=2)
    # icon disc, top-left
    ix0, iy0, ix1, iy1 = x0 + 16, y0 + 16, x0 + 96, y0 + 96
    d.ellipse([ix0, iy0, ix1, iy1], fill=tint)
    ICONS[icon](d, [ix0 + 8, iy0 + 8, ix1 - 8, iy1 - 8], accent)
    tx = x0 + 112
    tw = x1 - tx - 16
    kicker(d, (tx, y0 + 18), tag, font(SANS_B, 19), accent)
    y = y0 + 44
    y = para(d, (tx, y), headline, font(SERIF_B, head_size), tw, INK, 1.08)
    y += 4
    para(d, (tx, y), body, font(SANS, body_size), tw, SLATE, 1.3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=RED)
    kicker(d, (32, 22), "THE WORLD IN ONE PICTURE", font(SANS_B, 26), (255, 255, 255))
    d.text((W - 32, 26), "SIX STORIES  •  ONE DAY", font=font(SANS_B, 22),
           fill=(255, 214, 130), anchor="ra")
    d.text((32, 56), "MONDAY 23 NOVEMBER 2026", font=font(SERIF_B, 52),
           fill=(255, 255, 255))

    # ---- lead story: COP31 ----
    x0, y0, x1, y1 = 24, 174, 1000, 372
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=(255, 255, 255),
                        outline=LINE, width=2)
    ix0, iy0, ix1, iy1 = x0 + 20, y0 + 20, x0 + 170, y0 + 170
    d.ellipse([ix0, iy0, ix1, iy1], fill=TINTS[0])
    icon_globe(d, [ix0 + 12, iy0 + 12, ix1 - 12, iy1 - 12], TEAL)
    tx = x0 + 196
    kicker(d, (tx, y0 + 22), "CLIMATE  •  ANTALYA, TURKEY", font(SANS_B, 21), RED)
    y = para(d, (tx, y0 + 52), "COP31 ENDS WITH NO DEAL",
             font(SERIF_B, 44), x1 - tx - 20, INK, 1.05)
    para(d, (tx, y + 8),
         "Climate talks close with no pact as the UN chief warns there is "
         "\u201cno ambiguity in the science\u201d.",
         font(SANS, 22), x1 - tx - 20, SLATE, 1.3)

    # ---- four-story grid ----
    grid = [
        ("GULF  •  STRAIT OF HORMUZ", "TANKERS STRUCK IN HORMUZ",
         "At least two oil tankers are hit by projectiles as Iran\u2013US "
         "tensions flare.", "tanker", TINTS[1], RED),
        ("EARTHQUAKE  •  PERU", "MAGNITUDE 6.7 QUAKE HITS PERU",
         "A powerful earthquake strikes the Andes region of central Peru.",
         "quake", TINTS[2], AMBER),
        ("DISASTER  •  JAVA, INDONESIA", "FACTORY FIRE IN JAVA",
         "Three dead and dozens missing after a blaze tears through a candy "
         "factory in Banten.", "flame", TINTS[3], RED),
        ("WAR  •  UKRAINE", "DRONE HITS KYIV REGION",
         "At least 14 people are missing after a Russian drone strikes a "
         "building, Zelenskyy says.", "burst", TINTS[4], NAVY),
    ]
    gw, gh, gx, gy = 478, 218, 24, 392
    for i, (tag, head, body, icon, tint, accent) in enumerate(grid):
        cx = gx + (i % 2) * (gw + 20)
        cy = gy + (i // 2) * (gh + 16)
        story_panel(d, (cx, cy, cx + gw, cy + gh), tag, head, body, icon,
                    tint, accent)

    # ---- bottom story: great powers ----
    x0, y0, x1, y1 = 24, 860, 1000, 962
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=(255, 255, 255),
                        outline=LINE, width=2)
    ix0, iy0, ix1, iy1 = x0 + 16, y0 + 14, x0 + 96, y0 + 88
    d.ellipse([ix0, iy0, ix1, iy1], fill=TINTS[5])
    icon_flags(d, [ix0 + 8, iy0 + 8, ix1 - 8, iy1 - 8], NAVY)
    tx = x0 + 112
    kicker(d, (tx, y0 + 14), "GREAT POWERS  •  WASHINGTON", font(SANS_B, 19), TEAL)
    para(d, (tx, y0 + 40), "TRUMP: CHINA'S NUCLEAR ARSENAL GROWING",
         font(SERIF_B, 28), x1 - tx - 16, INK, 1.05)
    para(d, (tx, y0 + 76),
         "Warning comes a day after his meeting with Xi Jinping and "
         "Vladimir Putin.", font(SANS, 20), x1 - tx - 16, SLATE, 1.25)

    # ---- footer ticker ----
    d.rectangle([0, 982, W, H], fill=NAVY)
    d.text((32, 998),
           "ALSO TODAY:  Modi meets Nepal's PM  •  "
           "EU proposes a Big Tech tax  •  Hong Kong polls return 723",
           font=font(SANS_B, 17), fill=(255, 255, 255))

    img.save("entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
