# zh-v2：Japanese IT Vocabulary（中文版・新UI）

例句学习卡风格的新版中文牌组（1,516 条，与旧版 build_zh_deck.py 的牌组相互独立、互不影响）。

- 固定下载链接（永远指向最新版）：https://github.com/yydlun/nihongo-it-anki-zh/releases/latest/download/it-vocab-zh-v2.apkg
- 数据：`data/cards.json`（由 `tools/build_data.py` 从 decks/it-vocab 的 15 个 tier CSV ＋ `data/` 下的中文词典 JSON 生成）
- 音频：`tools/generate_audio.py`（Edge TTS 整句发音，GitHub Actions 自动补齐并发布，逻辑同 native-nihongo）
- 打包：`build.py`（genanki；MODEL_ID / DECK_ID 固定，guid 为 `it-zh2-<id>`）
