#!/usr/bin/env python3
"""20-card sample: nihongo-it (it-vocab) data in the native-nihongo UI.
Same visual system (cream/dark card, furigana ruby, orange highlight on
the key phrase, tags, house sizes), adapted to sentence cards:
front = the sentence (+ audio), back = furigana sentence with the key
phrase highlighted, the key phrase with the deck's own pitch-accent
markup, Chinese translation as the core meaning, English below, tags.
Audio: Google Translate TTS (local sandbox cannot reach Edge TTS).
.sec-h { display: flex; align-items: center; gap: 6px; font-size: 13px;
  font-weight: 700; letter-spacing: .08em; color: #2563eb; margin: 18px 0 8px; }
.sec-h:first-child { margin-top: 0; }
.nightMode .sec-h { color: #72bceb; }
.ic { width: 15px; height: 15px; flex: none; }
.zhbox { background: rgba(90, 75, 50, 0.05); border: 1px solid rgba(90, 75, 50, 0.12);
  border-radius: 14px; padding: 12px 14px; margin-top: 18px;
  box-shadow: 0 1px 3px rgba(60, 45, 20, 0.08); }
.nightMode .zhbox { background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.09); box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25); }
.zhbox .sec-h { margin: 0 0 6px; }
.meaning { font-size: 24px; font-weight: 700; margin-top: 14px; line-height: 1.45; }
.t-cat { background: rgba(37, 99, 235, 0.10); color: #1d4ed8; }
.nightMode .t-cat { background: rgba(114, 188, 235, 0.16); color: #9fd3f5; }
.t-reg { background: rgba(124, 58, 237, 0.08); color: #6d28d9; }
.nightMode .t-reg { background: rgba(190, 164, 235, 0.16); color: #d3bdf5; }
.vocab { margin-top: 2px; }
.vocab-row { padding: 9px 0 10px; border-bottom: 1px solid rgba(120, 105, 80, 0.18); }
.nightMode .vocab-row { border-bottom-color: rgba(255, 255, 255, 0.09); }
.vocab-row:last-child { border-bottom: none; }
.v-word { font-size: 18px; font-weight: 700; color: #33529e; }
.nightMode .v-word { color: #72bceb; }
.v-read { font-size: 13px; color: #8a7f6d; margin-left: 7px; }
.nightMode .v-read { color: #a99f90; }
.v-line2 { margin-top: 3px; }
.v-pos { font-size: 10.5px; color: #6f6154; background: rgba(90, 75, 50, 0.10);
  border-radius: 999px; padding: 1px 7px; line-height: 1.6; }
.nightMode .v-pos { color: #a99f90; background: rgba(255, 255, 255, 0.10); }
.v-en { font-size: 15px; color: #6f6154; margin-left: 7px; }
.nightMode .v-en { color: #beb4a4; }
.v-zh { font-size: 16.5px; margin-top: 3px; }

"""
import csv
import json
import html
import os
import re
import time

import genanki

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data", "cards.json")
MEDIA = os.path.join(ROOT, "media")
MODEL_ID = 1738092461
DECK_ID = 2048691741

