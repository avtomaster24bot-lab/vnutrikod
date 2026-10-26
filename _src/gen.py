# -*- coding: utf-8 -*-
"""Генератор сайта «Внутрикод». Запуск: python3 _src/gen.py"""
import os, re, json, sys
from html import escape as e
from urllib.parse import quote as _q
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import MODULES, T, MINIS, TOPICS
from reviews import R
from art import ARTICLES, CATS
import articles1, articles2, articles3, articles4  # noqa: регистрируют статьи
from tests_data import TESTS, SCALE
from extra import LILA_CELLS, LILA_JUMPS, CARD_PROMPTS, CARD_WORDS, CHALLENGE, NAV_THEMES

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://avtomaster24bot-lab.github.io/vnutrikod/"
BASE = "/vnutrikod/"
BRAND = "Внутрикод"
V = "8"
TG = "https://t.me/MarinaNew"
PAGES = []
MOD = {m["n"]: m for m in MODULES}
MINI = {m["slug"]: m for m in MINIS}
TESTD = {t["slug"]: t for t in TESTS}
CAT = dict(CATS)

# ---- цены из config.js (для HTML без JS; источник истины — config.js) ----
_cfg = open(os.path.join(OUT, "assets/config.js"), encoding="utf-8").read()
_pb = re.search(r"prices:\s*\{(.*?)\}", _cfg, re.S).group(1)
PRICES = dict(re.findall(r'"([^"]+)":\s*"([^"]*)"', _pb))
def pr(code, group=""): return PRICES.get(code) or PRICES.get(group) or "Цена уточняется"

# ---------------------------------------------------------------- продукты
TAIL = "Подскажите, как оплатить и ближайшую дату."
HI = "Здравствуйте, Марина! "
PROD = {}
def P(key, title, url, code, group, head, tail=TAIL, kicker="", short="", noprice=False):
    PROD[key] = dict(t=title, u=url, code=code, g=group, head=HI + head, tail=tail, k=kicker, s=short, np=noprice)

for m in MINIS:
    P("mini:" + m["slug"], "Мини-тренинг «%s»" % m["title"], "mini/%s/" % m["slug"], "mini-" + m["slug"], "mini",
      "Хочу купить мини-тренинг «%s» (1–1,5 часа, онлайн)." % m["title"], kicker="Мини-тренинг · 1–1,5 ч", short=m["hook"])
for s, t in T.items():
    mod = (" (модуль «%s»)" % MOD[t["module"]]["title"]) if t["module"] else ""
    P("trening:" + s, "Тренинг «%s»" % t["title"], "trening/%s/" % s, "trening-" + s, "training" if s != "samotsennost" else "",
      "Хочу купить тренинг «%s»%s." % (t["title"], mod), kicker="Трансформационный тренинг · 2–3 ч", short=t["short"])
for m in MODULES:
    P("modul:%d" % m["n"], "Модуль %d «%s»" % (m["n"], m["title"]), "modul/%s/" % m["slug"], "modul-%d" % m["n"], "module",
      "Хочу купить модуль %d «%s» программы «Колесо успеха» (1 месяц, 4 тренинга)." % (m["n"], m["title"]), kicker="Модуль · 1 месяц · 4 тренинга", short=m["intro"][:150].rsplit(" ", 1)[0] + "…")
P("koleso", "Программа «Колесо успеха»", "koleso-uspeha/", "koleso-full", "", "Хочу купить программу «Колесо успеха» — вариант: полная программа (6 месяцев, 24 тренинга).", kicker="Флагман · 6 месяцев", short="6 модулей, 24 живых тренинга: от денег и страхов до проявленности и масштаба.")
P("koleso-part1", "«Колесо успеха» — Часть 1 «Внутренняя опора»", "koleso-uspeha/", "koleso-part1", "", "Хочу купить программу «Колесо успеха» — вариант: Часть 1 «Внутренняя опора» (модули 1–3, 3 месяца).", kicker="3 месяца · модули 1–3", short="Деньги, страхи, выход из замкнутого круга. 12 тренингов.")
P("koleso-part2", "«Колесо успеха» — Часть 2 «Проявленность и масштаб»", "koleso-uspeha/", "koleso-part2", "", "Хочу купить программу «Колесо успеха» — вариант: Часть 2 «Проявленность и масштаб» (модули 4–6, 3 месяца).", kicker="3 месяца · модули 4–6", short="Продукт и цена, ритм без стресса, от мечты к цели. 12 тренингов.")
P("lila", "Игра «Лила» с Мариной", "lila/", "igra-lila", "", "Хочу записаться на игру «Лила» (4 часа, онлайн).", kicker="Т-игра · 4 часа · до 4 игроков", short="Авторская версия для бизнеса и жизненных ситуаций.")
P("klub", "Закрытый клуб", "klub/", "club", "", "Хочу в закрытый клуб (подписка): медитации по понедельникам и групповые «Разборы».", "Пришлите, пожалуйста, детали подписки.", kicker="Подписка · Telegram · предзапись", short="Медитации по понедельникам, групповые «Разборы», карта недели.")
P("diag", "Личная диагностика 30 минут", "diagnostika/", "diagnostika", "", "Хочу записаться на полную индивидуальную диагностику по запросу (30 минут, 1 на 1).", "Подскажите, пожалуйста, ближайшее время и как оплатить.", kicker="1 на 1 · 30 минут", short="Понять, что стоит за вашей ситуацией и какой шаг нужен дальше. Засчитывается в покупку.")
P("individ", "Индивидуальная сессия", "individualno/", "individ-sessiya", "", "Хочу купить индивидуальную сессию (1–2 часа, онлайн).", "Подскажите, пожалуйста, ближайшее свободное время и как оплатить.", kicker="1 на 1 · 1–2 часа", short="Разбор системы мышления как архитектуры и её перенастройка.")
P("individ3", "Пакет из 3 сессий", "individualno/", "individ-paket3", "", "Хочу купить пакет из 3 индивидуальных сессий.", "Подскажите, пожалуйста, ближайшее время и как оплатить.", kicker="Пакет · 3 сессии", short="7 000 ₽ за сессию.")
P("individ5", "Пакет из 5 сессий", "individualno/", "individ-paket5", "", "Хочу купить пакет из 5 индивидуальных сессий.", "Подскажите, пожалуйста, ближайшее время и как оплатить.", kicker="Пакет · 5 сессий", short="7 000 ₽ за сессию — для продолжительной работы.")
P("individ-povtor", "Повторная сессия", "individualno/", "individ-povtor", "", "Я уже был(а) у вас на сессии — хочу записаться на повторную индивидуальную сессию.", "Подскажите, пожалуйста, ближайшее время и как оплатить.", kicker="Для постоянных клиентов", short="Для тех, кто уже был у Марины на сессии.")
P("marafon:samoprinyatie", "Марафон «Самопринятие»", "marafon/samoprinyatie/", "marafon-samoprinyatie", "", "Хочу участвовать в марафоне «Самопринятие» (5 недель).", kicker="Марафон · 5 недель", short="5 недель мягкой трансформации в поддерживающем кругу.")
P("marafon:dvizhenie", "Марафон «Движение к цели»", "marafon/dvizhenie-k-celi/", "marafon-dvizhenie", "", "ХОЧУ В ДВИЖЕНИЕ — участвовать в марафоне «Движение к цели» (14 дней).", "Подскажите, как оплатить и когда старт.", kicker="Марафон · 14 дней", short="8 шагов и 3 живых эфира, чтобы сдвинуться с мёртвой точки.")
P("psy", "Наставничество «Архитектор продукта»", "psihologam/", "arhitektor-produkta", "", "Хочу обсудить наставничество «Архитектор продукта» для своего проекта.", "Расскажите, пожалуйста, как проходит работа и как оплатить.", kicker="Для психологов · 1–2 месяца", short="Создать свою трансформационную игру или программу.")
P("psy-wait", "Лист ожидания: обучение ведению Т-игр", "psihologam/", "psy-obuchenie", "", "Хочу встать в лист ожидания на обучение ведению Т-игр и групп с МАК.", "Сообщите, пожалуйста, когда откроется набор.", noprice=True)
P("vopros", "Вопрос Марине", "marina/", "vopros", "", "У меня вопрос.", "", noprice=True)

def cta(key, label="Записаться", cls="btn", title=None):
    p = PROD[key]
    static = (p["head"] + " " + p["tail"]).strip()
    return ('<a href="%s" class="%s" target="_blank" rel="noopener" data-cta="%s" data-group="%s" data-title="%s" data-head="%s" data-tail="%s"%s>%s</a>'
            % (e(TG + "?text=" + _q(static, safe="")), cls, p["code"], p["g"], e(title or p["t"]), e(p["head"]), e(p["tail"]), " data-noprice" if p["np"] else "", label))
def price(key): p = PROD[key]; return '<span data-price="%s" data-group="%s">%s</span>' % (p["code"], p["g"], pr(p["code"], p["g"]))
def prodcard(key, root):
    p = PROD[key]
    return ('<article class="pcard glass rv"><span class="kick">%s</span><h3><a href="%s%s">%s</a></h3><p class="muted">%s</p><div class="pfoot"><b class="pp">%s</b>%s</div></article>'
            % (e(p["k"]), root, p["u"], e(p["t"]), e(p["s"]), price(key), cta(key, "Записаться", "btn sm")))

# ---------------------------------------------------------------- макет
NAV = [("navigator/", "Навигатор", "nav"), ("znaniya/", "Знания", "zn"), ("podarki/", "Подарки", "gift"), ("ceny/", "Форматы и цены", "price"), ("marina/", "Марина", "mar")]
LOGO = '<svg class="logo-i" viewBox="0 0 40 40" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7cf7ff"/><stop offset=".5" stop-color="#9b7bff"/><stop offset="1" stop-color="#ff6bd6"/></linearGradient></defs><circle cx="20" cy="20" r="17" fill="none" stroke="url(#lg)" stroke-width="2.5"/><path d="M8 20h6l3-7 6 14 3-7h6" fill="none" stroke="url(#lg)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

MODAL = '''<div class="toast" id="toast" role="status" aria-live="polite"></div>
<div class="modal" id="cta-modal" role="dialog" aria-modal="true" aria-labelledby="m-t"><div class="mbox glass">
<button class="mclose" type="button" aria-label="Закрыть">×</button>
<span class="kick">Запись к Марине</span><h3 id="m-t" data-m-title></h3>
<p class="small muted">Стоимость: <b data-m-price></b> · Ближайшая дата: <b data-m-date></b></p>
<p class="small" data-m-paynote>Напишите Марине — она пришлёт детали для оплаты.</p>
<p class="small muted">Текст сообщения (подставится в Telegram и скопируется):</p>
<div class="codebox" data-m-msg></div>
<div class="btns"><a class="btn" data-m-tg href="https://t.me/MarinaNew" target="_blank" rel="noopener">Написать Марине в Telegram</a>
<a class="btn ghost hidden" data-m-pay target="_blank" rel="noopener">Оплатить онлайн</a>
<button class="btn ghost" data-m-copy type="button">Скопировать текст</button></div>
<p class="ok small"></p>
<p class="small muted">Все сессии проходят онлайн и вживую — с Мариной Степановой. Группы до 8 человек.</p>
</div></div>'''
GIFT = '''<div class="giftpop glass" id="giftpop" role="dialog" aria-labelledby="gp-t" hidden><button class="mclose" type="button" aria-label="Закрыть" data-gp-close>×</button>
<span class="kick">Подарок перед уходом</span><b id="gp-t">Узнайте за 2 минуты, кто жмёт на ваши тормоза</b><p class="small muted">Бесплатный тест: 8 ситуаций → персональный разбор и следующий шаг.</p>
<a class="btn sm" data-gp-go href="#">Пройти тест</a></div>'''

