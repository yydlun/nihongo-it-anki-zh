#!/usr/bin/env python3
"""用 Edge TTS 为 zh-v2/data/cards.json 的每张卡生成整句发音
（media/<id>_sent.mp3，断点续跑：已存在的非空文件跳过）。
音色 ja-JP-NanamiNeural。本地沙箱连不上 Edge TTS，主要在 GitHub
Actions 里跑（.github/workflows/zh-v2-audio.yml）。
"""
import asyncio
import json
import os

import edge_tts

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA = os.path.join(BASE, "media")
VOICE = "ja-JP-NanamiNeural"
SEM = asyncio.Semaphore(6)


async def synth(text, path):
    await edge_tts.Communicate(text, VOICE).save(path)


async def worker(card, results):
    fname = f"{card['id']}_sent.mp3"
    path = os.path.join(MEDIA, fname)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        results["skip"] += 1
        return
    async with SEM:
        last = None
        for attempt in range(3):
            try:
                await asyncio.wait_for(synth(card["Sentence"], path), timeout=60)
                if os.path.getsize(path) > 0:
                    results["ok"] += 1
                    return
                last = "empty file"
            except Exception as e:  # noqa: BLE001
                last = f"{type(e).__name__}: {e}"
            await asyncio.sleep(2 * (attempt + 1))
        results["fail"].append({"id": card["id"], "error": last})


async def main():
    os.makedirs(MEDIA, exist_ok=True)
    cards = json.load(open(os.path.join(BASE, "data", "cards.json"), encoding="utf-8"))
    results = {"ok": 0, "skip": 0, "fail": []}
    await asyncio.gather(*(worker(c, results) for c in cards))
    print(f"audio: ok={results['ok']} skip={results['skip']} fail={len(results['fail'])}")
    if results["fail"]:
        print(results["fail"][:10])


if __name__ == "__main__":
    asyncio.run(main())