CSS = """
.card { font-family: "Hiragino Sans", "Noto Sans CJK SC", sans-serif; font-size: 19px;
  text-align: left; color: #2a251d; background: #faf7f0; line-height: 1.55;
  padding: 14px 14px calc(96px + env(safe-area-inset-bottom, 0px)); }
.nightMode.card, .night-mode .card, .night_mode.card { background: #20201e; color: #eae5dc; }
.front-sent { font-size: 26px; font-weight: 600; line-height: 1.7; }
.sent-wrap { position: relative; padding-right: 46px; }
.divider { border-top: 1px solid rgba(120, 105, 80, 0.25); margin: 18px 0 4px; }
.nightMode .divider { border-top-color: rgba(255, 255, 255, 0.14); }
.box { background: rgba(90, 75, 50, 0.06); border-radius: 12px;
  padding: 10px 12px; margin-top: 14px; }
.nightMode .box { background: rgba(255, 255, 255, 0.055); }
.sent { font-size: 21px; line-height: 2.1; }
ruby rt { font-size: 10.5px; color: #8a7f6d; }
.nightMode ruby rt { color: #a99f90; }
.hl { color: #c2540a; font-weight: 700; }
.nightMode .hl { color: #e58a48; }
.key { }

.key .vocab { font-size: 20px; font-weight: 700; color: #1f6f5c; }
.nightMode .key .vocab { color: #73bba5; }
.key .vocab rt { font-size: 12px; }
.pitch-h { border-top: 2px solid #c2540a; padding-top: 1px; }
.nightMode .pitch-h { border-top-color: #e58a48; }
.keymean { font-size: 16px; color: #6f6154; margin-left: 8px; }
.nightMode .keymean { color: #beb4a4; }
.zh { font-size: 24px; font-weight: 700; margin-top: 14px; line-height: 1.45; }
.en { font-size: 15px; color: #857761; margin-top: 6px; }
.nightMode .en { color: #a99f90; }
.utags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 14px; }
.utag { font-size: 12px; color: #5d5342; background: rgba(90, 75, 50, 0.10); border: none;
  border-radius: 999px; padding: 2px 10px; line-height: 1.7; }
.nightMode .utag { color: #cfc6b4; background: rgba(255, 255, 255, 0.10); }
.replay-button { display: inline-flex; align-items: center; justify-content: center;
  width: 38px; height: 38px; border-radius: 50%; border: none;
  background-color: rgba(90, 75, 50, 0.08);
  background-image: url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20viewBox%3D%270%200%2024%2024%27%3E%3Cpath%20fill%3D%27%23c2540a%27%20d%3D%27M3%209.2v5.6c0%20.6.4%201%201%201h3.4L12%2019.6c.5.4%201.3.1%201.3-.6V5c0-.7-.8-1-1.3-.6L7.4%208.2H4c-.6%200-1%20.4-1%201z%27%2F%3E%3Cpath%20fill%3D%27none%27%20stroke%3D%27%23c2540a%27%20stroke-width%3D%271.8%27%20stroke-linecap%3D%27round%27%20d%3D%27M15.6%209.2a4%204%200%200%201%200%205.6%27%2F%3E%3Cpath%20fill%3D%27none%27%20stroke%3D%27%23c2540a%27%20stroke-width%3D%271.8%27%20stroke-linecap%3D%27round%27%20d%3D%27M18%206.8a7.4%207.4%200%200%201%200%2010.4%27%2F%3E%3C%2Fsvg%3E");
  background-repeat: no-repeat; background-position: center; background-size: 19px 19px;
  box-shadow: 0 2px 8px rgba(90, 75, 50, 0.12); }
.nightMode .replay-button { background-color: rgba(255, 255, 255, 0.10);
  background-image: url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20viewBox%3D%270%200%2024%2024%27%3E%3Cpath%20fill%3D%27%23f5ede0%27%20d%3D%27M3%209.2v5.6c0%20.6.4%201%201%201h3.4L12%2019.6c.5.4%201.3.1%201.3-.6V5c0-.7-.8-1-1.3-.6L7.4%208.2H4c-.6%200-1%20.4-1%201z%27%2F%3E%3Cpath%20fill%3D%27none%27%20stroke%3D%27%23f5ede0%27%20stroke-width%3D%271.8%27%20stroke-linecap%3D%27round%27%20d%3D%27M15.6%209.2a4%204%200%200%201%200%205.6%27%2F%3E%3Cpath%20fill%3D%27none%27%20stroke%3D%27%23f5ede0%27%20stroke-width%3D%271.8%27%20stroke-linecap%3D%27round%27%20d%3D%27M18%206.8a7.4%207.4%200%200%201%200%2010.4%27%2F%3E%3C%2Fsvg%3E");
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25); }
.replay-button:active { transform: scale(0.93); }
.replay-button svg { display: none; }
.kata { }
.kata-h { font-size: 13px; color: #8a7f6d; margin-bottom: 4px; }
.nightMode .kata-h { color: #a99f90; }
.kata-row { font-size: 16px; margin: 3px 0; }
.kata-w { font-weight: 700; color: #33529e; }
.nightMode .kata-w { color: #72bceb; }
.kata-en { margin-left: 8px; }
.kata-zh { color: #6f6154; margin-left: 8px; }
.nightMode .kata-zh { color: #beb4a4; }
.audio { position: absolute; top: 2px; right: 0; }

.sec-h { display: flex; align-items: center; gap: 6px; font-size: 13px;
  font-weight: 700; letter-spacing: .08em; color: #2563eb; margin: 18px 0 8px; }
.sec-h:first-child { margin-top: 0; }
.nightMode .sec-h { color: #72bceb; }
.ic { width: 15px; height: 15px; flex: none; }
.zhbox { background: rgba(90, 75, 50, 0.05); border: 1px solid rgba(90, 75, 50, 0.12);
  border-radius: 14px; padding: 12px 14px; margin-top: 18px;
  box-shadow: 0 1px 3px rgba(60, 45, 20, 0.08); }
.nightMode .zhbox { background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.09); box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25); }
.zhbox .sec-h { margin: 0 0 6px; }
.meaning { font-size: 24px; font-weight: 700; margin-top: 14px; line-height: 1.45; }
.t-cat { background: rgba(37, 99, 235, 0.10); color: #1d4ed8; }
.nightMode .t-cat { background: rgba(114, 188, 235, 0.16); color: #9fd3f5; }
.t-reg { background: rgba(124, 58, 237, 0.08); color: #6d28d9; }
.nightMode .t-reg { background: rgba(190, 164, 235, 0.16); color: #d3bdf5; }
.vocab { margin-top: 2px; }
.vocab-row { padding: 9px 0 10px; border-bottom: 1px solid rgba(120, 105, 80, 0.18); }
.nightMode .vocab-row { border-bottom-color: rgba(255, 255, 255, 0.09); }
.vocab-row:last-child { border-bottom: none; }
.v-word { font-size: 18px; font-weight: 700; color: #33529e; }
.nightMode .v-word { color: #72bceb; }
.v-read { font-size: 13px; color: #8a7f6d; margin-left: 7px; }
.nightMode .v-read { color: #a99f90; }
.v-line2 { margin-top: 3px; }
.v-pos { font-size: 10.5px; color: #6f6154; background: rgba(90, 75, 50, 0.10);
  border-radius: 999px; padding: 1px 7px; line-height: 1.6; }
.nightMode .v-pos { color: #a99f90; background: rgba(255, 255, 255, 0.10); }
.v-en { font-size: 15px; color: #6f6154; margin-left: 7px; }
.nightMode .v-en { color: #beb4a4; }
.v-zh { font-size: 16.5px; margin-top: 3px; }

"""