def layout(path, title, desc, body, active="", mcta=None, jsonld=None, tools=False, og="og.png", ogtype="website", crumbs=None):
    depth = 0 if path in ("", "404.html") else path.rstrip("/").count("/") + 1
    root = BASE if path == "404.html" else "../" * depth
    home_href = root or "./"
    url = SITE + ("" if path == "404.html" else path)
    full = title if BRAND in title else "%s — %s" % (title, BRAND)
    nav = "".join('<a href="%s%s"%s>%s</a>' % (root, u, ' class="on" aria-current="page"' if k == active else "", t) for u, t, k in NAV)
    lds = []
    if jsonld: lds += jsonld if isinstance(jsonld, list) else [jsonld]
    bc = ""
    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": BRAND, "item": SITE}] + [
            {"@type": "ListItem", "position": i + 2, "name": n, "item": SITE + u} for i, (u, n) in enumerate(crumbs)]
        lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
        bc = '<nav class="crumbs" aria-label="Хлебные крошки"><a href="%s">%s</a>%s</nav>' % (home_href, BRAND, "".join(
            ' <span>/</span> ' + ('<a href="%s%s">%s</a>' % (root, u, e(n)) if i < len(crumbs) - 1 else '<span aria-current="page">%s</span>' % e(n)) for i, (u, n) in enumerate(crumbs)))
    ld = "".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in lds)
    mob = '<div class="mbar">%s<a class="btn ghost sm" href="%snavigator/">Навигатор</a></div>' % (mcta or cta("diag", "Диагностика · 1 000 ₽", "btn sm"), root)
    tl = ('<script src="%sassets/tools.js?v=%s"></script>' % (root, V)) if tools else ""
    html = f'''<!doctype html><html lang="ru" class="no-js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(full)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="{ogtype}"><meta property="og:site_name" content="{BRAND}"><meta property="og:locale" content="ru_RU"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}assets/{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#07061a"><link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<link rel="preload" href="{root}assets/fonts/unbounded-cyrillic.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{root}assets/style.css?v={V}">{ld}</head>
<body data-root="{root}" data-page="{path or 'home'}"><canvas id="cosmos" aria-hidden="true"></canvas>
<a class="skip" href="#main">К содержанию</a>
<header class="top"><div class="wrap topin"><a class="logo" href="{home_href}">{LOGO}<span>{BRAND}</span></a><nav class="nav" id="nav" aria-label="Главное меню">{nav}</nav>
<a class="me" href="{root}moj-put/" title="Мой путь: уровень и награды"><span class="lvl" data-lvl>1</span><span class="me-t">Мой путь</span></a><button class="burger" type="button" aria-label="Меню" aria-controls="nav" aria-expanded="false"><span></span><span></span></button></div></header>
<main id="main">{('<div class="wrap">' + bc + '</div>') if bc else ''}{body}</main>
<footer class="foot"><div class="wrap fgrid"><div><a class="logo" href="{home_href}">{LOGO}<span>{BRAND}</span></a><p class="muted small">Психологическая лаборатория Марины Степановой: знания, бесплатные инструменты и живые онлайн-сессии в группах до 8 человек.</p>
<p class="small"><a href="{root}vazhno/">Важно: не замена медицинской помощи</a> · <a href="{root}konfidencialnost/">Конфиденциальность</a></p></div>
<div><b>Начать</b><a href="{root}navigator/">Навигатор</a><a href="{root}testy/">Тесты</a><a href="{root}podarki/">Подарки</a><a href="{root}moj-put/">Мой путь</a></div>
<div><b>Знания</b><a href="{root}znaniya/">Энциклопедия</a><a href="{root}znaniya/igra-lila/">Игра «Лила»</a><a href="{root}znaniya/sindrom-samozvanca/">Синдром самозванца</a><a href="{root}znaniya/treugolnik-karpmana/">Треугольник Карпмана</a></div>
<div><b>Работа с Мариной</b><a href="{root}ceny/">Форматы и цены</a><a href="{root}diagnostika/">Диагностика</a><a href="{root}koleso-uspeha/">«Колесо успеха»</a><a href="{root}klub/">Закрытый клуб</a><a href="{root}psihologam/">Психологам</a><a href="{root}otzyvy/">Отзывы</a><a href="{root}faq/">Вопросы</a></div></div>
<div class="wrap small muted fbot">© Марина Степанова · Telegram <a href="{TG}" target="_blank" rel="noopener">@MarinaNew</a> · канал <a href="https://t.me/koleso_uspeha" target="_blank" rel="noopener">@koleso_uspeha</a> · Если вам сейчас очень плохо — <a href="{root}vazhno/#help">куда обратиться</a></div></footer>
{mob}{MODAL}{GIFT}
<script src="{root}assets/config.js?v={V}"></script><script src="{root}assets/catalog.js?v={V}"></script><script src="{root}assets/app.js?v={V}"></script>{tl}
</body></html>'''
    fp = os.path.join(OUT, path if path.endswith(".html") else os.path.join(path, "index.html"))
    os.makedirs(os.path.dirname(fp) or OUT, exist_ok=True)
    open(fp, "w", encoding="utf-8").write(html)
    PAGES.append((path, title))

def sec(inner, cls=""): return '<section class="sec %s"><div class="wrap">%s</div></section>' % (cls, inner)
def head(kick, h, lead=""): return '<div class="sh rv"><span class="kick">%s</span><h2>%s</h2>%s</div>' % (kick, h, ('<p class="lead">%s</p>' % lead) if lead else "")
def ticks(items, cls=""): return '<ul class="ticks %s">%s</ul>' % (cls, "".join("<li>%s</li>" % e(i) for i in items))
def rev(key, label, limit=1, start=0):
    return "".join('<blockquote class="rev glass rv"><p>%s</p><cite>%s</cite></blockquote>' % (e(t), e(s or label or "Участница")) for t, s in R.get(key, [])[start:start + limit])
def readmin(a):
    words = len(" ".join([a["lead"]] + a["body"] + a["signs"] + a["practice"][1]).split())
    return max(2, round(words / 170))
def acard(slug, root):
    a = ARTICLES[slug]; d = a["desc"]
    return ('<a class="acard glass rv" href="%sznaniya/%s/" data-art="%s"><span class="kick">%s · %d мин</span><b>%s</b><span class="muted small">%s</span><i class="seen" aria-hidden="true">✓ прочитано</i></a>'
            % (root, slug, slug, e(CAT[a["cat"]]), readmin(a), e(a["title"]), e(d if len(d) < 125 else d[:120].rsplit(" ", 1)[0] + "…")))
def tcard(slug, root):
    t = TESTD[slug]
    return '<a class="tcard glass rv" href="%stesty/%s/" data-testlink="%s"><span class="emo">%s</span><b>%s</b><span class="muted small">%s</span><span class="chip">%d мин · бесплатно</span><i class="seen" aria-hidden="true">✓ пройден</i></a>' % (root, slug, slug, t["emoji"], e(t["title"]), e(t["desc"]), t["mins"])

GIFTS = [("testy/", "🧭", "8 тестов-самонаблюдений", "Самозванец, денежный сценарий, гиперконтроль, колесо баланса — с персональным разбором."),
         ("karta-dnya/", "🃏", "Карта дня", "Генеративный образ и вопрос для самоисследования. Новая карта каждый день."),
         ("mini-lila/", "🎲", "Мини-Лила онлайн", "Упрощённая игра самоисследования: кубик, 36 клеток, змеи и стрелы."),
         ("dyhanie/", "🌬", "Дыхание 4–6", "Таймер медленного дыхания: 1, 3 или 5 минут, чтобы выдохнуть."),
         ("7-dnej/", "🔥", "Челлендж «7 дней»", "Неделя коротких практик: от денежных установок до плана мечты."),
         ("chek-listy/", "📄", "Чек-листы для печати", "PDF: «Тащу всё на себе», «Мои денежные установки», «Колесо баланса»."),
         ("znaniya/", "📚", "Энциклопедия", "%d статей простым языком — с практиками и источниками." % len(ARTICLES)),
         ("moj-put/", "🏅", "Мой путь", "Ваш прогресс, результаты тестов, награды и следующий шаг.")]
def giftgrid(root, n=8): return '<div class="grid g4">%s</div>' % "".join('<a class="gcard glass rv" href="%s%s"><span class="emo">%s</span><b>%s</b><span class="muted small">%s</span></a>' % (root, u, i, e(t), e(d)) for u, i, t, d in GIFTS[:n])

TOPIC_ART = {"dengi": ["dengi-scenarii", "finansovyj-potolok", "kak-nazyvat-cenu"], "strahi": ["strah-uspeha", "sindrom-samozvanca", "bazovyj-strah"],
             "kontrol": ["giperkontrol", "giperotvetstvennost", "delegirovanie"], "konflikty": ["treugolnik-karpmana", "konflikty", "emocionalnyj-intellekt"],
             "proyavlennost": ["proyavlennost", "kak-nazyvat-cenu", "sindrom-samozvanca"], "samoocenka": ["samocennost-i-samoocenka", "perfekcionizm", "prokrastinaciya"],
             "celi": ["mechta-i-cel", "zona-komforta", "neyroplastichnost-i-privychki"]}
TOPIC_TEST = {"dengi": "dengi", "strahi": "tormoza", "kontrol": "kontrol", "konflikty": "karpman", "proyavlennost": "samozvanec", "samoocenka": "perfekcionizm", "celi": "koleso"}

def learn_block(topics, root, title="Перед записью — разберитесь глубже"):
    arts, tests = [], []
    for tp in topics:
        for s in TOPIC_ART.get(tp, []):
            if s not in arts: arts.append(s)
        t = TOPIC_TEST.get(tp)
        if t and t not in tests: tests.append(t)
    return sec(head("Бесплатно", title) + '<div class="grid g3">%s</div><div class="grid g3 mt">%s</div>' % ("".join(acard(s, root) for s in arts[:3]), "".join(tcard(t, root) for t in tests[:2])), "alt")

