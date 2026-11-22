# -*- coding: utf-8 -*-
"""Обложка подкаста 1400×1400: python3 _src/podcast_cover.py"""
import os, random, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = "/usr/share/fonts/truetype/sand-box/google/"
def font(fam, size, w):
    f = ImageFont.truetype(G + "%s/%s-VariableFont_wght.ttf" % (fam, fam), size)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
S = 1400; rnd = random.Random(7)
im = Image.new("RGB", (S, S), (7, 6, 26)); g = Image.new("RGB", (S, S)); d = ImageDraw.Draw(g)
for col, (cx, cy, r) in zip([(124, 247, 255), (155, 123, 255), (255, 107, 214)], [(1150, 250, 420), (300, 1150, 480), (1200, 1200, 360)]):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=tuple(int(c * .55) for c in col))
im = Image.blend(im, g.filter(ImageFilter.GaussianBlur(170)), .85); d = ImageDraw.Draw(im)
pts = [(rnd.random() * S, rnd.random() * S) for _ in range(90)]
for i, p in enumerate(pts):
    for q in pts[i + 1:]:
        if math.dist(p, q) < 150: d.line([p, q], fill=(110, 100, 190), width=1)
    r = rnd.random() * 2.5 + 1; d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=(220, 230, 255))
# логотип-волна
x, y, s = 120, 130, 170
d.ellipse([x, y, x + s, y + s], outline=(124, 247, 255), width=12)
k = s / 40; d.line([(x + a * k, y + b * k) for a, b in [(8, 20), (14, 20), (17, 13), (23, 27), (26, 20), (32, 20)]], fill=(255, 107, 214), width=12, joint="curve")
d.text((120, 470), "ВНУТРИКОД", font=font("Unbounded", 150, 800), fill=(255, 255, 255))
d.text((126, 690), "послушать", font=font("Unbounded", 96, 600), fill=(124, 247, 255))
d.text((126, 810), "объяснение", font=font("Unbounded", 96, 600), fill=(124, 247, 255))
d.text((126, 1170), "Психология простым языком", font=font("Manrope", 58, 700), fill=(230, 225, 255))
d.text((126, 1250), "Марина Степанова · живые онлайн-встречи", font=font("Manrope", 46, 600), fill=(185, 175, 220))
im.save(os.path.join(OUT, "assets/podcast-cover.png"), optimize=True); print("ok")
