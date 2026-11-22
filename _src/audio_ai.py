# -*- coding: utf-8 -*-
"""Черновики продающих аудио-сценариев через Agnes → _src/audio_texts.json.
python3 _src/audio_ai.py [--only id1,id2] [--force]
Требует AGNES_API_KEY. Тексты проверяются автоматически; результат — исходник для audio_scripts.py.
"""
import json, os, re, sys, concurrent.futures as cf, requests
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from audio_scripts import SCRIPTS_OLD
OUTF = os.path.join(HERE, "audio_texts.json")
BANK = {t["id"]: t for t in json.load(open(os.environ.get("TOPIC_BANK", "/workspace/kod-zhizni-ai/content/topic_bank.json")))["topics"]}
SYSTEM = open(os.path.join(HERE, "audio_prompt.md"), encoding="utf-8").read()
BANNED = re.compile(r"\bАнн[аыеу]\b|Элиа|генн\w* ключ|Радд|Хологенет|Голографическ|\bКПТ\b|\bРПТ\b|\bНЛП\b|гештальт|гарант|исцел|вылеч|100\s*%|\d+\s*%|навсегда|по России|рубл|₽|тенге|ничтожеств|неудачни|лузер|тупы|последн\w+ мест|\bотзыв(?:ы|ов|ам|ами)?\b", re.I)

def check(d, src):
    t = d.get("text", ""); allt = t + " " + d.get("teaser", "")
    w = len(t.split())
    if not 140 <= w <= 300: return "слов %d" % w
    if re.search(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]|[A-Za-z]{3,}", allt): return "латиница/иероглифы"
    m = BANNED.search(allt)
    if m: return "запрещено: " + m.group(0)
    nums = set(re.findall(r"\d+", src)) | {"1", "2", "3", "4", "5", "6", "7", "8", "30"}
    bad = [x for x in re.findall(r"\d+", allt) if x not in nums]
    if bad: return "числа: " + ",".join(bad)
    if not d.get("teaser"): return "нет teaser"
    ps = [p for p in re.split(r"\n\s*\n", t) if p.strip()]
    if len(ps) < 7: return "абзацев %d" % len(ps)
    if max(len(p.split()) for p in ps) > 60: return "длинный абзац"
    if re.search(r"\b(ты|тебя|тебе|твой|твоя|твои)\b", allt, re.I): return "на ты"
    if re.search(r"расскаж", d.get("teaser", ""), re.I): return "teaser обещает"
    sh = [w for w in re.findall(r"\b\w+(?:ешь|ишь|ёшь)(?:ся)?\b", allt.lower()) if w not in ("лишь", "тишь", "мышь", "глушь", "малышь")]
    if sh: return "на ты: " + sh[0]
    return None

def gen(x):
    t = BANK[x["id"]]
    from audio_scripts import PLAN, TITLE
    nx = PLAN[x["id"]]["next"][0]
    payload = {"title": x["title"], "kind": x["kind"], "facts": t["facts"], "page_text": x["text"],
               "next_audio": {"title": TITLE[nx], "about": BANK[nx]["facts"]["hook"] if nx in BANK else ""}}
    if x["id"].startswith(("trening-", "mini-", "modul-")):
        payload["format"] = ("Онлайн, вживую, с Мариной. Работа идёт пошагово: от распознавания своего сценария — к развороту в ресурс; "
                             "используются метафорические карты, ситуацию рассматривают с разных сторон; в конце — рефлексия «было — стало», выводы и шаг, который реально сделать сейчас.")
    src = json.dumps(payload, ensure_ascii=False)
    last = None
    for a in range(6):
        try:
            r = requests.post("https://apihub.agnes-ai.com/v1/chat/completions", timeout=120,
                              headers={"Authorization": "Bearer " + os.environ["AGNES_API_KEY"]},
                              json={"model": "agnes-2.5-flash", "temperature": 0.6, "max_tokens": 2500, "messages": [
                                  {"role": "system", "content": SYSTEM}, {"role": "user", "content": "Сценарий аудио для этой страницы:\n" + src}]})
            j = r.json()
            if "choices" not in j:
                import time; last = str(j)[:120]; time.sleep(15 * (a + 1)); continue
            c = j["choices"][0]["message"]["content"]
            d = json.loads(c[c.index("{"): c.rindex("}") + 1])
            d = {k: v.replace("\u2011", "-").replace("\u00a0", " ").strip() for k, v in d.items() if k in ("text", "teaser")}
            last = check(d, src)
            if not last: return x["id"], d, None
        except Exception as ex: last = type(ex).__name__ + str(ex)[:100]
    return x["id"], None, last

if __name__ == "__main__":
    data = json.load(open(OUTF)) if os.path.exists(OUTF) else {}
    only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
    todo = [x for x in SCRIPTS_OLD if (only is None or x["id"] in only) and ("--force" in sys.argv or x["id"] not in data)]
    with cf.ThreadPoolExecutor(3) as ex:
        for i, d, err in ex.map(gen, todo):
            if d: data[i] = d; json.dump(data, open(OUTF, "w"), ensure_ascii=False, indent=1); print("ok", i, len(d["text"].split()), flush=True)
            else: print("FAIL", i, err, flush=True)
    print(len(data), "texts")