def buybox(key, rows, label="Записаться"):
    p = PROD[key]
    rr = "".join("<li><span>%s</span><b>%s</b></li>" % (a, b) for a, b in rows)
    return ('<aside class="buy glass rv"><span class="kick">Стоимость</span><div class="big">%s</div><p class="small muted" data-pnote="%s"></p><ul class="kv">%s<li><span>Ближайшая дата</span><b><span data-date="%s" data-group="%s">Дата уточняется</span></b></li></ul>%s<p class="small muted">Онлайн, вживую, с Мариной Степановой.</p></aside>'
            % (price(key), p["code"], rr, p["code"], p["g"], cta(key, label, "btn block")))

def hero(kick, h1, lead, btns="", extra="", cls=""):
    return '<section class="hero %s"><div class="wrap"><span class="kick rv">%s</span><h1 class="rv">%s</h1>%s%s%s</div></section>' % (cls, kick, h1, ('<p class="lead rv">%s</p>' % lead) if lead else "", ('<div class="btns rv">%s</div>' % btns) if btns else "", extra)

LADDER = [("Бесплатно", "Тесты, карта дня, Мини-Лила, энциклопедия", "podarki/", "0 ₽", None),
          ("Диагностика", "Лично, 1 на 1, 30 минут — засчитывается в покупку", "diagnostika/", None, "diag"),
          ("Мини-тренинг", "Групповая диагностика с лёгким разворотом, 1–1,5 часа", "ceny/#mini", None, "mini:samozvanets"),
          ("Клуб", "Медитации по понедельникам, групповые «Разборы»", "klub/", None, "klub"),
          ("Игра «Лила»", "4 часа, до 4 игроков, авторская версия", "lila/", None, "lila"),
          ("Тренинг", "2–3 часа, группа до 8, глубина личной сессии", "ceny/#trening", None, "trening:strah-uspeha"),
          ("Сессия 1 на 1", "1–2 часа, разбор архитектуры мышления", "individualno/", None, "individ"),
          ("Модуль", "1 месяц, 4 тренинга по одной сфере", "ceny/#modul", None, "modul:1"),
          ("«Колесо успеха»", "6 месяцев, 24 тренинга, полная трансформация", "koleso-uspeha/", None, "koleso")]
def ladder(root):
    return '<div class="ladder">%s</div>' % "".join('<a class="step glass rv" href="%s%s" style="--i:%d"><span class="n">%02d</span><b>%s</b><span class="muted small">%s</span><span class="pp">%s</span></a>' % (root, u, i, i + 1, e(t), e(d), fixed or price(key)) for i, (t, d, u, fixed, key) in enumerate(LADDER))

def marina_block(root):
    return f'''<div class="marina glass rv"><img src="{root}assets/img/marina.jpg" alt="Марина Степанова" width="400" height="485" loading="lazy"><div>
<span class="kick">Ведущая всех живых сессий</span><h2>Марина Степанова</h2>
<p>Психолог, автор и ведущая трансформационных игр и тренингов, предприниматель с 9-летним опытом. Сначала она разбирает систему мышления человека как архитектуру: убеждения, эмоциональные реакции, защиты и привычные сценарии. А затем вместе с ним перенастраивает её — часто уже за одну встречу.</p>
<p class="muted">В работе — МАК-карты и авторские протоколы, сложившиеся в практике: микс психологических, трансперсональных и трансцендентных техник.</p>
<div class="btns"><a class="btn ghost" href="{root}marina/">О Марине</a>{cta("vopros", "Задать вопрос", "btn ghost")}</div></div></div>'''

NAVBOX = '<div class="navbox glass rv" data-navigator><div class="nv-head"><span class="nv-dot"></span><b>Проводник Внутрикода</b><span class="nv-mode" data-nv-mode>Навигатор · сценарий</span></div><div class="nv-log" data-nv-log aria-live="polite"></div><div class="nv-opts" data-nv-opts></div><form class="nv-form" data-nv-form><input type="text" data-nv-input placeholder="Или опишите своими словами…" aria-label="Ваш вопрос навигатору" maxlength="500"><button class="btn sm" type="submit">→</button></form><noscript><p>Для навигатора нужен JavaScript. <a href="znaniya/">Перейти в энциклопедию</a>.</p></noscript></div>'

# ================================================================ HOME
def home():
    root = ""
    popular = ["sindrom-samozvanca", "giperotvetstvennost", "dengi-scenarii", "treugolnik-karpmana", "igra-lila", "prokrastinaciya"]
    revs = rev("bazovyj-strah", "Участница тренинга «Базовый страх»", 1, 2) + rev("igra-lila", "Участница игры «Лила»") + rev("mini-bez-menya", "Участница мини-тренинга «Без меня никто не справится!»")
    body = f'''<section class="hero home"><div class="wrap hgrid"><div>
<span class="kick rv">Психологическая лаборатория Марины Степановой</span>
<h1 class="rv glow">Внутри&shy;код</h1>
<p class="lead rv">Ваши решения о деньгах, целях и людях подчиняются внутреннему коду: убеждениям, страхам и сценариям. Здесь его можно <b>расшифровать</b> — бесплатно, с тестами и знаниями, — и <b>перенастроить</b> вживую с Мариной.</p>
<div class="btns rv"><a class="btn" href="#navigator">Запустить навигатор</a><a class="btn ghost" href="testy/tormoza/">Тест «Кто жмёт на тормоза?»</a></div>
<div class="chips rv"><span class="chip">{len(ARTICLES)} статей</span><span class="chip">{len(TESTS)} тестов</span><span class="chip">Мини-Лила онлайн</span><span class="chip">Группы до 8 человек</span></div></div>
<div class="orb rv" aria-hidden="true"><div class="core"></div><span class="ring r1"></span><span class="ring r2"></span><span class="ring r3"></span></div></div></section>
<section class="sec" id="navigator"><div class="wrap">{head("Интерактивный навигатор", "Ваш личный маршрут за 1 минуту", "Ответьте на 4 вопроса — навигатор соберёт путь: подарок, статья, тест и живой шаг с Мариной. Работает прямо в браузере, без регистрации.")}{NAVBOX}</div></section>
{sec(head("Метод", "Распознать → углубить → развернуть в ресурс", "Так устроена каждая живая сессия Марины. Первый шаг вы можете сделать сами.") + '<div class="grid g3"><div class="glass card rv"><span class="num">1</span><h3>Распознать</h3><p class="muted">Тесты и статьи помогают увидеть, какой «код» срабатывает: самозванец, денежный сценарий, гиперконтроль, роль в треугольнике.</p></div><div class="glass card rv"><span class="num">2</span><h3>Углубить</h3><p class="muted">На диагностике и мини-тренинге вы видите, откуда растёт сценарий и что он охраняет.</p></div><div class="glass card rv"><span class="num">3</span><h3>Развернуть в ресурс</h3><p class="muted">На тренингах и сессиях Марина шаг за шагом перенастраивает реакцию — вы уходите с результатом и планом на 24 часа.</p></div></div>')}
{sec(head("Бесплатные подарки", "Начните с того, что откликается", "Всё бесплатно и без регистрации. Прогресс сохраняется только в вашем браузере.") + giftgrid(root), "alt")}
{sec(head("Энциклопедия", "Психология простым языком — с источниками", "Статьи связаны между собой: от самозванца к цене, от контроля к делегированию, от «Лилы» к МАК-картам.") + '<div class="grid g3">' + "".join(acard(s, root) for s in popular) + '</div><div class="btns center"><a class="btn ghost" href="znaniya/">Все статьи</a></div>')}
{sec(head("Лестница форматов", "От бесплатного теста до полной трансформации", "Каждая ступень логично ведёт к следующей.") + ladder(root) + '<div class="btns center"><a class="btn" href="ceny/">Все форматы и цены</a></div>', "alt")}
{sec(marina_block(root))}
{sec(head("Отзывы", "Что говорят участники") + '<div class="grid g3">' + revs + '</div><div class="btns center"><a class="btn ghost" href="otzyvy/">Все отзывы</a></div>', "alt")}
{sec('<div class="band glass rv"><h2>Не знаете, с чего начать?</h2><p>Личная диагностика: 30 минут один на один с Мариной. Её стоимость засчитывается, если вы продолжите работу.</p><div class="btns center">' + cta("diag", "Записаться на диагностику · 1 000 ₽") + '<a class="btn ghost" href="#navigator">Сначала навигатор</a></div></div>')}'''
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": SITE, "inLanguage": "ru"},
          {"@context": "https://schema.org", "@type": "Person", "name": "Марина Степанова", "jobTitle": "Психолог, автор и ведущая трансформационных игр и тренингов", "url": SITE + "marina/", "image": SITE + "assets/img/marina.jpg", "sameAs": ["https://t.me/koleso_uspeha"]}]
    layout("", "Внутрикод — расшифруйте свой внутренний код с Мариной Степановой", "Психологическая лаборатория: интерактивный навигатор, 8 бесплатных тестов, энциклопедия, Мини-Лила и живые онлайн-сессии с психологом Мариной Степановой в группах до 8 человек.", body, "home", jsonld=ld, tools=True)

def navigator_page():
    root = "../"
    body = hero("Интерактивный навигатор", "Соберите свой маршрут", "4 вопроса — и вы получите персональный путь: с чего начать бесплатно и какой живой шаг с Мариной подойдёт именно вам. По умолчанию навигатор работает по готовому сценарию прямо в браузере. Если в окне стоит метка «ИИ-помощник», свободный текст отправляется ИИ-помощнику для ответа — не пишите туда личные данные.") + sec(NAVBOX.replace('href="znaniya/"', 'href="../znaniya/"'))
    body += sec(head("Или выберите сами", "Темы, с которыми приходят чаще всего") + '<div class="grid g4">' + "".join('<a class="gcard glass rv" href="%sznaniya/%s/"><b>%s</b><span class="muted small">Статья · тест · живой шаг</span></a>' % (root, th["articles"][0], e(th["label"])) for th in NAV_THEMES.values()) + "</div>", "alt")
    layout("navigator/", "Навигатор: ваш личный маршрут", "Интерактивный навигатор подберёт бесплатный подарок, статью, тест и живой шаг с Мариной Степановой под ваш запрос.", body, "nav", tools=True, crumbs=[("navigator/", "Навигатор")])

def enc_index():
    root = "../"
    chips = '<button class="fchip on" type="button" data-cat="all">Все</button>' + "".join('<button class="fchip" type="button" data-cat="%s">%s</button>' % (k, e(v)) for k, v in CATS)
    cards = "".join('<div class="encit" data-c="%s" data-q="%s">%s</div>' % (a["cat"], e((a["title"] + " " + a["desc"]).lower()), acard(s, root)) for s, a in ARTICLES.items())
    body = hero("Энциклопедия", "Знания о внутреннем коде", "%d коротких статей о страхах, деньгах, контроле, отношениях, привычках и трансформационных играх. В каждой — чек-лист, мини-практика, связанные темы и источники." % len(ARTICLES),
                extra='<div class="encbar rv"><input type="search" id="encq" placeholder="Поиск: самозванец, деньги, Лила…" aria-label="Поиск по статьям"><div class="fchips">%s</div><p class="small muted" id="encstat"></p></div>' % chips)
    body += sec('<div class="grid g3" id="enc">%s</div><p class="muted hidden" id="encempty">Ничего не нашлось. Попробуйте другое слово или <a href="../navigator/">спросите навигатор</a>.</p>' % cards)
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Энциклопедия Внутрикода", "url": SITE + "znaniya/", "hasPart": [{"@type": "Article", "headline": a["title"], "url": SITE + "znaniya/%s/" % s} for s, a in ARTICLES.items()]}
    layout("znaniya/", "Энциклопедия психологии: страхи, деньги, контроль, Лила", "Короткие статьи о синдроме самозванца, страхе успеха, денежных сценариях, гиперконтроле, треугольнике Карпмана, перфекционизме, игре «Лила» и МАК-картах — с практиками и источниками.", body, "zn", jsonld=ld, tools=True, crumbs=[("znaniya/", "Энциклопедия")])

