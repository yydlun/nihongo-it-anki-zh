"""Keep the reported 言う reading correct in both source decks and Echo export."""
import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = 'ざっくり言うと、移行は半分終わっています。'
READING = 'ざっくり言【い】うと、移行【いこう】は半分【はんぶん】終【お】わっています。'

class MigrationSentenceReading(unittest.TestCase):
    def test_source_decks(self):
        for path in [ROOT/'decks/agentic-lab/tier5-vocabulary.csv', ROOT/'decks/it-vocab/tier12-vocabulary.csv']:
            with path.open(encoding='utf-8-sig', newline='') as file:
                rows = [row for row in csv.reader(file) if row and row[0] == TEXT]
            self.assertEqual(len(rows), 1, str(path))
            self.assertEqual(rows[0][3], READING)
            self.assertEqual(rows[0][2], 'ざっくり')

    def test_echo_export(self):
        deck = json.loads((ROOT/'imports/agentic-lab-jp-echo.json').read_text())
        rows = [row for row in deck['sentences'] if row.get('plainTarget') == TEXT]
        self.assertEqual(len(rows), 1)
        for field in ['target', 'casualTarget', 'politeTarget']:
            self.assertEqual(rows[0][field], READING)
