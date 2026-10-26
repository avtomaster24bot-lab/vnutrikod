# -*- coding: utf-8 -*-
"""OG-картинки, иконки. Запуск: python3 _src/images.py (после gen.py не обязателен — независим)."""
import os, sys, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import ARTICLES, CATS
import articles1, articles2, articles3, articles4  # noqa
from tests_data import TESTS
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = "/usr/share/fonts/truetype/sand-box/google/"
def font(fam, size, wght):
    f = ImageFont.truetype(G + "%s/%s-VariableFont_wght.ttf" % (fam, fam), size)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f
CAT = dict(CATS)
def bg(W, H, seed):
    rnd = random.Random(seed)
    im = Image.new("RGB", (W, H), (7, 6, 26))
    glow = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(glow)
    for col, (cx, cy, r) in zip([(124, 247, 255), (155, 123, 255), (255, 107, 214)], [(W*.85, H*.15, 380), (W*.65, H*.8, 420), (W*.98, H*.6, 300)]):
        cx += rnd.randint(-80, 80); cy += rnd.randint(-60, 60)
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=tuple(int(c*.55) for c in col))
    glow = glow.filter(ImageFilter.GaussianBlur(140)); im = Image.blend(im, glow, .85)
    d = ImageDraw.Draw(im); pts = [(rnd.random()*W, rnd.random()*H) for _ in range(70)]
    for i, p in enumerate(pts):
        for q in pts[i+1:]:
            if math.dist(p, q) < 130: d.line([p, q], fill=(120, 110, 200), width=1)
        r = rnd.random()*2.2 + .8; d.ellipse([p[0]-r, p[1]-r, p[0]+r, p[1]+r], fill=(220, 230, 255))
    return im
def logo(d, x, y, s):
    d.ellipse([x, y, x+s, y+s], outline=(124, 247, 255), width=max(2, s//14))
    k = s/40; pts = [(8, 20), (14, 20), (17, 13), (23, 27), (26, 20), (32, 20)]
    d.line([(x+a*k, y+b*k) for a, b in pts], fill=(255, 107, 214), width=max(2, s//14), joint="curve")
def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines
def card(path, kicker, title, sub, seed):
    W, H = 1200, 630; im = bg(W, H, seed); d = ImageDraw.Draw(im)
    logo(d, 70, 60, 54); d.text((140, 66), "Внутрикод", font=font("Unbounded", 34, 700), fill=(255, 255, 255))
    d.text((70, 170), kicker.upper(), font=font("Manrope", 26, 800), fill=(124, 247, 255))
    size = 64
    while True:
        f = font("Unbounded", size, 700); ls = wrap(d, title, f, W-160)
        if len(ls) <= 3 or size <= 40: break
        size -= 4
    y = 215
    for l in ls[:3]: d.text((70, y), l, font=f, fill=(255, 255, 255)); y += int(size*1.22)
    fs = font("Manrope", 28, 500)
    for l in wrap(d, sub, fs, W-160)[:2]: d.text((70, y+18), l, font=fs, fill=(205, 198, 240)); y += 38
    d.text((70, H-70), "Марина Степанова · психолог · живые онлайн-сессии", font=font("Manrope", 24, 600), fill=(180, 172, 214))
    os.makedirs(os.path.dirname(path), exist_ok=True); im.save(path, optimize=True)
A = os.path.join(OUT, "assets")
card(A + "/og.png", "Психология нового поколения", "Расшифруйте свой внутренний код", "Энциклопедия, бесплатные тесты, Мини-Лила и живые сессии с Мариной Степановой.", 1)
for s, a in ARTICLES.items(): card(A + "/og/%s.png" % s, "Энциклопедия · " + CAT[a["cat"]], a["title"], a["desc"], s)
for t in TESTS: card(A + "/og/test-%s.png" % t["slug"], "Бесплатный тест", t["title"], t["desc"], t["slug"])
# apple-touch-icon
im = Image.new("RGB", (180, 180), (7, 6, 26)); g = Image.new("RGB", (180, 180)); ImageDraw.Draw(g).ellipse([20, 20, 160, 160], fill=(80, 50, 160)); g = g.filter(ImageFilter.GaussianBlur(30))
im = Image.blend(im, g, .8); logo(ImageDraw.Draw(im), 30, 30, 120); im.save(A + "/apple-touch-icon.png")
open(A + "/favicon.svg", "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7cf7ff"/><stop offset=".5" stop-color="#9b7bff"/><stop offset="1" stop-color="#ff6bd6"/></linearGradient></defs><rect width="40" height="40" rx="10" fill="#07061a"/><circle cx="20" cy="20" r="15" fill="none" stroke="url(#g)" stroke-width="2.8"/><path d="M8 20h6l3-7 6 14 3-7h6" fill="none" stroke="url(#g)" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')
print("ok", len(os.listdir(A + "/og")))