ORDER = list(ARTICLES.keys())
def article(slug):
    a = ARTICLES[slug]; root = "../../"
    nxt = ORDER[(ORDER.index(slug) + 1) % len(ORDER)]
    signs = "".join('<li><label><input type="checkbox" data-sign> <span>%s</span></label></li>' % e(s) for s in a["signs"])
    steps = "".join("<li>%s</li>" % e(s) for s in a["practice"][1])
    src = "".join('<li>%s</li>' % (('<a href="%s" target="_blank" rel="noopener nofollow">%s</a>' % (e(u), e(t))) if u else e(t)) for t, u in a["sources"])
    key = a["cta"]; p = PROD[key]; t = TESTD[a["test"]]
    paras = "".join("<p>%s</p>" % e(x) for x in a["body"])
    body = f'''<article class="art" data-article="{slug}"><div class="readbar" aria-hidden="true"><i></i></div>
<header class="hero art-h"><div class="wrap narrow"><a class="chip" href="{root}znaniya/?cat={a["cat"]}">{e(CAT[a["cat"]])}</a> <span class="chip">{readmin(a)} мин чтения</span>
<h1 class="rv">{e(a["title"])}</h1><p class="lead rv">{e(a["lead"])}</p></div></header>
<div class="wrap narrow prose">{paras}
<section class="glass box rv"><span class="kick">Как это проявляется</span><h2>Отметьте, что узнаёте в себе</h2><ul class="checks">{signs}</ul><p class="small" data-signres>Отмечено: 0 из {len(a["signs"])}.</p>
<a class="btn sm" href="{root}testy/{t["slug"]}/">Тест «{e(t["title"])}» · {t["mins"]} мин</a></section>
<section class="glass box rv practice"><span class="kick">Мини-практика · 5–10 минут</span><h2>{e(a["practice"][0])}</h2><ol class="steps">{steps}</ol>
<button class="btn ghost sm" type="button" data-done="{slug}">Я сделала практику ✓</button></section>
<section class="glass box rv offer"><span class="kick">Следующий шаг — вживую с Мариной</span><h2><a href="{root}{p["u"]}">{e(p["t"])}</a></h2><p>{e(p["s"] or "Живая онлайн-работа — пошагово от распознавания к развороту в ресурс.")}</p>
<div class="pfoot"><b class="pp">{price(key)}</b>{cta(key, "Записаться", "btn")}<a class="btn ghost" href="{root}{p["u"]}">Подробнее</a></div></section>
<section class="src"><h2>Источники</h2><ol>{src}</ol><p class="small muted">Статья носит просветительский характер и не заменяет консультацию врача или психотерапевта. <a href="{root}vazhno/">Подробнее</a>.</p></section>
</div>
<div class="wrap">{head("Читать дальше", "Связанные темы")}<div class="grid g3">{"".join(acard(s, root) for s in a["related"][:6])}</div>
<div class="btns center"><a class="btn" href="{root}znaniya/{nxt}/">Следующая статья: {e(ARTICLES[nxt]["title"])} →</a></div></div></article>'''
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"], "inLanguage": "ru", "url": SITE + "znaniya/%s/" % slug,
          "image": SITE + "assets/og/%s.png" % slug, "author": {"@type": "Person", "name": "Марина Степанова"}, "publisher": {"@type": "Organization", "name": BRAND},
          "datePublished": "2026-10-26", "citation": [u for _, u in a["sources"] if u]}
    layout("znaniya/%s/" % slug, a["title"], a["desc"], body, "zn", mcta=cta(key, "Записаться · " + pr(p["code"], p["g"]), "btn sm"), jsonld=ld, tools=True, og="og/%s.png" % slug, ogtype="article",
           crumbs=[("znaniya/", "Энциклопедия"), ("znaniya/%s/" % slug, a["title"])])

def tests_index():
    root = "../"
    body = hero("Бесплатные тесты", "Тесты-самонаблюдения", "8 авторских опросников с персональным разбором. Это не клиническая диагностика, а способ честно посмотреть на себя и выбрать следующий шаг. Ответы остаются только в вашем браузере.")
    body += sec('<div class="grid g4">%s</div>' % "".join(tcard(t["slug"], root) for t in TESTS))
    layout("testy/", "Бесплатные психологические тесты", "Индекс самозванца, денежный сценарий, кто жмёт на тормоза, гиперконтроль, колесо баланса, индикатор ресурса, треугольник Карпмана, перфекционизм — бесплатно, с разбором.", body, "gift", tools=True, crumbs=[("podarki/", "Подарки"), ("testy/", "Тесты")])

def test_page(t):
    root = "../../"
    others = [x["slug"] for x in TESTS if x["slug"] != t["slug"]][:3]
    sp = PROD[t["step"]]
    body = f'''<section class="hero"><div class="wrap narrow"><span class="kick rv">Бесплатный тест · {t["mins"]} мин</span><h1 class="rv">{t["emoji"]} {e(t["title"])}</h1><p class="lead rv">{e(t["desc"])}</p></div></section>
<section class="sec"><div class="wrap narrow"><div class="quiz glass rv" data-test="{t["slug"]}"><noscript>Для теста нужен JavaScript.</noscript></div>
<p class="small muted">Это авторский опросник для самонаблюдения, а не психологическая или медицинская диагностика. Результат хранится только в вашем браузере.</p></div></section>
{sec(head("Ещё подарки", "Другие тесты") + '<div class="grid g3">' + "".join(tcard(s, root) for s in others) + '</div>', "alt")}'''
    layout("testy/%s/" % t["slug"], "Тест «%s»" % t["title"], t["desc"], body, "gift", tools=True, og="og/test-%s.png" % t["slug"], crumbs=[("testy/", "Тесты"), ("testy/%s/" % t["slug"], t["title"])],
           mcta=cta(t["step"], "Живой шаг · " + pr(sp["code"], sp["g"]), "btn sm"))

# ================================================================ GIFTS & TOOLS
def gifts():
    root = "../"
    body = hero("Бесплатно", "Подарки Внутрикода", "Инструменты, к которым хочется возвращаться: тесты, карта дня, Мини-Лила, дыхание, челлендж и чек-листы. Без регистрации.") + sec(giftgrid(root))
    body += sec('<div class="band glass rv"><h2>Хотите живой разбор?</h2><p>Подарки помогают распознать «код». Перенастроить его быстрее вместе с Мариной — на диагностике или мини-тренинге.</p><div class="btns center">%s<a class="btn ghost" href="../ceny/">Все форматы</a></div></div>' % cta("diag", "Диагностика · 1 000 ₽"), "alt")
    layout("podarki/", "Бесплатные подарки: тесты, карта дня, Мини-Лила", "Бесплатные инструменты самопознания: 8 тестов, генеративная карта дня, онлайн Мини-Лила, дыхательный таймер, 7-дневный челлендж и чек-листы в PDF.", body, "gift", crumbs=[("podarki/", "Подарки")])

def card_day():
    root = "../"
    body = f'''<section class="hero"><div class="wrap narrow"><span class="kick rv">Подарок · каждый день новая</span><h1 class="rv">🃏 Карта дня</h1><p class="lead rv">Абстрактный образ, созданный алгоритмом на сегодняшнюю дату, и вопрос к нему. Посмотрите 30 секунд и запишите первое, что приходит. Это метафорическая практика, а не гадание.</p></div></section>
<section class="sec"><div class="wrap"><div class="cardday glass rv" data-cardday><div class="cd-art"><canvas width="600" height="840" role="img" aria-label="Абстрактная карта дня"></canvas></div><div class="cd-txt"><span class="kick" data-cd-date></span><h2 data-cd-word></h2><p class="lead" data-cd-q></p>
<label class="small muted" for="cd-note">Мой ответ (сохраняется только в браузере)</label><textarea id="cd-note" rows="4" data-cd-note placeholder="Что вы видите? Как это связано с вашим днём?"></textarea>
<div class="btns"><button class="btn" type="button" data-cd-save>Сохранить ответ</button><button class="btn ghost" type="button" data-cd-more>Ещё одна карта</button></div><p class="small ok" data-cd-ok></p></div></div>
<p class="small muted">Образы генерируются кодом из даты — это оригинальные абстракции, а не изображения из колод МАК. С настоящими МАК-картами Марина работает на тренингах. <a href="{root}znaniya/mak-karty/">Что такое МАК →</a></p></div></section>
{sec(head("Глубже", "Поработать с картами вживую") + '<div class="grid g3">' + prodcard("mini:samozvanets", root) + prodcard("diag", root) + prodcard("klub", root) + '</div>', "alt")}'''
    layout("karta-dnya/", "Карта дня — метафорическая практика", "Бесплатная генеративная карта дня с вопросом для самоисследования. Новая абстракция каждый день.", body, "gift", tools=True, crumbs=[("podarki/", "Подарки"), ("karta-dnya/", "Карта дня")])

def mini_lila():
    root = "../"
    body = f'''<section class="hero"><div class="wrap"><span class="kick rv">Подарок · игра самоисследования</span><h1 class="rv">🎲 Мини-Лила</h1><p class="lead rv">Упрощённая онлайн-версия трансформационной игры: 36 клеток, кубик, змеи и стрелы. Сформулируйте запрос, бросайте кубик и отвечайте на вопросы клеток. Полная «Лила» (72 клетки, 4 часа, до 4 игроков) проходит вживую с Мариной.</p></div></section>
<section class="sec"><div class="wrap"><div class="lila" data-lila><noscript>Для игры нужен JavaScript.</noscript></div>
<p class="small muted">Названия и описания клеток созданы для этой мини-версии и не повторяют классическое поле. <a href="{root}znaniya/igra-lila/">История и правила классической «Лилы» →</a></p></div></section>
{sec(head("Полная игра", "Сыграть в «Лилу» с Мариной") + '<div class="grid g3">' + prodcard("lila", root) + acard("igra-lila", root) + acard("kletki-lily", root) + '</div>', "alt")}'''
    layout("mini-lila/", "Мини-Лила — бесплатная онлайн-игра самоисследования", "Бесплатная упрощённая онлайн-версия игры «Лила»: 36 клеток, кубик, змеи и стрелы, вопросы для самоисследования.", body, "gift", tools=True, crumbs=[("podarki/", "Подарки"), ("mini-lila/", "Мини-Лила")],
           mcta=cta("lila", "«Лила» с Мариной · " + pr("igra-lila"), "btn sm"))

