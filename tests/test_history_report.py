import os, sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from decimal import Decimal
from pathlib import Path
import tempfile
import unittest

from history import SessionHistory
from report import build_report, save_report


class HistoryReportTests(unittest.TestCase):
    def test_history_add_clear_and_reuse(self):
        history = SessionHistory()
        history.add({'imc': '22.86'})
        self.assertEqual(history.items(), [{'imc': '22.86'}])
        self.assertEqual(history.latest(), {'imc': '22.86'})
        history.clear()
        self.assertEqual(history.items(), [])

    def test_report_contains_required_sections(self):
        data = {'Edad': '30', 'IMC': '22.86', 'Categoría': 'Rango de referencia'}
        content = build_report(data)
        self.assertIn('PROY-IMC-001', content)
        self.assertIn('Advertencia', content)
        self.assertIn('Fuentes', content)
        with tempfile.TemporaryDirectory() as temp:
            path = save_report(Path(temp) / 'informe.txt', data)
            self.assertTrue(path.exists())
            self.assertIn('22.86', path.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
