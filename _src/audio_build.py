# -*- coding: utf-8 -*-
"""Озвучка аудио-объяснений: python3 _src/audio_build.py [--force] [--only id1,id2]

Голос: edge-tts ru-RU-SvetlanaNeural (бесплатный нейроголос, женский). Это голос диктора,
не голос Марины. Чтобы заменить на запись Марины — положите assets/audio/<id>.mp3 и
добавьте id в assets/audio/own_voice.txt: такие файлы скрипт не перезаписывает.
Пересобираются только файлы, у которых изменился текст (хеш в manifest.json).
"""
import asyncio, hashlib, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio_scripts import SCRIPTS

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "audio")
VOICE = os.getenv("TTS_VOICE", "ru-RU-SvetlanaNeural")
RATE = os.getenv("TTS_RATE", "+5%")
MAN = os.path.join(OUT, "manifest.json")

def dur(fp):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", fp]).strip())

def chunks(text, n=700):
    import re
    parts, cur = [], ""
    for snt in re.split(r"(?<=[.!?»])\s+", text):
        if cur and len(cur) + len(snt) > n: parts.append(cur); cur = snt
        else: cur = (cur + " " + snt).strip()
    if cur: parts.append(cur)
    return parts

async def synth(text, out):
    """Короткие куски с таймаутом — edge-tts иногда «зависает» на длинных запросах."""
    import edge_tts, tempfile
    d = tempfile.mkdtemp(); files = []
    for i, c in enumerate(chunks(text)):
        f = os.path.join(d, "%03d.mp3" % i)
        for k in range(8):   # сервис периодически отвечает «No audio received» — повторяем кусок
            try:
                await asyncio.wait_for(edge_tts.Communicate(c, VOICE, rate=RATE).save(f), timeout=90)
                if os.path.getsize(f) < 2000: raise RuntimeError("empty chunk")
                break
            except Exception as ex:
                print("  chunk retry", k, type(ex).__name__, flush=True)
                if k == 7: raise
                await asyncio.sleep(2 + 2 * k)
        files.append(f)
    with open(out, "wb") as w:   # mp3-кадры edge-tts одного формата — можно склеивать побайтно
        for f in files: w.write(open(f, "rb").read())

async def one(x, sem, man, force):
    import edge_tts
    fp = os.path.join(OUT, x["id"] + ".mp3")
    h = hashlib.sha1((VOICE + RATE + x["text"]).encode()).hexdigest()[:12]
    if not force and os.path.exists(fp) and man.get(x["id"], {}).get("hash") == h: return
    async with sem:
        for attempt in range(6):
            try:
                tmp = fp + ".tmp.mp3"
                await synth(x["text"], tmp)
                # моно 24 кГц ~48 кбит/с — родной формат edge-tts; добавляем теги без перекодирования
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-c", "copy", "-metadata", "title=" + x["title"],
                                "-metadata", "artist=Внутрикод · Марина Степанова (голос диктора)", "-metadata", "album=Внутрикод: послушать объяснение", fp], check=True)
                os.remove(tmp)
                man[x["id"]] = dict(hash=h, duration=round(dur(fp), 1), bytes=os.path.getsize(fp), voice=VOICE)
                json.dump(man, open(MAN, "w"), ensure_ascii=False, indent=1)  # сохраняем по ходу
                print("ok", x["id"], man[x["id"]]["duration"], flush=True); return
            except Exception as ex:
                print("retry", x["id"], ex, flush=True); await asyncio.sleep(3 * (attempt + 1))
        raise RuntimeError("TTS failed: " + x["id"])

async def main():
    os.makedirs(OUT, exist_ok=True)
    force = "--force" in sys.argv
    only = None
    if "--only" in sys.argv: only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    man = json.load(open(MAN)) if os.path.exists(MAN) else {}
    own = set()
    ov = os.path.join(OUT, "own_voice.txt")
    if os.path.exists(ov): own = {l.strip() for l in open(ov) if l.strip() and not l.startswith("#")}
    sem = asyncio.Semaphore(int(os.getenv("TTS_PAR", "3")))
    todo = [x for x in SCRIPTS if x["id"] not in own and (only is None or x["id"] in only)]
    await asyncio.gather(*(one(x, sem, man, force) for x in todo))
    for i in own:
        fp = os.path.join(OUT, i + ".mp3")
        if os.path.exists(fp): man[i] = dict(hash="own", duration=round(dur(fp), 1), bytes=os.path.getsize(fp), voice="own")
    ids = {x["id"] for x in SCRIPTS}
    man = {k: v for k, v in sorted(man.items()) if k in ids}
    json.dump(man, open(MAN, "w"), ensure_ascii=False, indent=1)
    print(len(man), "files,", round(sum(v["bytes"] for v in man.values()) / 1e6, 1), "MB,", round(sum(v["duration"] for v in man.values()) / 60, 1), "min")

asyncio.run(main())
