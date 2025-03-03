from argenta.command.params.flag import FlagsGroup, Flag
from argenta.router import Router
from argenta.command import Command

import unittest


class TestRouter(unittest.TestCase):
    def test_get_router_name(self):
        self.assertEqual(Router(name='test name').get_name(), 'test name')

    def test_get_router_title(self):
        self.assertEqual(Router(title='test title').get_title(), 'test title')

    def test_input_correct_command(self):
        router = Router()
        @router.command(Command(command='test'))
        def test():
            return 'correct result'

        self.assertEqual(router.input_command_handler(Command(command='test')), 'correct result')

    def test_input_command_with_invalid_flag(self):
        router = Router()
        router.set_invalid_input_flag_handler(lambda x: x)

        @router.command(Command(command='test'))
        def test():
            return 'correct result'

        input_command = Command(command='test')
        input_command.set_input_flags(FlagsGroup([Flag('host')]))

        self.assertEqual(router.input_command_handler(input_command), None)