def breath():
    root = "../"
    body = f'''<section class="hero"><div class="wrap narrow"><span class="kick rv">Подарок · практика</span><h1 class="rv">🌬 Дыхание 4–6</h1><p class="lead rv">Медленное дыхание с удлинённым выдохом — простой способ снизить напряжение. Следите за кругом: он растёт на вдохе и сжимается на выдохе.</p></div></section>
<section class="sec"><div class="wrap narrow"><div class="breath glass rv" data-breath><div class="bcirc" data-b-c><span data-b-txt>Готовы?</span></div>
<div class="bopts"><label>Ритм <select data-b-mode><option value="4,0,6,0">Вдох 4 · выдох 6</option><option value="4,4,4,4">Квадрат 4-4-4-4</option><option value="5,0,5,0">Ровное 5-5</option></select></label>
<label>Время <select data-b-min><option value="1">1 мин</option><option value="3" selected>3 мин</option><option value="5">5 мин</option></select></label></div>
<div class="btns center"><button class="btn" type="button" data-b-start>Начать</button><button class="btn ghost" type="button" data-b-stop>Стоп</button></div><p class="small muted center" data-b-left></p></div>
<p class="small muted">Если появилось головокружение или дискомфорт — вернитесь к обычному дыханию. Медленное дыхание изучено как способ расслабления (<a href="https://doi.org/10.3389/fnhum.2018.00353" target="_blank" rel="noopener">обзор Zaccaro et al., 2018</a>), но не является лечением.</p></div></section>
{sec(head("Регулярно", "Медитации по понедельникам — в закрытом клубе") + '<div class="grid g3">' + prodcard("klub", root) + acard("meditaciya-i-vnimanie", root) + acard("vygoranie", root) + '</div>', "alt")}'''
    layout("dyhanie/", "Дыхание 4–6 — бесплатный дыхательный таймер", "Бесплатный таймер медленного дыхания: ритм 4–6, квадрат, ровное дыхание. 1, 3 или 5 минут.", body, "gift", tools=True, crumbs=[("podarki/", "Подарки"), ("dyhanie/", "Дыхание")])

def challenge():
    root = "../"
    days = "".join(f'''<li class="cday glass rv"><label class="cchk"><input type="checkbox" data-ch="{n}"><span>День {n}</span></label><div><h3>{e(t)}</h3><p class="muted">{e(d)}</p><a class="small" href="{root}{u}/">Открыть практику →</a></div></li>''' for n, t, d, u, a in CHALLENGE)
    body = f'''<section class="hero"><div class="wrap narrow"><span class="kick rv">Подарок · 7 дней по 10–15 минут</span><h1 class="rv">🔥 Челлендж «Перезагрузка внутреннего кода»</h1><p class="lead rv">Каждый день — одна короткая практика из энциклопедии. Отмечайте выполненное: прогресс сохранится в «Моём пути». На 7-й день — ваше обновлённое колесо баланса.</p>
<div class="prog rv"><i data-ch-bar></i></div><p class="small" data-ch-stat></p></div></section>
<section class="sec"><div class="wrap narrow"><ol class="clist">{days}</ol>
<div class="band glass rv hidden" data-ch-done><h2>Неделя пройдена! 🎉</h2><p>Хотите, чтобы так было каждую неделю — с медитациями по понедельникам и живыми «Разборами»? Приходите в закрытый клуб.</p><div class="btns center">{cta("klub", "В клуб · " + pr("club"))}<a class="btn ghost" href="{root}diagnostika/">Личная диагностика</a></div></div></div></section>'''
    layout("7-dnej/", "Челлендж «7 дней»: перезагрузка внутреннего кода", "Бесплатный 7-дневный челлендж: короткие практики про деньги, контроль, самоценность, конфликты, проявленность и цели.", body, "gift", tools=True, crumbs=[("podarki/", "Подарки"), ("7-dnej/", "Челлендж 7 дней")])

PDFS = [("tashu-vsyo-na-sebe.pdf", "Чек-лист «Тащу всё на себе»", "12 признаков гиперответственности + практика «Инвентаризация чужого»."),
        ("denezhnye-ustanovki.pdf", "Рабочий лист «Мои денежные установки»", "Семейные фразы о деньгах, их влияние и взрослая версия."),
        ("koleso-balansa.pdf", "Колесо баланса для печати", "6 сфер «Колеса успеха» — оцените и обведите своё колесо.")]
def checklists():
    root = "../"
    cards = "".join('<a class="gcard glass rv" href="%sassets/pdf/%s" download data-pdf><span class="emo">📄</span><b>%s</b><span class="muted small">%s</span><span class="chip">PDF · скачать</span></a>' % (root, f, e(t), e(d)) for f, t, d in PDFS)
    body = hero("Подарок · для печати", "Чек-листы и рабочие листы", "Распечатайте, заполните ручкой — и возьмите на диагностику или тренинг: так работа пойдёт глубже.") + sec('<div class="grid g3">%s</div>' % cards)
    body += sec(head("Следующий шаг", "Разобрать результаты вживую") + '<div class="grid g3">' + prodcard("diag", root) + prodcard("mini:bez-menya", root) + prodcard("mini:finansovyj-strah", root) + "</div>", "alt")
    layout("chek-listy/", "Чек-листы и рабочие листы в PDF", "Бесплатные PDF: чек-лист «Тащу всё на себе», рабочий лист «Мои денежные установки», колесо баланса для печати.", body, "gift", tools=True, crumbs=[("podarki/", "Подарки"), ("chek-listy/", "Чек-листы")])

def my_path():
    body = '''<section class="hero"><div class="wrap"><span class="kick rv">Ваш прогресс · хранится только в этом браузере</span><h1 class="rv">🏅 Мой путь</h1><p class="lead rv">Здесь собирается всё, что вы прошли: статьи, тесты, практики и маршрут навигатора. Возвращайтесь — Внутрикод подскажет следующий шаг.</p></div></section>
<section class="sec"><div class="wrap"><div class="mypath" data-mypath><noscript>Для этой страницы нужен JavaScript.</noscript></div></div></section>'''
    layout("moj-put/", "Мой путь — прогресс и награды", "Ваш личный прогресс во Внутрикоде: прочитанные статьи, результаты тестов, награды, уровень и рекомендованный следующий шаг.", body, "", tools=True, crumbs=[("moj-put/", "Мой путь")])

