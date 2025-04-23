from argenta.router import Router
from argenta.command import Command
from argenta.router.exceptions import TriggerContainSpacesException

import unittest


class TestRouter(unittest.TestCase):
    def test_get_router_name(self):
        self.assertEqual(Router(name='test name').get_name(), 'test name')

    def test_get_router_title(self):
        self.assertEqual(Router(title='test title').get_title(), 'test title')

    def test_register_command_with_spaces_in_trigger(self):
        router = Router()
        with self.assertRaises(TriggerContainSpacesException):
            @router.command(Command(trigger='command with spaces'))
            def test():
                return 'correct result'
















