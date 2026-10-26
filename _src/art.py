# -*- coding: utf-8 -*-
ARTICLES = {}
CATS = [("strahi","Страхи и тормоза"),("dengi","Деньги"),("kontrol","Контроль и лидерство"),
        ("konflikty","Отношения и конфликты"),("samoocenka","Самоценность и продуктивность"),
        ("celi","Цели и рост"),("mozg","Мозг и мышление"),("igry","Игры, метафоры, смыслы")]
def A(slug, title, cat, desc, lead, body, signs, practice, related, cta, test, sources):
    ARTICLES[slug] = dict(slug=slug, title=title, cat=cat, desc=desc, lead=lead, body=body, signs=signs,
                          practice=practice, related=related, cta=cta, test=test, sources=sources)
