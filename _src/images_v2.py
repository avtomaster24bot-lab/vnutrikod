# -*- coding: utf-8 -*-
"""Иллюстрации v2: PNG от Agnes (agnes-image-2.1-flash) → assets/img/v2/<key>.webp (1200 px, <150 КБ) + <key>-480.webp.
Запуск: python3 _src/images_v2.py <папка_с_png> [ключи...]. Если PNG нет — абстракция в стиле бренда (Pillow).
Абстрактные метафорические образы, без текста и без лиц реальных людей."""
import os, sys, json, math, random, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
from data import T, MINIS, MODULES
from art import ARTICLES, CATS
from tests_data import TESTS
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img", "v2")
SEC = {"znaniya": "энциклопедия", "ceny": "лестница форматов", "podarki": "бесплатные подарки", "testy": "тесты-самонаблюдения", "karta-dnya": "карта дня",
       "mini-lila": "Мини-Лила", "dyhanie": "дыхание 4–6", "7-dnej": "челлендж «7 дней»", "chek-listy": "чек-листы", "moj-put": "мой путь", "marina": "ведущая и наставник",
       "faq": "частые вопросы", "navigator": "навигатор", "slushat": "аудио-объяснения", "otzyvy": "отзывы", "podpiska": "ИИ-навигатор", "vazhno": "поддержка и безопасность"}
def labels():
    L = {}
    for m in MODULES: L["modul-%d" % m["n"]] = "модуль «%s»" % m["title"]
    for s, t in T.items(): L["trening-" + s] = "тренинг «%s»" % t["title"]
    for m in MINIS: L["mini-" + m["slug"]] = "мини-тренинг «%s»" % m["title"]
    for k, v in CATS: L["cat-" + k] = "рубрика «%s»" % v
    for t in TESTS: L["test-" + t["slug"]] = "тест «%s»" % t["title"]
    for k, v in SEC.items(): L["sec-" + k] = v
    L.update({"koleso-uspeha": "программа «Колесо успеха»", "lila": "игра «Лила»", "klub": "закрытый клуб", "individualno": "индивидуальная сессия", "diagnostika": "личная диагностика",
              "psihologam": "психологам и коучам", "marafon-dvizhenie-k-celi": "марафон «Движение к цели»", "marafon-samoprinyatie": "марафон «Самопринятие»"})
    return L
def fallback(key, w=1312, h=738):
    rnd = random.Random(key); im = Image.new("RGB", (w, h), (7, 6, 26)); d = ImageDraw.Draw(im, "RGBA")
    cols = [(124, 247, 255), (155, 123, 255), (255, 107, 214)]
    for _ in range(260): x, y = rnd.random() * w, rnd.random() * h; r = rnd.random() * 1.6; d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, rnd.randint(60, 200)))
    pts = [(rnd.uniform(.15, .85) * w, rnd.uniform(.15, .85) * h) for _ in range(14)]
    for i, a in enumerate(pts):
        for b in pts[i + 1:]:
            if math.dist(a, b) < w * .28: d.line([a, b], fill=cols[i % 3] + (90,), width=2)
    glow = Image.new("RGBA", (w, h)); g = ImageDraw.Draw(glow)
    for i, (x, y) in enumerate(pts): r = rnd.uniform(8, 26); g.ellipse([x - r, y - r, x + r, y + r], fill=cols[i % 3] + (200,))
    cx, cy = w * rnd.uniform(.35, .65), h * .5
    for k in range(6): R = 60 + k * 55; g.ellipse([cx - R, cy - R, cx + R, cy + R], outline=cols[k % 3] + (120,), width=3)
    glow = glow.filter(ImageFilter.GaussianBlur(6)); im.paste(glow, (0, 0), glow)
    return im
def save(im, key):
    os.makedirs(OUT, exist_ok=True)
    im = im.convert("RGB")
    big = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
    if abs(big.height - 675) > 2:  # кадрируем к 16:9
        t = max(0, (big.height - 675) // 2); big = big.crop((0, t, 1200, t + 675)) if big.height > 675 else big.resize((1200, 675))
    for q in (80, 74, 68, 60, 52, 45):
        b = io.BytesIO(); big.save(b, "WEBP", quality=q, method=6)
        if b.tell() < 150_000: break
    open(os.path.join(OUT, key + ".webp"), "wb").write(b.getvalue())
    sm = big.resize((480, 270), Image.LANCZOS); sm.save(os.path.join(OUT, key + "-480.webp"), "WEBP", quality=72, method=6)
    return b.tell()
if __name__ == "__main__":
    src = sys.argv[1]; L = labels(); keys = sys.argv[2:] or list(L)
    meta, rep = {}, {"agnes": 0, "fallback": 0}
    for k in keys:
        fp = os.path.join(src, k + ".png")
        if os.path.exists(fp): im = Image.open(fp); rep["agnes"] += 1
        else: im = fallback(k); rep["fallback"] += 1; print("fallback", k)
        n = save(im, k); meta[k] = "Абстрактная иллюстрация: " + L.get(k, k)
        print(k, n // 1024, "KB")
    af = os.path.join(OUT, "alt.json"); old = json.load(open(af, encoding="utf-8")) if os.path.exists(af) else {}
    old.update(meta); json.dump(old, open(af, "w", encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)
    print(rep)
