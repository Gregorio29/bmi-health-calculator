import os, sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import tkinter as tk
import unittest

from ui import BMIApp


class UISmokeTests(unittest.TestCase):
    def test_calculate_and_clear(self):
        try:
            root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(f'Entorno sin pantalla: {error}')
        root.withdraw()
        app = BMIApp(root)
        app.age_var.set('30')
        app.weight_var.set('70')
        app.height_var.set('175')
        app.calculate()
        self.assertIn('22.86', app.results.get('1.0', 'end'))
        app.clear()
        self.assertEqual(app.age_var.get(), '')
        root.destroy()


if __name__ == '__main__':
    unittest.main()
