#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-01 (build-time only, NOT shipped logic).

Layout (1024x1024, newspaper front page):
  header masthead + big date
  lead panel: NVIDIA (image left, text right)
  2x2 grid: Microsoft / Ukraine / Gulf / Taiwan
  bottom strip: COP31 climate
All text is drawn with PIL + DejaVu Sans (sharp, exact spelling).
Panel photos are AI-generated illustrations (no text in them).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (178, 34, 34)
NAVY = (16, 42, 67)
GREEN = (18, 77, 56)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, fnt, max_w, max_lines):
    """Shrink font until text fits max_w x max_lines."""
    size = fnt.size
    while size > 12:
        f = font(fnt.path, size)
        if len(wrap(draw, text, f, max_w)) <= max_lines:
            return f
        size -= 1
    return font(fnt.path, 12)


def crop_cover(img, tw, th):
    iw, ih = img.size
    s = max(tw / iw, th / ih)
    img = img.resize((round(iw * s), round(ih * s)), Image.LANCZOS)
    x = (img.width - tw) // 2
    y = (img.height - th) // 2
    return img.crop((x, y, x + tw, y + th))


def load(name):
    p = sorted(ASSETS.glob(name))
    assert p, f"missing asset {name}"
    return Image.open(p[0]).convert("RGB")


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 24  # margin

# ---------- header ----------
d.text((M, 26), "THE WORLD IN ONE DAY", font=font(FB, 26), fill=INK)
d.text((W - M - d.textlength("FRIDAY", font=font(FB, 26)), 26),
       "FRIDAY", font=font(FB, 26), fill=RED)
d.text((M, 58), "13 NOVEMBER 2026", font=font(FB, 66), fill=NAVY)
d.text((M, 130), "Six stories from around the globe — in one picture",
       font=font(FR, 22), fill=GREY)
d.rectangle([M, 158, W - M, 164], fill=RED)

# ---------- lead: NVIDIA ----------
ly, lh = 176, 196
lead_img = crop_cover(load("media-generation-panel-nvidia-*.webp"), 500, lh)
img.paste(lead_img, (M, ly))
d.rectangle([M, ly, M + 500, ly + lh], outline=INK, width=2)
tx = M + 516
d.text((tx, ly + 2), "TECH  •  LEAD STORY", font=font(FB, 19), fill=RED)
d.text((tx, ly + 30), "NVIDIA CHIEF", font=font(FB, 46), fill=INK)
d.text((tx, ly + 80), "QUITS", font=font(FB, 46), fill=INK)
sub = "Jensen Huang resigns after 33 years. CFO Colette Kress is interim CEO."
y = ly + 140
for line in wrap(d, sub, font(FR, 22), W - M - tx):
    d.text((tx, y), line, font=font(FR, 22), fill=(40, 40, 40))
    y += 28

# ---------- 2x2 grid ----------
panels = [
    ("media-generation-panel-microsoft-*.webp", "TECH  •  OUTAGE",
     "MICROSOFT 365 DOWN",
     "Outlook, Teams and Copilot hit for a second day. Microsoft: not a cyberattack."),
    ("media-generation-panel-ukraine-*.webp", "DIPLOMACY",
     "EUROPE JOINS UKRAINE TALKS",
     "UK, France, Germany, Italy and Poland named for the next round. Kremlin yet to confirm."),
    ("media-generation-panel-gulf-*.webp", "MIDDLE EAST",
     "GULF ON EDGE",
     "Iran claims a strike on a US radar in Bahrain. US says it downed two drones; no damage."),
    ("media-generation-panel-taiwan-*.webp", "ASIA",
     "CHINA DRILLS OFF TAIWAN",
     "Taipei says Beijing staged large unannounced Pacific drills with 100+ vessels."),
]
cw, gap = 488, 16
ch_img, ch_txt = 128, 134
gy = 384
for i, (pat, kicker, head, sub) in enumerate(panels):
    col, row = i % 2, i // 2
    x0 = M + col * (cw + gap)
    y0 = gy + row * (ch_img + ch_txt + 10)
    pic = crop_cover(load(pat), cw, ch_img)
    img.paste(pic, (x0, y0))
    d.rectangle([x0, y0, x0 + cw, y0 + ch_img], outline=INK, width=2)
    ty = y0 + ch_img + 8
    d.text((x0, ty), kicker, font=font(FB, 17), fill=RED)
    hf = fit_text(d, head, font(FB, 28), cw, 2)
    hy = ty + 24
    for line in wrap(d, head, hf, cw):
        d.text((x0, hy), line, font=hf, fill=INK)
        hy += hf.size + 4
    sf = font(FR, 19)
    sy = hy + 2
    for line in wrap(d, sub, sf, cw)[:2]:
        d.text((x0, sy), line, font=sf, fill=(40, 40, 40))
        sy += 24

# ---------- bottom strip: COP31 ----------
sy0 = 940
d.rectangle([M, sy0, W - M, 1000], fill=GREEN)
d.text((M + 14, sy0 + 8), "CLIMATE  •  COP31, ANTALYA",
       font=font(FB, 18), fill=(255, 214, 120))
strip = "UN chief: 1.5°C overshoot “now inevitable” — drastic cuts urged at COP31."
sz = 24
while d.textlength(strip, font=font(FB, sz)) > W - 2 * M - 28 and sz > 14:
    sz -= 1
d.text((M + 14, sy0 + 32), strip, font=font(FB, sz), fill=WHITE)

img.save(HERE / "entry.png", optimize=True)
print("saved", HERE / "entry.png", img.size)
