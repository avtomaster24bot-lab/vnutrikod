# -*- coding: utf-8 -*-
"""PDF-подарки: HTML → PDF через headless Chrome. Запуск: python3 _src/pdfs.py"""
import os, subprocess, math, tempfile
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = "file://" + OUT + "/assets/fonts/"
CSS = """@font-face{font-family:U;src:url(%(f)sunbounded-cyrillic.woff2)}@font-face{font-family:M;src:url(%(f)smanrope-cyrillic.woff2)}
@page{size:A4;margin:16mm}body{font:12pt/1.5 M,sans-serif;color:#1b1640}h1{font:700 24pt/1.15 U,sans-serif;margin:0 0 6mm;color:#3a1f8f}
.k{font:800 9pt M;letter-spacing:.15em;text-transform:uppercase;color:#c2389a}.box{border:1.5px solid #9b7bff;border-radius:10px;padding:5mm 6mm;margin:5mm 0}
ul.c{list-style:none;padding:0}ul.c li{padding:2.2mm 0 2.2mm 9mm;position:relative;border-bottom:1px solid #e6e1fb}ul.c li:before{content:"";position:absolute;left:0;top:3mm;width:4.5mm;height:4.5mm;border:1.5px solid #3a1f8f;border-radius:3px}
.line{border-bottom:1px solid #b9b0e6;height:9mm}table{width:100%%;border-collapse:collapse}td,th{border:1px solid #c8bff0;padding:2.5mm;vertical-align:top;font-size:10.5pt}th{background:#f1edff;text-align:left}td{height:14mm}
.f{margin-top:8mm;font-size:9pt;color:#6a6390;border-top:1px solid #ddd;padding-top:3mm}""" % {"f": FONTS}
FOOT = '<div class="f">Внутрикод · Марина Степанова · avtomaster24bot-lab.github.io/vnutrikod · Telegram: @MarinaNew. Материал для самонаблюдения, не диагностика и не замена помощи специалиста.</div>'
def page(title, kicker, body): return '<!doctype html><html lang="ru"><meta charset="utf-8"><style>%s</style><body><div class="k">%s</div><h1>%s</h1>%s%s</body></html>' % (CSS, kicker, title, body, FOOT)
P1 = page("Тащу всё на себе", "Чек-лист · Внутрикод", """<p>Отметьте пункты, которые узнаёте в себе за последний месяц.</p><ul class="c">""" + "".join("<li>%s</li>" % x for x in [
 "Мне проще сделать самой, чем объяснять другому.", "Я перепроверяю чужую работу, даже когда это не нужно.", "Я чувствую вину, если кто-то рядом расстроен.",
 "Мне трудно просить о помощи.", "Я беру задачи, о которых меня не просили.", "Отдых без плана вызывает тревогу.", "Я думаю: «если отпущу — всё развалится».",
 "Окружающие привыкли, что я всё решу.", "Я решаю проблемы взрослых людей за них.", "Мои собственные цели откладываются «на потом».",
 "Я раздражаюсь, что никто ничего не делает, но продолжаю делать сама.", "Я устаю от того, что всегда за всё отвечаю."]) + """</ul>
<div class="box"><b>Практика «Инвентаризация чужого»</b><p>Выпишите 5 дел, которые вы сейчас тянете. Рядом с каждым ответьте: <i>чья это зона ответственности на самом деле?</i> Выберите одно дело и в ближайшие 7 дней верните его владельцу — спокойно и без объяснений «почему так».</p>
<table><tr><th style="width:45%">Дело, которое я тяну</th><th>Чьё оно на самом деле</th><th>Что я сделаю</th></tr>""" + "<tr><td></td><td></td><td></td></tr>"*5 + "</table></div><p>Отмечено 6 и больше? Посмотрите статью «Гиперответственность» и тест «Уровень гиперконтроля» на сайте.</p>")
P2 = page("Мои денежные установки", "Рабочий лист · Внутрикод", """<p>Денежные установки часто звучат голосами семьи. Вспомните фразы, которые вы слышали в детстве, и посмотрите, как они влияют на вас сейчас.</p>
<table><tr><th>Фраза из детства о деньгах</th><th>Как она проявляется сейчас (цены, траты, доход)</th><th>Взрослая версия, которую я выбираю</th></tr>""" + "<tr><td style='height:24mm'></td><td></td><td></td></tr>"*5 + """</table>
<div class="box"><b>Пример</b><p>«Деньги достаются тяжёлым трудом» → беру только «тяжёлые» проекты, стесняюсь лёгких денег → «Деньги приходят за ценность, которую я создаю, — не только за усталость».</p></div>
<div class="box"><b>Вопрос для размышления</b><p>Какая сумма в месяц кажется мне «уже слишком»? Что я чувствую в теле, когда представляю её?</p><div class="line"></div><div class="line"></div></div>""")
cx, cy, R = 250, 250, 200
sp = ["Деньги и доход", "Свобода от страхов", "Опора и границы", "Проявленность и цена", "Ритм и энергия", "Мечта и цели"]
svg = ['<svg viewBox="0 0 500 500" width="150mm" height="150mm" style="display:block;margin:4mm auto">']
for k in range(1, 11): svg.append('<circle cx="%d" cy="%d" r="%.1f" fill="none" stroke="%s" stroke-width="%s"/>' % (cx, cy, R*k/10, "#9b7bff" if k == 10 else "#ddd6ff", 1.5 if k == 10 else .8))
for i, s in enumerate(sp):
    a = -math.pi/2 + i*2*math.pi/6
    svg.append('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="#9b7bff"/>' % (cx, cy, cx + R*math.cos(a), cy + R*math.sin(a)))
    for k in (5, 10): svg.append('<text x="%.1f" y="%.1f" font-size="9" fill="#888">%d</text>' % (cx + R*k/10*math.cos(a) + 3, cy + R*k/10*math.sin(a) - 3, k))
    tx, ty = cx + (R + 28)*math.cos(a), cy + (R + 22)*math.sin(a)
    svg.append('<text x="%.1f" y="%.1f" font-size="12" font-family="M" text-anchor="middle" fill="#3a1f8f" font-weight="700">%s</text>' % (tx, ty, s))
svg.append("</svg>")
P3 = page("Колесо баланса", "Для печати · Внутрикод", "<p>Оцените каждую сферу от 1 до 10 (10 — у края круга), поставьте точки на спицах и соедините их. Самая короткая спица — ваша точка роста.</p>" + "".join(svg) +
          '<div class="box"><b>Моя точка роста:</b><div class="line"></div><b>Один шаг на эту неделю:</b><div class="line"></div><b>Дата:</b> ____________ · Повторите через месяц и сравните.</div>')
os.makedirs(OUT + "/assets/pdf", exist_ok=True)
for name, html in [("tashu-vsyo-na-sebe.pdf", P1), ("denezhnye-ustanovki.pdf", P2), ("koleso-balansa.pdf", P3)]:
    tmp = os.path.join(tempfile.gettempdir(), name + ".html"); open(tmp, "w", encoding="utf-8").write(html)
    subprocess.run(["/usr/bin/google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files", "--print-to-pdf=" + OUT + "/assets/pdf/" + name, "file://" + tmp], check=True, capture_output=True, timeout=90)
    print(name, os.path.getsize(OUT + "/assets/pdf/" + name))
