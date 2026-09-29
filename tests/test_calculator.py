import os, sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from decimal import Decimal
import unittest

from calculator import (
    bmi, bmi_category, reference_weight_range, kg_to_lb, lb_to_kg,
    height_to_meters, feet_inches_to_meters, weight_change,
    mifflin_st_jeor, tdee,
)


class CalculatorTests(unittest.TestCase):
    def test_bmi_normal_precision(self):
        self.assertEqual(bmi(Decimal('70'), Decimal('1.75')), Decimal('22.86'))

    def test_bmi_categories_and_exact_boundaries(self):
        self.assertEqual(bmi_category(Decimal('18.49')), 'Bajo peso')
        self.assertEqual(bmi_category(Decimal('18.5')), 'Rango de referencia')
        self.assertEqual(bmi_category(Decimal('24.99')), 'Rango de referencia')
        self.assertEqual(bmi_category(Decimal('25')), 'Sobrepeso')
        self.assertEqual(bmi_category(Decimal('30')), 'Obesidad')

    def test_reference_weight_range(self):
        self.assertEqual(reference_weight_range(Decimal('1.75')), (Decimal('56.66'), Decimal('76.56')))

    def test_weight_conversions(self):
        self.assertEqual(kg_to_lb(Decimal('70')), Decimal('154.32'))
        self.assertEqual(lb_to_kg(Decimal('154.324')), Decimal('70.00'))

    def test_height_conversions(self):
        self.assertEqual(height_to_meters(Decimal('175'), 'cm'), Decimal('1.75'))
        self.assertEqual(height_to_meters(Decimal('1.75'), 'm'), Decimal('1.75'))
        self.assertEqual(feet_inches_to_meters(5, Decimal('9')), Decimal('1.75'))

    def test_weight_change(self):
        self.assertEqual(weight_change(Decimal('80'), Decimal('76')), (Decimal('-4.00'), Decimal('-5.00'), 'disminuyó'))
        self.assertEqual(weight_change(Decimal('70'), Decimal('70')), (Decimal('0.00'), Decimal('0.00'), 'permaneció igual'))

    def test_mifflin_st_jeor(self):
        self.assertEqual(mifflin_st_jeor(Decimal('70'), Decimal('175'), 30, 'Masculino'), Decimal('1649'))
        self.assertEqual(mifflin_st_jeor(Decimal('70'), Decimal('175'), 30, 'Femenino'), Decimal('1483'))

    def test_tdee(self):
        self.assertEqual(tdee(Decimal('1649'), 'Moderada'), Decimal('2556'))

    def test_invalid_domain_values_raise(self):
        with self.assertRaises(ValueError):
            bmi(Decimal('-1'), Decimal('1.75'))
        with self.assertRaises(ValueError):
            weight_change(Decimal('0'), Decimal('70'))


if __name__ == '__main__':
    unittest.main()
