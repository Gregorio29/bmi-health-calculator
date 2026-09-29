import os, sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import unittest
from validation import parse_decimal, validate_age, validate_weight, validate_height


class ValidationTests(unittest.TestCase):
    def test_parse_spanish_decimal(self):
        self.assertEqual(str(parse_decimal('70,5', 'Peso')), '70.5')

    def test_rejects_invalid_input_and_excess_decimals(self):
        for value in ('', 'abc', '-2', '1.2345'):
            with self.assertRaises(ValueError):
                parse_decimal(value, 'Campo', max_decimals=2)

    def test_age_rules(self):
        self.assertEqual(validate_age('20'), 20)
        for value in ('0', '151', '20.5'):
            with self.assertRaises(ValueError):
                validate_age(value)

    def test_plausible_weight_and_height(self):
        self.assertEqual(str(validate_weight('70')), '70')
        self.assertEqual(str(validate_height('1.75')), '1.75')
        with self.assertRaises(ValueError): validate_weight('600')
        with self.assertRaises(ValueError): validate_height('0.2')


if __name__ == '__main__':
    unittest.main()