ANN = re.compile(r"([^【]+)【([^】]+)】")
KATA_RE = re.compile(r"[ァ-ヶー]{2,}")
# katakana loanword -> (English original, Chinese meaning in IT context)
KATA_DICT = {
    "アクセス": ("access", "访问"),
    "コード": ("code", "代码"),
    "ステージングデータベース": ("staging database", "预发布（staging）数据库"),
    "ステータス": ("status", "状态"),
    "チケット": ("ticket", "工单、任务单"),
    "チーム": ("team", "团队"),
    "チームリード": ("team lead", "团队负责人"),
    "バグ": ("bug", "程序缺陷、bug"),
    "ファイル": ("file", "文件"),
    "フロー": ("flow", "流程"),
    "ブロック": ("block / blocked", "阻塞、卡住"),
    "モバイル": ("mobile", "移动端"),
    "レビュー": ("review", "评审、审查"),
    "ログイン": ("login", "登录"),
}

def kata_html(sentence):
    seen, out = set(), []
    for w in KATA_RE.findall(sentence):
        if w in seen or w not in KATA_DICT:
            continue
        seen.add(w)
        en, zh = KATA_DICT[w]
        out.append(f'<div class="kata-row"><span class="kata-w">{html.escape(w)}</span>'
                   f'<span class="kata-en">{html.escape(en)}</span>'
                   f'<span class="kata-zh">{html.escape(zh)}</span></div>')
    return "".join(out)

KANJI = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf々]")

def parse_pron(pron):
    """Pronunciation -> [(surface, reading-or-None)] tokens.
    The source data glues preceding unannotated text into each annotated
    chunk (e.g. は完了【かんりょう】); the reading belongs to the trailing
    kanji run of the chunk, so split the chunk at its last kanji run."""
    toks, pos = [], 0
    for m in ANN.finditer(pron):
        if m.start() > pos:
            toks.append((pron[pos:m.start()], None))
        surf, read = m.group(1), m.group(2)
        idx = None
        for i, ch in enumerate(surf):
            if KANJI.match(ch):
                idx = i
        if idx is None:
            toks.append((surf, read))
        else:
            # annotated word = from the START of the kanji run containing
            # the last kanji (plus its okurigana tail) to the chunk end
            start = idx
            while start > 0 and KANJI.match(surf[start - 1]):
                start -= 1
            if start > 0:
                toks.append((surf[:start], None))
            toks.append((surf[start:], read))
        pos = m.end()
    if pos < len(pron):
        toks.append((pron[pos:], None))
    return toks

