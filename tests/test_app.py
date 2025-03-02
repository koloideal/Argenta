from argenta.app import App
from argenta.app.exceptions import (InvalidDescriptionMessagePatternException,
                                    NoRegisteredRoutersException)

import unittest


class TestApp(unittest.TestCase):
    def test_set_invalid_description_message_pattern(self):
        with self.assertRaises(InvalidDescriptionMessagePatternException):
            App().set_description_message_pattern('Invalid des{}cription pattern')

    def test_no_registered_router(self):
        with self.assertRaises(NoRegisteredRoutersException):
            App()._validate_number_of_routers()