# ================================================================ OFFERS
def prices_page():
    root = "../"
    minis = "".join(prodcard("mini:" + m["slug"], root) for m in MINIS)
    trs = "".join(prodcard("trening:" + s, root) for m in MODULES for s in m["trainings"])
    mods = "".join(prodcard("modul:%d" % m["n"], root) for m in MODULES)
    body = hero("Форматы и цены", "Лестница работы с Мариной", "Начните бесплатно, сделайте первый живой шаг за 1 000–1 500 ₽ и идите так глубоко, как нужно. Все сессии — онлайн, вживую, группы до 8 человек.")
    body += sec(ladder(root))
    body += sec(head("Почему такая цена", "Глубина индивидуальной сессии — в малой группе") + '<div class="grid g3"><div class="glass card rv"><h3>До 8 человек</h3><p class="muted">Оптимально 5. Каждый работает со своим запросом, а не слушает лекцию.</p></div><div class="glass card rv"><h3>Пошагово</h3><p class="muted">Распознавание → углубление → разворот в ресурс. В конце — конкретные шаги на 24 часа.</p></div><div class="glass card rv"><h3>Дешевле, чем лично</h3><p class="muted">Индивидуальная сессия у Марины — %s. Тренинг даёт сопоставимую глубину за %s.</p></div></div>' % (price("individ"), price("trening:strah-uspeha")), "alt")
    body += sec(head("Вход", "Диагностика, клуб и игра") + '<div class="grid g3">' + prodcard("diag", root) + prodcard("klub", root) + prodcard("lila", root) + "</div>")
    body += sec('<div id="mini"></div>' + head("1–1,5 часа · групповая диагностика", "Мини-тренинги", "Смотреть могут многие, активно играют 5–6 участников — каждый уходит с лёгким разворотом.") + '<div class="grid g3">' + minis + "</div>", "alt")
    body += sec('<div id="trening"></div>' + head("2–3 часа · группа до 8", "Трансформационные тренинги") + '<div class="grid g3">' + trs + prodcard("trening:samotsennost", root) + "</div>")
    body += sec('<div id="modul"></div>' + head("1 месяц · 4 тренинга", "Модули «Колеса успеха»", "Модуль выгоднее, чем 4 тренинга по отдельности.") + '<div class="grid g3">' + mods + "</div>", "alt")
    body += sec(head("Флагман", "«Колесо успеха»: 6 месяцев") + '<div class="grid g3">' + prodcard("koleso-part1", root) + prodcard("koleso", root) + prodcard("koleso-part2", root) + '</div><p class="note rv" data-upgrade></p>')
    body += sec(head("Лично", "Индивидуальная работа") + '<div class="grid g4">' + "".join(prodcard(k, root) for k in ("individ", "individ3", "individ5", "individ-povtor")) + "</div>", "alt")
    body += sec(head("Марафоны и программы", "Ещё форматы") + '<div class="grid g3">' + prodcard("marafon:dvizhenie", root) + prodcard("marafon:samoprinyatie", root) + prodcard("psy", root) + "</div>")
    ld = {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Форматы работы с Мариной Степановой", "itemListElement": [{"@type": "Offer", "name": PROD[k]["t"], "price": re.sub(r"\D", "", pr(PROD[k]["code"], PROD[k]["g"])), "priceCurrency": "RUB", "url": SITE + PROD[k]["u"]} for k in ("diag", "mini:samozvanets", "trening:strah-uspeha", "modul:1", "koleso", "individ", "lila")]}
    layout("ceny/", "Форматы и цены: от бесплатного теста до «Колеса успеха»", "Все форматы работы с психологом Мариной Степановой: диагностика 1 000 ₽, мини-тренинги 1 500 ₽, тренинги 5 000 ₽, модули 16 000 ₽, «Колесо успеха» 75 000 ₽, индивидуальные сессии, клуб, «Лила».", body, "price", jsonld=ld, crumbs=[("ceny/", "Форматы и цены")])

def clean(items): return [x for x in items if not re.search(r"\d+\s*%|3х|3x", x)]

def mini_page(m):
    root = "../../"; key = "mini:" + m["slug"]; pair = T.get(m["pair"])
    body = hero("Мини-тренинг · 1–1,5 часа · онлайн", e(m["title"]), e(m["hook"]), cta(key, "Записаться · " + pr("mini-" + m["slug"], "mini")) + '<a class="btn ghost" href="#ob">Что будет</a>')
    left = '<div class="glass box rv"><span class="kick">%s</span><h2>Это для вас, если</h2>%s</div><div class="glass box rv" id="ob"><h2>Что вы получите</h2>%s</div><div class="glass box rv"><h2>Формат</h2>%s</div>' % (e(m["aud"]), ticks(m["foryou"], "q"), ticks(m["res"]), ticks(["Групповая глубокая диагностика с лёгким разворотом.", "Смотреть могут многие, активно играют 5–6 участников.", "МАК-карты и вопросы ведущей.", "Только вживую, без записи."]))
    if R.get("mini-" + m["slug"]): left += '<div class="revs">%s</div>' % rev("mini-" + m["slug"], "Участница мини-тренинга", 2)
    body += sec('<div class="lay"><div>%s</div>%s</div>' % (left, buybox(key, [("Формат", "онлайн, вживую"), ("Длительность", "1–1,5 часа")])))
    if pair:
        body += sec('<div class="band glass rv"><span class="kick">Следующий шаг</span><h2>Полный тренинг «%s»</h2><p>%s</p><div class="btns center"><a class="btn" href="%strening/%s/">О тренинге</a></div></div>' % (e(pair["title"]), e(pair["short"]), root, pair["slug"]))
    body += learn_block(m["topics"], root)
    layout("mini/%s/" % m["slug"], "Мини-тренинг «%s»" % m["title"], ("%s Мини-тренинг с Мариной Степановой: 1–1,5 часа онлайн, групповая диагностика с лёгким разворотом." % m["hook"])[:290], body, "price", mcta=cta(key, "Записаться · " + pr("mini-" + m["slug"], "mini"), "btn sm"),
           crumbs=[("ceny/#mini", "Мини-тренинги"), ("mini/%s/" % m["slug"], m["title"])])

def training_page(s):
    t = T[s]; root = "../../"; key = "trening:" + s; p = PROD[key]
    mod = MOD.get(t["module"])
    mini = next((m for m in MINIS if m["pair"] == s), None)
    body = hero("Трансформационный тренинг · 2–3 часа · группа до 8", e(t["title"]), e(t["lead"]), cta(key, "Записаться · " + pr(p["code"], p["g"])) + ('<a class="btn ghost" href="%smodul/%s/">Весь модуль %d</a>' % (root, mod["slug"], mod["n"]) if mod else ""))
    left = ('<div class="glass box rv"><h2>%s</h2>%s</div>' % (e(t["sub"] or "Это для вас, если"), ticks(t["foryou"], "q")) if t["foryou"] else "") + '<div class="glass box rv"><h2>Что вы получите</h2>%s%s</div>' % (ticks(clean(t["results"])), ('<p class="note">%s</p>' % e(t["note"])) if t["note"] else "")
    left += '<div class="glass box rv"><h2>Как проходит</h2>%s</div>' % ticks(["Малая группа до 8 человек (оптимально 5) — глубина индивидуальной сессии.", "Пошагово: распознавание → углубление → разворот в ресурс.", "МАК-карты, вопросы и авторские протоколы Марины.", "Можно отвечать голосом или в чате.", "В конце — конкретные шаги на ближайшие 24 часа."])
    if R.get(s): left += '<div class="revs">%s</div>' % rev(s, "Участница тренинга «%s»" % t["title"], 2)
    body += sec('<div class="lay"><div>%s</div>%s</div>' % (left, buybox(key, [("Формат", "онлайн, вживую"), ("Длительность", "2–3 часа" if s != "samotsennost" else "3–3,5 часа"), ("Группа", "до 8 человек")])))
    nxt = ([prodcard("mini:" + mini["slug"], root)] if mini else []) + ([prodcard("modul:%d" % mod["n"], root)] if mod else [prodcard("marafon:samoprinyatie", root)]) + [prodcard("diag", root)]
    body += sec(head("Связанные форматы", "Начать мягче или пойти глубже") + '<div class="grid g3">%s</div>' % "".join(nxt))
    body += learn_block(t["topics"], root)
    layout("trening/%s/" % s, "Тренинг «%s»" % t["title"], ("%s Трансформационный тренинг с Мариной Степановой: онлайн, группа до 8 человек." % t["short"])[:290], body, "price",
           mcta=cta(key, "Записаться · " + pr(p["code"], p["g"]), "btn sm"), crumbs=[("ceny/#trening", "Тренинги"), ("trening/%s/" % s, t["title"])])

def module_page(m):
    root = "../../"; key = "modul:%d" % m["n"]
    trs = "".join(prodcard("trening:" + s, root) for s in m["trainings"])
    revs = rev("modul-6", None, 2) if m["n"] == 6 else ""
    body = hero("Модуль %d из 6 · 1 месяц · 4 тренинга · цель: %s" % (m["n"], e(m["goal"])), e(m["title"]), e(m["intro"]), cta(key, "Купить модуль · " + pr("modul-%d" % m["n"], "module")) + '<a class="btn ghost" href="%skoleso-uspeha/">Вся программа</a>' % root)
    body += sec('<div class="lay"><div><div class="glass box rv"><h2>Что внутри</h2>%s<p class="small muted" data-save="module" data-code="module"></p></div>%s</div>%s</div>' % (ticks(["4 живых трансформационных тренинга за месяц.", "Группа до 8 человек, глубина индивидуальной сессии.", "Последовательная работа с одной сферой — от осознания до новых действий."]), ('<div class="revs">%s</div>' % revs) if revs else "", buybox(key, [("Формат", "онлайн, вживую"), ("Длительность", "1 месяц"), ("Тренингов", "4")])))
    body += sec(head("Тренинги модуля", "4 шага месяца") + '<div class="grid g4">%s</div>' % trs, "alt")
    body += learn_block(m["topics"], root)
    layout("modul/%s/" % m["slug"], "Модуль %d «%s»" % (m["n"], m["title"]), ("%s Модуль программы «Колесо успеха»: 1 месяц, 4 тренинга онлайн." % m["intro"])[:290], body, "price", mcta=cta(key, "Купить модуль · " + pr("modul-%d" % m["n"], "module"), "btn sm"),
           crumbs=[("koleso-uspeha/", "«Колесо успеха»"), ("modul/%s/" % m["slug"], "Модуль %d" % m["n"])])

def flagship():
    root = "../"
    road = "".join('<a class="step glass rv" href="%smodul/%s/" style="--i:%d"><span class="n">М%d</span><b>%s</b><span class="muted small">Цель: %s</span><span class="pp">%s</span></a>' % (root, m["slug"], i, m["n"], e(m["title"]), e(m["goal"]), price("modul:%d" % m["n"])) for i, m in enumerate(MODULES))
    body = hero("Флагман · 6 модулей · 24 живых тренинга", "«Колесо успеха»", "6 месяцев, 6 сфер: деньги, страхи, внутренние ограничения, проявленность, ритм и цели. Каждая — месяц из 4 трансформационных тренингов в группе до 8 человек.", cta("koleso", "Купить программу · " + pr("koleso-full")) + '<a class="btn ghost" href="#tiers">Сравнить варианты</a><a class="btn ghost" href="%stesty/koleso/">Тест «Колесо баланса»</a>' % root)
    body += sec(head("Путь", "6 модулей = 6 спиц колеса") + '<div class="ladder six">%s</div>' % road)
    body += sec('<div id="tiers"></div>' + head("Варианты участия", "Целиком или частями") + '<div class="grid g3">' + prodcard("koleso-part1", root) + prodcard("koleso", root) + prodcard("koleso-part2", root) + '</div><p class="note rv" data-upgrade></p><p class="small muted" data-save="full" data-code="koleso-full"></p>', "alt")
    body += sec(head("Отзывы", "Участники тренингов программы") + '<div class="grid g3">%s</div>' % (rev("ya-vizhu-dengi", "Участница тренинга «Я вижу деньги»") + rev("strah-uspeha", "Участница тренинга «Страх успеха»") + rev("koroli-prokrastinacii", "Участница тренинга «Короли прокрастинации»")))
    layout("koleso-uspeha/", "Программа «Колесо успеха» — 6 месяцев, 24 тренинга", "Флагманская программа Марины Степановой: 6 модулей по месяцу — деньги, страхи, ограничения, проявленность, ритм, цели. Полностью или частями по 3 месяца.", body, "price",
           mcta=cta("koleso", "Купить · " + pr("koleso-full"), "btn sm"), crumbs=[("koleso-uspeha/", "«Колесо успеха»")])

def lila_page():
    root = "../"
    body = hero("Трансформационная игра · 4 часа · до 4 игроков · онлайн", "Игра «Лила» с Мариной", "Авторская версия Марины Степановой, переработанная для бизнеса и жизненных ситуаций (на основе версии Хариша Джохари). Найдите главную точку роста и увидьте скрытые сценарии через метафору пути.", cta("lila", "Записаться · " + pr("igra-lila")) + '<a class="btn ghost" href="%smini-lila/">Сначала Мини-Лила бесплатно</a>' % root)
    left = '<div class="glass box rv"><h2>Эта игра для вас, если</h2>%s</div><div class="glass box rv"><h2>В процессе игры вы</h2>%s<p class="note">«Лила» — часть индийской культурной и духовной традиции. Мы используем её как метафору и инструмент самоисследования, а не как предсказание.</p></div><div class="revs">%s</div>' % (
        ticks(["Бизнес застрял на одном уровне, и непонятно почему.", "Вы упускаете возможности, но боитесь рисковать.", "Сложно масштабироваться и делегировать.", "Внутренние страхи мешают смелым решениям.", "Хочется увидеть свою ситуацию целиком."], "q"),
        ticks(["Найдёте самую важную точку развития.", "Увидите скрытые сценарии, которые управляют жизнью.", "Поймёте, какие стратегии ведут вперёд, а какие — «по змее» вниз.", "Найдёте внутренние ресурсы и новые решения.", "Уйдёте с практическими инсайтами и шагом на 24 часа."]), rev("igra-lila", "Участница игры «Лила»", 3))
    body += sec('<div class="lay"><div>%s</div>%s</div>' % (left, buybox("lila", [("Формат", "онлайн, вживую"), ("Длительность", "4 часа"), ("Игроков", "до 4")], "Записаться на игру")))
    body += sec(head("Узнать больше", "«Лила» в энциклопедии") + '<div class="grid g3">' + acard("igra-lila", root) + acard("kletki-lily", root) + acard("biznes-lila", root) + "</div>", "alt")
    ld = {"@context": "https://schema.org", "@type": "Service", "name": "Игра «Лила» с Мариной Степановой", "provider": {"@type": "Person", "name": "Марина Степанова"}, "offers": {"@type": "Offer", "price": re.sub(r"\D", "", pr("igra-lila")), "priceCurrency": "RUB"}}
    layout("lila/", "Игра «Лила» онлайн с Мариной Степановой", "Авторская трансформационная игра «Лила» для бизнеса и жизненных ситуаций: 4 часа, до 4 игроков, онлайн. Специальная входная цена.", body, "price", jsonld=ld, mcta=cta("lila", "Записаться · " + pr("igra-lila"), "btn sm"), crumbs=[("lila/", "Игра «Лила»")])

def klub_page():
    root = "../"
    body = hero("Подписка · закрытый Telegram-канал и чат · предзапись", "Закрытый клуб", "Регулярная работа с собой вместе с Мариной: потоковые медитации каждый понедельник, групповые «Разборы» — живая диагностика на примерах участников, карта недели и ранняя запись на тренинги.", cta("klub", "Записаться в клуб · " + pr("club")))
    left = '<div class="glass box rv"><h2>Что внутри</h2>%s</div><div class="glass box rv"><h2>Как вступить</h2>%s</div>' % (
        ticks(["Потоковые медитации — по понедельникам.", "Групповые «Разборы» — групповая диагностика, только в клубе.", "МАК-карта недели с вопросом для самостоятельной работы.", "Тема месяца из «Колеса успеха»: деньги, страхи, проявленность…", "Ранняя запись на тренинги."]),
        ticks(["Нажмите «Записаться в клуб» — откроется сообщение Марине.", "Сейчас идёт предзапись: онлайн-оплата подписки ещё не подключена, Марина пришлёт детали лично.", "Подписка ежемесячная."]))
    body += sec('<div class="lay"><div>%s</div>%s</div>' % (left, buybox("klub", [("Формат", "закрытый Telegram-канал и чат"), ("Подписка", "ежемесячная")], "Записаться в клуб")))
    body += sec(head("Попробовать бесплатно", "Подарки в духе клуба") + giftgrid(root, 4), "alt")
    layout("klub/", "Закрытый клуб Марины Степановой — подписка", "Закрытый клуб по подписке: медитации по понедельникам, групповые «Разборы», карта недели и ранняя запись на тренинги. 1 990 ₽ в месяц, предзапись.", body, "price", mcta=cta("klub", "В клуб · " + pr("club"), "btn sm"), crumbs=[("klub/", "Закрытый клуб")])

def individual():
    root = "../"
    steps = [("Запрос и история", "Вы приходите с запросом и рассказываете свою историю — так, как она есть."),
             ("Архитектура", "За историей Марина видит систему: убеждения, эмоциональные всплески, избегание и защиты, которые складываются в последовательность реакций и результатов."),
             ("Перенастройка", "Затем эту систему перенастраивают: снимают привычные шаблоны поведения и сильные эмоциональные волны."),
             ("Проживание", "Часто уже за одну сессию удаётся прожить и перепрограммировать привычную реакцию. При необходимости — короткие погружения.")]
    st = "".join('<div class="glass card rv"><span class="num">%d</span><h3>%s</h3><p class="muted">%s</p></div>' % (i, e(a), e(b)) for i, (a, b) in enumerate(steps, 1))
    body = hero("Индивидуально · 1–2 часа · онлайн", "Сессия один на один с Мариной", "Сначала — разбор вашей системы мышления как архитектуры. Затем — её перенастройка. Авторские протоколы — микс психологических, трансперсональных и трансцендентных техник, МАК-карты.", cta("individ", "Купить сессию · " + pr("individ-sessiya")) + '<a class="btn ghost" href="%sdiagnostika/">Сначала диагностика</a>' % root)
    body += sec(head("Как проходит", "От архитектуры — к перенастройке") + '<div class="grid g4">%s</div>' % st)
    body += sec(head("Стоимость", "Сессия и пакеты", "В пакетах и для тех, кто уже был у Марины, — 7 000 ₽ за сессию.") + '<div class="grid g4">' + "".join(prodcard(k, root) for k in ("individ", "individ3", "individ5", "individ-povtor")) + '</div><p class="small muted" data-save="pkg" data-n="5" data-code="individ-paket5"></p>', "alt")
    body += sec('<div class="glass box rv"><h2>Важно</h2><p>Это психологическая работа с запросом. Она не заменяет медицинскую или психиатрическую помощь. Если вы в остром состоянии — <a href="%svazhno/#help">обратитесь за срочной помощью</a>.</p></div>' % root)
    layout("individualno/", "Индивидуальная работа с Мариной Степановой", "Индивидуальная сессия 1–2 часа онлайн: разбор системы мышления как архитектуры и её перенастройка. 10 000 ₽, пакет из 3 сессий — 21 000 ₽, из 5 — 35 000 ₽.", body, "price", mcta=cta("individ", "Сессия · " + pr("individ-sessiya"), "btn sm"), crumbs=[("individualno/", "Индивидуально")])

def diagnostics():
    root = "../"
    body = hero("Лично · 1 на 1 · 30 минут · онлайн", "Личная диагностика", "За каждой повторяющейся ситуацией стоит система: убеждения, эмоциональные всплески, избегание и защиты. За 30 минут один на один вы увидите, что стоит за вашей историей, и поймёте, какой шаг нужен дальше.", cta("diag", "Записаться · " + pr("diagnostika")))
    left = '<div class="glass box rv"><h2>Это для вас, если</h2>%s</div><div class="glass box rv"><h2>Что вы получите</h2>%s</div>' % (ticks(["Ситуация повторяется, а вы не понимаете, что её запускает.", "Хочется изменений, но непонятно, с чего начать.", "Вы выбираете между сессией, тренингом и модулем."], "q"), ticks(["Ясность: что на самом деле стоит за вашей ситуацией.", "Рекомендацию формата: сессия, тренинг, модуль или клуб.", "Зачёт стоимости диагностики при покупке следующего шага."]))
    body += sec('<div class="lay"><div>%s<p class="small muted">Групповые «Разборы» проходят только в <a href="%sklub/">закрытом клубе</a>.</p></div>%s</div>' % (left, root, buybox("diag", [("Формат", "лично, 1 на 1, онлайн"), ("Длительность", "30 минут")], "Записаться на диагностику")))
    body += sec(head("Перед диагностикой", "Пройдите тест — принесите результат") + '<div class="grid g4">' + "".join(tcard(s, root) for s in ("tormoza", "samozvanec", "dengi", "koleso")) + "</div>", "alt")
    layout("diagnostika/", "Личная диагностика 30 минут", "Полная индивидуальная диагностика по запросу: лично, 1 на 1, 30 минут онлайн, 1 000 ₽. Стоимость засчитывается при покупке тренинга, модуля или сессий.", body, "price", mcta=cta("diag", "Диагностика · " + pr("diagnostika"), "btn sm"), crumbs=[("diagnostika/", "Диагностика")])

def marathons():
    for key, slug, title, lead, items, rows, tp in [
        ("marafon:samoprinyatie", "samoprinyatie", "Марафон «Самопринятие»", "5 недель мягкой трансформации в поддерживающем кругу. Это не про «стать лучше». Это про — стать собой.",
         ["Умение останавливаться и слышать себя.", "Навык быть поддержкой себе без зависимости от чужого мнения.", "Спокойствие: не спасать всех, не додумывать за других.", "Принятие своей неидеальности как силы.", "6 живых эфиров (остаются в записи), чат поддержки, еженедельные задания."], [("Формат", "эфиры + чат"), ("Длительность", "5 недель")], "samoocenka"),
        ("marafon:dvizhenie", "dvizhenie-k-celi", "Марафон «Движение к цели»", "Не про волшебные пендели, а про реальное движение. 8 шагов и 14 дней, чтобы встроить навык идти к своему.",
         ["Найдём настоящую цель — не навязанную, а живую.", "Разложим её на понятные шаги.", "Отследим, что мешает — внутренне и внешне.", "Создадим устойчивый фокус и лёгкий темп без самоедства.", "Telegram + 3 живых эфира с Мариной."], [("Формат", "Telegram + 3 эфира"), ("Длительность", "14 дней")], "celi")]:
        root = "../../"
        body = hero("Марафон · онлайн", e(title), e(lead), cta(key, "Записаться · " + pr(PROD[key]["code"])))
        body += sec('<div class="lay"><div><div class="glass box rv"><h2>Что вас ждёт</h2>%s</div></div>%s</div>' % (ticks(items), buybox(key, rows)))
        body += learn_block([tp], root)
        layout("marafon/%s/" % slug, title, lead, body, "price", mcta=cta(key, "Записаться · " + pr(PROD[key]["code"]), "btn sm"), crumbs=[("ceny/", "Форматы"), ("marafon/%s/" % slug, title)])

def psy():
    root = "../"
    body = hero("Для психологов, коучей и экспертов", "Психологам и коучам", "Наставничество по созданию собственной трансформационной игры или программы и личная проработка профессиональных «тормозов».", cta("psy", "Обсудить проект"))
    body += sec('<div class="lay"><div><div class="glass box rv"><h2>«Архитектор продукта»</h2><p>Индивидуальное сопровождение 1–2 месяца для специалистов, которые хотят создать свой глубокий продукт.</p>%s</div><div class="glass box rv"><h2>Лист ожидания: обучение ведению Т-игр и групп с МАК</h2><p>Формат в разработке. Это не курс повышения квалификации и не программа с выдачей диплома.</p>%s</div></div>%s</div>'
                % (ticks(["Диагностика вашего продукта или идеи.", "Структура: от запроса — до механики.", "Присутствие на тестовом проведении с обратной связью.", "Рекомендации по упаковке и воронке."]), cta("psy-wait", "Встать в лист ожидания", "btn ghost"), buybox("psy", [("Формат", "индивидуально, онлайн"), ("Срок", "1–2 месяца")], "Обсудить проект")))
    body += sec(head("Личная проработка", "Тренинги, которые особенно откликаются специалистам") + '<div class="grid g3">' + "".join(prodcard("trening:" + s, root) for s in ("samozvanets-strah-razoblacheniya", "stoimost-uslugi", "kak-ozvuchivat-cenu", "samotsennost", "proyavlyajsya-legko", "moj-produkt-krutoj")) + "</div>", "alt")
    body += sec(head("Знания для практики", "Статьи, полезные специалистам") + '<div class="grid g3">' + acard("mak-karty", root) + acard("transformacionnye-igry", root) + acard("kak-nazyvat-cenu", root) + "</div>")
    layout("psihologam/", "Психологам и коучам: наставничество «Архитектор продукта»", "Наставничество для психологов и коучей по созданию своей трансформационной игры или программы. Личная проработка: самозванец, цена услуги, проявленность.", body, "price", mcta=cta("psy", "Обсудить проект", "btn sm"), crumbs=[("psihologam/", "Психологам")])

def marina_page():
    root = "../"
    body = hero("Ведущая", "Марина Степанова", "Психолог, автор и ведущая трансформационных игр и тренингов, автор программы «Колесо успеха», предприниматель с 9-летним опытом.")
    body += sec(marina_block(root))
    body += sec('<div class="grid g2"><div class="glass box rv"><h2>Как я работаю</h2><p>Человек приходит с запросом и рассказывает историю. За ней я вижу сеть: убеждения, эмоциональные всплески, убегание и избегание, защиты — и последовательность реакций, мыслей и результатов во взаимодействии с людьми.</p><p>Сначала я разбираю эту систему как архитектуру, затем перенастраиваю её: снимаем привычные паттерны и сильные эмоциональные волны. Часто это удаётся прожить и перепрограммировать за одну сессию.</p></div><div class="glass box rv"><h2>Инструменты</h2><p>Авторские протоколы, сложившиеся в практике: микс психологических, трансперсональных и трансцендентных техник, подобранный под человека и запрос.</p>%s</div></div>' % ticks(["МАК — метафорические ассоциативные карты.", "Потоковые медитации и короткие погружения.", "Трансформационные игры, в том числе авторская «Лила»."]), "alt")
    body += sec(head("Отзывы", "О работе Марины") + '<div class="grid g3">%s</div>' % (rev("bazovyj-strah", "Участница тренинга «Базовый страх»", 1, 2) + rev("samozvanets-strah-razoblacheniya", None, 1, 2) + rev("dejstvuj-kak", None, 1)))
    ld = {"@context": "https://schema.org", "@type": "Person", "name": "Марина Степанова", "jobTitle": "Психолог", "image": SITE + "assets/img/marina.jpg", "url": SITE + "marina/"}
    layout("marina/", "Марина Степанова — психолог, ведущая игр и тренингов", "Марина Степанова — психолог, автор и ведущая трансформационных игр и тренингов, автор программы «Колесо успеха». Индивидуальная работа, диагностика, группы до 8 человек.", body, "mar", jsonld=ld, crumbs=[("marina/", "Марина Степанова")])

def reviews_page():
    order = []
    for m in MODULES:
        for s in m["trainings"]:
            if s in R: order.append((s, "Тренинг «%s»" % T[s]["title"]))
    order += [("samotsennost", "Тренинг «Самоценность»"), ("modul-6", "Модуль «Квантовый скачок»")] + [("mini-" + m["slug"], "Мини-тренинг «%s»" % m["title"]) for m in MINIS if R.get("mini-" + m["slug"])] + [("igra-lila", "Игра «Лила»")]
    secs = "".join('<h2 class="rv revh">%s</h2><div class="grid g3">%s</div>' % (e(t), rev(k, "Участница", 6)) for k, t in order)
    body = hero("Отзывы", "Отзывы участников", "Настоящие отзывы участников тренингов и игр — слегка сокращены, без изменения смысла. Мы не публикуем выдуманных отзывов.") + sec(secs)
    layout("otzyvy/", "Отзывы участников тренингов и игр", "Реальные отзывы участников тренингов, мини-тренингов и игры «Лила» Марины Степановой.", body, "mar", crumbs=[("otzyvy/", "Отзывы")])

FAQ = [("Что такое Внутрикод?", "Экспериментальная площадка психолога Марины Степановой: энциклопедия, бесплатные тесты и инструменты, а также живые онлайн-сессии с Мариной."),
       ("Навигатор — это нейросеть?", "Сейчас нет: навигатор работает по заранее подготовленному сценарию прямо в браузере. Если в будущем подключится ИИ-помощник, это будет видно по метке «ИИ-помощник» в окне навигатора."),
       ("Тесты — это диагностика?", "Нет. Это авторские опросники для самонаблюдения. Они не ставят диагнозов и не заменяют консультацию специалиста."),
       ("Как проходят живые сессии?", "Онлайн и вживую с Мариной Степановой. Тренинги — в группах до 8 человек (оптимально 5), 2–3 часа. Можно отвечать голосом или в чате."),
       ("Есть ли записи тренингов?", "Нет: тренинги, мини-тренинги и игры проводятся только вживую — эффект возникает в живой работе. В марафоне «Самопринятие» эфиры остаются в записи."),
       ("С чего начать?", "С бесплатного навигатора или теста. Если хочется живого шага — с диагностики за 1 000 ₽ (засчитывается в покупку) или мини-тренинга за 1 500 ₽."),
       ("Как записаться и оплатить?", "Нажмите кнопку записи — откроется Telegram Марины (@MarinaNew) с готовым сообщением. Марина пришлёт дату и детали оплаты."),
       ("Это психотерапия?", "Нет. Это психологическая и трансформационная работа. Она не заменяет медицинскую или психиатрическую помощь."),
       ("Где хранится мой прогресс?", "Только в вашем браузере (localStorage). Сайт не собирает имена, почты и ответы тестов.")]
def faq_page():
    body = hero("Вопросы", "Частые вопросы", "") + sec("".join('<details class="glass rv"><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in FAQ))
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    layout("faq/", "Вопросы и ответы", "Как работают навигатор и тесты, как проходят живые сессии с Мариной Степановой, как записаться и где хранится прогресс.", body, "", jsonld=ld, crumbs=[("faq/", "Вопросы")])

def vazhno():
    body = hero("Важно", "Не замена медицинской помощи", "Материалы Внутрикода — просветительские. Тесты — инструменты самонаблюдения. Живые сессии — психологическая работа с запросом, а не лечение.")
    body += sec('''<div class="glass box rv" id="help"><h2>Если вам сейчас очень плохо</h2><p>Если есть мысли причинить себе вред или вы в опасности — не оставайтесь с этим в одиночку:</p>
<ul class="ticks"><li><b>112</b> — единый номер экстренных служб.</li>
<li><b>+7 (495) 989-50-50</b> — экстренная психологическая помощь МЧС России: круглосуточно, анонимно (оплачивается только междугородняя связь).</li>
<li><b>8-800-2000-122</b> (или <b>124</b> с мобильного) — детский телефон доверия для детей, подростков и их родителей, бесплатно.</li>
<li><b>051</b> с городского телефона в Москве или <b>+7 (495) 051</b> с мобильного — Московская служба психологической помощи населению.</li></ul>
<p class="small muted">Номера сверены с сайтами МЧС России (psi.mchs.gov.ru) и Фонда поддержки детей (fond-detyam.ru) в октябре 2026 года.</p></div>
<div class="glass box rv"><h2>Что мы делаем и чего не делаем</h2><ul class="ticks"><li>Не ставим диагнозов и не лечим.</li><li>Не обещаем гарантированного роста дохода или «чудес».</li><li>Не используем выдуманные отзывы и статистику.</li><li>Навигатор по умолчанию — сценарный помощник; если подключён ИИ, это отмечено в окне.</li><li>«Лила» и трансперсональные практики — культурные и духовные традиции; мы используем их как метафоры для самоисследования.</li></ul></div>''')
    layout("vazhno/", "Важно: не замена медицинской помощи", "Внутрикод не заменяет медицинскую и психиатрическую помощь. Телефоны экстренной психологической помощи в России.", body, "", crumbs=[("vazhno/", "Важно")])

def privacy():
    body = hero("Конфиденциальность", "Ваши данные остаются у вас", "") + sec('''<div class="glass box rv"><ul class="ticks"><li>Прогресс, ответы тестов, заметки к карте дня и маршрут навигатора хранятся только в localStorage вашего браузера.</li>
<li>Чтобы удалить всё, откройте «Мой путь» и нажмите «Сбросить прогресс» или очистите данные сайта в браузере.</li>
<li>Если в ссылке есть UTM-метки (например, из ролика), они запоминаются в браузере и добавляются в текст сообщения Марине, чтобы она знала, откуда вы пришли. Вы видите этот текст перед отправкой.</li>
<li>Сообщение Марине вы отправляете сами в Telegram — сайт его не отправляет.</li>
<li>Если владелец подключит ИИ-помощника, то текст, который вы сами напишете в окне навигатора, будет отправлен на сервер помощника для ответа. Окно навигатора в этом случае помечено «ИИ-помощник». Не пишите туда персональные данные.</li>
<li>Если владелец подключит Яндекс.Метрику, она будет собирать обезличенную статистику посещений по правилам Яндекса.</li></ul></div>''')
    layout("konfidencialnost/", "Конфиденциальность", "Внутрикод не собирает персональные данные: прогресс и ответы тестов хранятся только в вашем браузере.", body, "", crumbs=[("konfidencialnost/", "Конфиденциальность")])

def notfound():
    body = hero("404", "Такой страницы нет", "Зато есть навигатор, который подберёт маршрут.", '<a class="btn" href="%snavigator/">Навигатор</a><a class="btn ghost" href="%sznaniya/">Энциклопедия</a>' % (BASE, BASE))
    layout("404.html", "Страница не найдена", "Страница не найдена.", body)

def catalog_js():
    prods = {k: dict(t=p["t"], u=p["u"], code=p["code"], g=p["g"], head=p["head"], tail=p["tail"], k=p["k"], s=p["s"], np=p["np"]) for k, p in PROD.items()}
    arts = {s: dict(t=a["title"], c=CAT[a["cat"]], d=a["desc"]) for s, a in ARTICLES.items()}
    data = dict(prods=prods, arts=arts, tests=TESTS, scale=SCALE, themes={k: {kk: vv for kk, vv in v.items()} for k, v in NAV_THEMES.items()},
                lila=dict(cells=LILA_CELLS, jumps={str(k): v for k, v in LILA_JUMPS.items()}), card=dict(q=CARD_PROMPTS, w=CARD_WORDS),
                challenge=[[n, t, u] for n, t, d, u, a in CHALLENGE], gifts=[[u, i, t] for u, i, t, d in GIFTS], nArts=len(ARTICLES))
    open(os.path.join(OUT, "assets/catalog.js"), "w", encoding="utf-8").write("/* Сгенерировано _src/gen.py — не редактируйте вручную */\nwindow.VK=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")

if __name__ == "__main__":
    for s, a in ARTICLES.items():
        for r in a["related"]: assert r in ARTICLES, (s, r)
        assert a["cta"] in PROD, (s, a["cta"]); assert a["test"] in TESTD, (s, a["test"])
    for t in TESTS:
        for k in [t["step"], t["deep"]] + [v[3] for v in t.get("results", {}).values()] + [x[2] for x in t.get("spheres", [])]: assert k in PROD, (t["slug"], k)
        for s in t["articles"] + [x for v in t.get("results", {}).values() for x in v[2]]: assert s in ARTICLES, (t["slug"], s)
    for k, th in NAV_THEMES.items():
        for x in (th["mini"], th["deep"], th["module"]): assert x in PROD, (k, x)
        for s in th["articles"]: assert s in ARTICLES, (k, s)
    home(); navigator_page(); enc_index()
    for s in ARTICLES: article(s)
    tests_index()
    for t in TESTS: test_page(t)
    gifts(); card_day(); mini_lila(); breath(); challenge(); checklists(); my_path()
    prices_page()
    for m in MINIS: mini_page(m)
    for s in T: training_page(s)
    for m in MODULES: module_page(m)
    flagship(); lila_page(); klub_page(); individual(); diagnostics(); marathons(); psy(); marina_page(); reviews_page(); faq_page(); vazhno(); privacy(); notfound()
    catalog_js()
    urls = "".join("<url><loc>%s%s</loc></url>" % (SITE, p) for p, _ in PAGES if not p.endswith(".html"))
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>' % urls)
    open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n" % SITE)
    print(len(PAGES), "pages,", len(ARTICLES), "articles,", len(TESTS), "tests")
