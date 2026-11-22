# -*- coding: utf-8 -*-
"""Архитектура аудио-путешествия «Внутрикод» (фаза 1 — карта, без публикации).

Вход: start («С чего начать»). Дальше 7 тематических маршрутов:
статья (бесплатно) → тест/подарок → мини-тренинг/диагностика → тренинг/модуль → программа.
У каждого аудио: 1–2 следующих аудио (NEXT) + одна мягкая CTA (CTA).
"""
START = "start"
PATHS = {
 "dengi": ("Деньги", [
   "znaniya-dengi-scenarii", "znaniya-finansovyj-potolok", "znaniya-vyuchennaya-bespomoshchnost", "znaniya-kak-nazyvat-cenu",
   "mini-finansovyj-strah", "trening-ya-vizhu-dengi", "trening-dengi-iz-detstva", "trening-finansovyj-potolok", "trening-moya-bogataya-zhizn",
   "trening-finansovyj-strah-osvobozhdenie", "modul-1", "koleso-uspeha"]),
 "strahi": ("Страхи и тормоза", [
   "znaniya-strah-uspeha", "znaniya-bazovyj-strah", "znaniya-zona-komforta", "mini-strah-uspeha", "mini-bazovyj-strah",
   "trening-strah-uspeha", "trening-bazovyj-strah", "modul-2", "koleso-uspeha"]),
 "samozvanec": ("Самозванец и самоценность", [
   "znaniya-sindrom-samozvanca", "znaniya-vnutrennij-kritik", "znaniya-samocennost-i-samoocenka", "znaniya-perfekcionizm", "znaniya-prokrastinaciya",
   "znaniya-proyavlennost", "mini-samozvanets", "trening-samozvanets-strah-razoblacheniya", "trening-samoocenka", "trening-samotsennost",
   "trening-perfekcionizm", "trening-koroli-prokrastinacii", "trening-proyavlyajsya-legko", "trening-moj-produkt-krutoj", "trening-stoimost-uslugi",
   "trening-kak-ozvuchivat-cenu", "modul-4", "modul-5", "koleso-uspeha"]),
 "otnosheniya": ("Отношения, контроль, конфликты", [
   "znaniya-giperkontrol", "znaniya-giperotvetstvennost", "znaniya-delegirovanie", "znaniya-treugolnik-karpmana", "znaniya-konflikty",
   "znaniya-teoriya-privyazannosti", "znaniya-psihologicheskie-zashchity", "znaniya-emocionalnyj-intellekt",
   "mini-kontrol", "mini-bez-menya", "mini-istoki-konfliktov", "mini-svyaz-v-konfliktah", "diagnostika",
   "trening-vsyo-pod-kontrolem", "trening-lider-a-ne-nyanka", "trening-ne-daj-soboj-manipulirovat", "trening-konflikty-v-rost", "trening-dejstvuj-kak",
   "modul-3", "individualno"]),
 "prednaznachenie": ("Предназначение, цели, ресурс", [
   "znaniya-mechta-i-cel", "znaniya-detskie-scenarii", "znaniya-kognitivnye-iskazheniya", "znaniya-neyroplastichnost-i-privychki", "znaniya-vygoranie",
   "znaniya-meditaciya-i-vnimanie", "marafon-samoprinyatie", "marafon-dvizhenie-k-celi", "trening-vsyo-nachinaetsya-s-mechty", "trening-istinnost-celi",
   "trening-fundament-starta", "trening-konkretnye-shagi", "modul-6", "klub", "koleso-uspeha"]),
 "lila": ("Игра «Лила» и метафоры", [
   "znaniya-igra-lila", "znaniya-kletki-lily", "znaniya-biznes-lila", "znaniya-transformacionnye-igry", "znaniya-mak-karty",
   "znaniya-transpersonalnaya-psihologiya", "lila", "individualno"]),
 "psy": ("Психологам и коучам", [
   "znaniya-transformacionnye-igry", "znaniya-mak-karty", "trening-stoimost-uslugi", "trening-kak-ozvuchivat-cenu", "psihologam"]),
}
# основной маршрут для аудио, которые встречаются в нескольких
PRIMARY = {"koleso-uspeha": "samozvanec", "individualno": "otnosheniya", "znaniya-transformacionnye-igry": "lila", "znaniya-mak-karty": "lila",
           "trening-stoimost-uslugi": "samozvanec", "trening-kak-ozvuchivat-cenu": "samozvanec"}
