from argenta.app.dividing_line import DynamicDividingLine, StaticDividingLine

import unittest


class TestDividingLine(unittest.TestCase):
    def test_get_static_dividing_line_full_line(self):
        line = StaticDividingLine('-')
        self.assertEqual(line.get_full_static_line(True).count('-'), 25)

    def test_get_dynamic_dividing_line_full_line(self):
        line = DynamicDividingLine()
        self.assertEqual(line.get_full_dynamic_line(20, True).count('-'), 20)

    def test_get_dividing_line_unit_part(self):
        line = StaticDividingLine('')
        self.assertEqual(line.get_unit_part(), ' ')

    def test_get_dividing_line2_unit_part(self):
        line = StaticDividingLine('+-0987654321!@#$%^&*()_')
        self.assertEqual(line.get_unit_part(), '+')
