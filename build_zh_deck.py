#!/usr/bin/env python3
"""Build the Chinese edition of the it-vocab deck.

Standalone companion to scripts/create_deck.py: reads the fifteen
decks/it-vocab/tier{N}-vocabulary.csv files (which carry a TranslationZh
column in this fork) and writes build-zh/it-vocab-zh.apkg.

It deliberately does NOT reuse the production nine-field model from
scripts/create_deck.py / deck.toml: that model is pinned because changing
it would reset existing users' review history. This script defines its
own model with its own fixed IDs, so the Chinese deck imports as a
separate deck and never collides with the original.

Usage:
    python3 build_zh_deck.py
"""

import csv
from pathlib import Path

import genanki

ROOT = Path(__file__).parent
DECK_DIR = ROOT / "decks" / "it-vocab"
OUTPUT_PATH = ROOT / "build-zh" / "it-vocab-zh.apkg"

# Fixed IDs for the Chinese edition only (NOT the ids in deck.toml).
MODEL_ID = 1593827164
DECK_ID = 2048173659
DECK_NAME = "Japanese IT Vocabulary (中文版)"

FIELDS = [
    {"name": "Sentence"},
    {"name": "Pronunciation"},
    {"name": "TranslationZh"},
    {"name": "Translation"},
    {"name": "KeyMeaning"},
    {"name": "Note"},
    {"name": "Register"},
]

CSS = """
.card {
  font-family: "Hiragino Sans", "Noto Sans CJK SC", sans-serif;
  font-size: 20px;
  text-align: left;
  color: #222;
  background: #fff;
  padding: 16px;
}
.sentence { font-size: 26px; line-height: 1.5; }
.pron { color: #666; font-size: 17px; margin-top: 6px; }
.zh {
  font-size: 24px;
  font-weight: 600;
  line-height: 1.5;
  margin: 10px 0 6px;
}
.en { color: #444; font-size: 19px; margin: 4px 0; }
.key { color: #0b5394; margin: 8px 0 2px; }
.note { color: #777; font-size: 16px; margin-top: 8px; }
.register {
  display: inline-block;
  font-size: 13px;
  color: #888;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 0 8px;
  margin-left: 8px;
  vertical-align: middle;
}
"""

MODEL = genanki.Model(
    MODEL_ID,
    "Japanese IT Vocabulary (中文版) Model",
    fields=FIELDS,
    templates=[
        {
            "name": "Chinese Card",
            "qfmt": '<div class="sentence">{{Sentence}}</div>',
            "afmt": (
                '<div class="sentence">{{Sentence}}</div>'
                '<div class="pron">{{Pronunciation}}</div>'
                "<hr>"
                '<div class="zh">{{TranslationZh}}</div>'
                '<div class="en">{{Translation}}</div>'
                '<div class="key">{{KeyMeaning}}</div>'
                '<div class="note">{{Note}}'
                '<span class="register">{{Register}}</span></div>'
            ),
        }
    ],
    css=CSS,
)


def main() -> None:
    deck = genanki.Deck(DECK_ID, DECK_NAME)
    count = 0
    for tier in range(1, 16):
        csv_path = DECK_DIR / f"tier{tier}-vocabulary.csv"
        with open(csv_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                zh = (row.get("TranslationZh") or "").strip()
                if not zh:
                    raise SystemExit(f"{csv_path.name}: empty TranslationZh for {row['Sentence']!r}")
                note = genanki.Note(
                    model=MODEL,
                    fields=[
                        row["Sentence"],
                        row["Pronunciation"],
                        row["TranslationZh"],
                        row["Translation"],
                        row["KeyMeaning"],
                        row["Note"],
                        row["Register"],
                    ],
                    guid=genanki.guid_for("it-vocab-zh", row["Sentence"]),
                )
                deck.add_note(note)
                count += 1
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(deck).write_to_file(OUTPUT_PATH)
    print(f"Wrote {OUTPUT_PATH} with {count} notes")


if __name__ == "__main__":
    main()