# «боковые» рекомендации: второй вариант, куда пойти (из другой темы или ступенью выше)
SIDE = {
 "znaniya-sindrom-samozvanca": "mini-samozvanets", "znaniya-dengi-scenarii": "trening-dengi-iz-detstva", "znaniya-strah-uspeha": "znaniya-sindrom-samozvanca",
 "znaniya-giperkontrol": "mini-kontrol", "znaniya-treugolnik-karpmana": "mini-istoki-konfliktov", "znaniya-igra-lila": "lila",
 "znaniya-mechta-i-cel": "marafon-dvizhenie-k-celi", "znaniya-perfekcionizm": "trening-perfekcionizm", "znaniya-prokrastinaciya": "trening-koroli-prokrastinacii",
 "znaniya-kak-nazyvat-cenu": "trening-kak-ozvuchivat-cenu", "znaniya-vygoranie": "klub", "znaniya-meditaciya-i-vnimanie": "klub",
 "znaniya-detskie-scenarii": "znaniya-dengi-scenarii", "znaniya-bazovyj-strah": "mini-bazovyj-strah", "znaniya-giperotvetstvennost": "mini-bez-menya",
 "znaniya-konflikty": "mini-svyaz-v-konfliktah", "znaniya-teoriya-privyazannosti": "diagnostika", "znaniya-psihologicheskie-zashchity": "individualno",
 "znaniya-kognitivnye-iskazheniya": "diagnostika", "znaniya-transpersonalnaya-psihologiya": "individualno", "znaniya-mak-karty": "psihologam",
 "znaniya-transformacionnye-igry": "psihologam", "znaniya-proyavlennost": "trening-proyavlyajsya-legko", "znaniya-samocennost-i-samoocenka": "trening-samotsennost",
 "znaniya-vnutrennij-kritik": "trening-samoocenka", "znaniya-zona-komforta": "mini-strah-uspeha", "znaniya-vyuchennaya-bespomoshchnost": "trening-moya-bogataya-zhizn",
 "znaniya-finansovyj-potolok": "trening-finansovyj-potolok", "znaniya-delegirovanie": "trening-lider-a-ne-nyanka", "znaniya-emocionalnyj-intellekt": "trening-konflikty-v-rost",
 "znaniya-neyroplastichnost-i-privychki": "klub", "znaniya-kletki-lily": "lila", "znaniya-biznes-lila": "lila",
 "mini-samozvanets": "trening-samozvanets-strah-razoblacheniya", "mini-strah-uspeha": "trening-strah-uspeha", "mini-finansovyj-strah": "trening-finansovyj-strah-osvobozhdenie",
 "mini-bazovyj-strah": "trening-bazovyj-strah", "mini-kontrol": "trening-vsyo-pod-kontrolem", "mini-bez-menya": "trening-lider-a-ne-nyanka",
 "mini-istoki-konfliktov": "trening-ne-daj-soboj-manipulirovat", "mini-svyaz-v-konfliktah": "trening-konflikty-v-rost",
 "modul-1": "modul-2", "modul-2": "modul-3", "modul-3": "modul-4", "modul-4": "modul-5", "modul-5": "modul-6", "modul-6": "koleso-uspeha",
 "koleso-uspeha": "diagnostika", "lila": "klub", "klub": "lila", "individualno": "diagnostika", "diagnostika": "individualno",
 "marafon-samoprinyatie": "klub", "marafon-dvizhenie-k-celi": "trening-istinnost-celi", "psihologam": "lila",
}
# одна мягкая CTA на аудио: (тип, текст)
TEST_BY_PATH = {"dengi": ("тест «Мой денежный сценарий»", "testy/dengi/"), "strahi": ("тест «Кто жмёт на тормоза?»", "testy/tormoza/"),
                "samozvanec": ("тест «Индекс самозванца»", "testy/samozvanec/"), "otnosheniya": ("тест «Моя роль в треугольнике»", "testy/karpman/"),
                "prednaznachenie": ("тест «Колесо баланса»", "testy/koleso/"), "lila": ("бесплатная «Мини-Лила»", "mini-lila/"),
                "psy": ("раздел «Психологам»", "psihologam/")}

def path_of(i):
    if i in PRIMARY: return PRIMARY[i]
    for k, (_, lst) in PATHS.items():
        if i in lst: return k
    return None

def plan(ids):
    """{id: {path, stage, next:[..], cta}}"""
    out = {START: dict(path="start", stage="вход", next=["znaniya-sindrom-samozvanca", "znaniya-dengi-scenarii"], cta=("Навигатор: 4 вопроса — и личный маршрут", "navigator/"))}
    for i in ids:
        p = path_of(i); lst = PATHS[p][1]; k = lst.index(i)
        nxt = [lst[k + 1]] if k + 1 < len(lst) else []
        s = SIDE.get(i)
        if s and s not in nxt and s != i: nxt.append(s)
        if not nxt: nxt = ["diagnostika", "klub"]
        stage = "статья" if i.startswith("znaniya-") else "мини/диагностика" if i.startswith("mini-") or i in ("diagnostika",) else \
                "тренинг/модуль" if i.startswith(("trening-", "modul-")) else "программа/формат"
        if i.startswith("znaniya-"): cta = TEST_BY_PATH[p]
        elif i.startswith("mini-") or i == "diagnostika": cta = ("запись в Телеграме: кнопка «Записаться»", "")
        else: cta = ("сначала — личная диагностика 30 минут", "diagnostika/") if i not in ("diagnostika", "klub") else ("запись в Телеграме", "")
        out[i] = dict(path=p, stage=stage, next=nxt[:2], cta=cta)
    return out