def ruby_html(toks, cloze_span=None):
    out, plain = [], 0
    for surf, read in toks:
        seg = (f"<ruby>{html.escape(surf)}<rt>{html.escape(read)}</rt></ruby>"
               if read else html.escape(surf))
        if cloze_span and cloze_span[0] <= plain and plain + len(surf) <= cloze_span[1]:
            seg = f'<span class="hl">{seg}</span>'
        out.append(seg)
        plain += len(surf)
    return "".join(out)

ICON_Q = ('<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
          '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>')
ICON_T = ('<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
          '<path d="M4 5h9"/><path d="M8.5 3v2c0 3.8-2 7-4.5 9"/>'
          '<path d="M5.5 8.5c1.2 2.6 3.4 4.8 6 6"/>'
          '<path d="M12.5 21l4.3-9.5L21 21"/><path d="M14.3 17.5h5"/></svg>')
ICON_B = ('<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
          '<path d="M2 4h6a4 4 0 0 1 4 4v12a3 3 0 0 0-3-3H2z"/>'
          '<path d="M22 4h-6a4 4 0 0 0-4 4v12a3 3 0 0 1 3-3h7z"/></svg>')

def vocab_row(word_html, read_html, pos, en, zh):
    return (f'<div class="vocab-row"><div class="v-line1">'
            f'<span class="v-word">{word_html}</span>'
            f'<span class="v-read">{read_html}</span></div>'
            f'<div class="v-line2"><span class="v-pos">{html.escape(pos)}</span>'
            f'<span class="v-en">{html.escape(en)}</span></div>'
            f'<div class="v-zh">{html.escape(zh)}</div></div>')

def vocab_html(card):
    out = []
    for v in card["vocab"]:
        out.append(vocab_row(html.escape(v["word"]), v["reading_html"],
                             v["pos"], v["en"], v["zh"]))
    return "".join(out)

def main():
    with open(DATA, encoding="utf-8") as f:
        cards = json.load(f)
    model = genanki.Model(
        MODEL_ID, "Japanese IT Vocabulary (zh-v2 UI)",
        fields=[{"name": n} for n in
                ["Sentence", "SentenceHtml", "VocabHtml",
                 "TranslationZh", "Translation", "Note", "Register", "Audio"]],
        templates=[{
            "name": "Sentence",
            "qfmt": ('<div class="sec-h">' + ICON_Q + '例句</div>'
                     '<div class="sent-wrap"><div class="front-sent">{{Sentence}}</div>'
                     '<span class="audio">{{Audio}}</span></div>'),
            "afmt": ('<div class="sec-h">' + ICON_Q + '例句</div>'
                     '<div class="sent-wrap"><div class="sent">{{SentenceHtml}}</div>'
                     '<span class="audio">{{Audio}}</span></div>'
                     '<div class="meaning">{{TranslationZh}}</div>'
                     '<div class="en">{{Translation}}</div>'
                     '<div class="utags"><span class="utag t-cat">{{Note}}</span>'
                     '<span class="utag t-reg">{{Register}}</span></div>'
                     '<div class="sec-h">' + ICON_B + '词汇信息</div>'
                     '<div class="vocab">{{VocabHtml}}</div>'),
        }],
        css=CSS)
    deck = genanki.Deck(DECK_ID, "Japanese IT Vocabulary （中文版・新UI）")
    media_files = []
    with_audio = 0
    for c in cards:
        toks = parse_pron(c["Pronunciation"])
        plain = "".join(s for s, _ in toks)
        span = None
        j = plain.find(c["Cloze"])
        if j >= 0:
            span = (j, j + len(c["Cloze"]))
        sent_html = ruby_html(toks, span)
        mp3 = f"{c['id']}_sent.mp3"
        path = os.path.join(MEDIA, mp3)
        audio = ""
        if os.path.exists(path) and os.path.getsize(path) > 0:
            media_files.append(path)
            audio = f"[sound:{mp3}]"
            with_audio += 1
        deck.add_note(genanki.Note(
            model=model, guid=f"it-zh2-{c['id']}",
            fields=[c["Sentence"], sent_html, vocab_html(c),
                    c["TranslationZh"], c["Translation"], c["Note"], c["Register"],
                    audio]))
    pkg = genanki.Package(deck)
    pkg.media_files = media_files
    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    out = os.path.join(ROOT, "dist", "it-vocab-zh-v2.apkg")
    pkg.write_to_file(out)
    print("wrote", out, os.path.getsize(out), "bytes,", len(cards),
          "cards,", with_audio, "with audio")

if __name__ == "__main__":
    main()
