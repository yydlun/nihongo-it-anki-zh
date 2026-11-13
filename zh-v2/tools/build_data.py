#!/usr/bin/env python3
"""Build zh-v2/data/cards.json from the it-vocab tier CSVs plus the
Chinese gloss dictionaries (cloze_zh.json / kata_dict.json / cloze_pos.json
in zh-v2/data/). Run locally; the output cards.json is committed and is
the single source the deck build + audio generation consume.
Each card: {id, Sentence, Cloze, Pronunciation, PitchAccent, KeyMeaning,
Note, Register, Translation, TranslationZh, vocab: [{word, reading_html,
pos, en, zh}]} where vocab[0] is the key phrase and the rest are the
katakana loanwords appearing in the sentence.
"""
import csv
import glob
import html
import json
import os
import re

from janome.tokenizer import Tokenizer

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(BASE)
DATA = os.path.join(BASE, "data")
KATA_RE = re.compile(r"[ァ-ヶー]{2,}")
POS_OVERRIDES = {"必要": "形容词"}

tk = Tokenizer()
cloze_zh = json.load(open(os.path.join(DATA, "cloze_zh.json"), encoding="utf-8"))
kata_dict = json.load(open(os.path.join(DATA, "kata_dict.json"), encoding="utf-8"))
cloze_pos = json.load(open(os.path.join(DATA, "cloze_pos.json"), encoding="utf-8"))


def to_hira(s):
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)


def janome_reading(s):
    return to_hira("".join(t.reading or t.surface for t in tk.tokenize(s)))


def key_pos(cloze):
    if "かもしれません" in cloze:
        return "短语"
    return POS_OVERRIDES.get(cloze, cloze_pos.get(cloze, "名词"))


def main():
    cards = []
    cid = 0
    for path in sorted(glob.glob(os.path.join(REPO, "decks", "it-vocab", "tier*-vocabulary.csv")),
                       key=lambda p: int(re.search(r"tier(\d+)", p).group(1))):
        for row in csv.DictReader(open(path, encoding="utf-8")):
            cid += 1
            cloze = row["Cloze"]
            m = re.search(r"<rt>(.*?)</rt>", row["PitchAccent"])
            reading_html = m.group(1) if m else html.escape(janome_reading(cloze))
            vocab = [{"word": cloze, "reading_html": reading_html,
                      "pos": key_pos(cloze), "en": row["KeyMeaning"],
                      "zh": cloze_zh.get(cloze, "")}]
            seen = set()
            for w in KATA_RE.findall(row["Sentence"]):
                if w in seen or w not in kata_dict:
                    continue
                seen.add(w)
                if w == cloze or cloze.startswith(w) or w in cloze:
                    continue
                d = kata_dict[w]
                vocab.append({"word": w, "reading_html": html.escape(to_hira(w)),
                              "pos": "名词", "en": d["en"], "zh": d["zh"]})
            cards.append({
                "id": cid, "Sentence": row["Sentence"], "Cloze": cloze,
                "Pronunciation": row["Pronunciation"],
                "PitchAccent": row["PitchAccent"], "KeyMeaning": row["KeyMeaning"],
                "Note": row["Note"], "Register": row["Register"],
                "Translation": row["Translation"], "TranslationZh": row["TranslationZh"],
                "vocab": vocab,
            })
    json.dump(cards, open(os.path.join(DATA, "cards.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    no_zh = [c["id"] for c in cards if not c["vocab"][0]["zh"]]
    print(f"cards: {len(cards)} | key entries missing zh: {len(no_zh)} {no_zh[:10]}")


if __name__ == "__main__":
    main()
