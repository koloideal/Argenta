from argenta.app import App
from argenta.app.exceptions import InvalidDescriptionMessagePatternException

import unittest


class TestApp(unittest.TestCase):
    def test_set_invalid_description_message_pattern(self):
        with self.assertRaises(InvalidDescriptionMessagePatternException):
            App().set_description_message_pattern('Invalid description pattern')

    def test_set_invalid_description_message_pattern2(self):
        with self.assertRaises(InvalidDescriptionMessagePatternException):
            App().set_description_message_pattern('Invalid {desription} description {comand} pattern')

