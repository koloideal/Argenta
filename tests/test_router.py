from argenta.command.params.flag import FlagsGroup, Flag
from argenta.router import Router
from argenta.command import Command
from argenta.router.exceptions import RepeatedCommandException

import unittest


class TestRouter(unittest.TestCase):
    def test_get_router_name(self):
        self.assertEqual(Router(name='test name').get_name(), 'test name')

    def test_get_router_title(self):
        self.assertEqual(Router(title='test title').get_title(), 'test title')

    def test_input_correct_command(self):
        router = Router()
        @router.command(Command(trigger='test'))
        def test():
            return 'correct result'

        self.assertEqual(router.input_command_handler(Command(trigger='test')), 'correct result')

    def test_input_command_with_invalid_flag(self):
        router = Router()
        router.set_invalid_input_flag_handler(lambda x: x)

        @router.command(Command(trigger='test'))
        def test():
            return 'correct result'

        input_command = Command(trigger='test')
        input_command._set_input_flags(FlagsGroup([Flag('host')]))

        self.assertEqual(router.input_command_handler(input_command), None)

    def test_input_correct_command_with_one_register_and_ignore_command_register(self):
        router = Router()
        router.set_ignore_command_register(True)
        @router.command(Command(trigger='test'))
        def test():
            return 'correct result'

        self.assertEqual(router.input_command_handler(Command(trigger='test')), 'correct result')

    def test_input_correct_command_with_different_register_and_ignore_command_register(self):
        router = Router()
        router.set_ignore_command_register(True)
        @router.command(Command(trigger='test'))
        def test():
            return 'correct result'

        self.assertEqual(router.input_command_handler(Command(trigger='TeSt')), 'correct result')

    def test_input_incorrect_command_with_ignore_command_register(self):
        router = Router()
        router.set_ignore_command_register(True)
        @router.command(Command(trigger='test'))
        def test():
            return 'correct result'

        self.assertEqual(router.input_command_handler(Command(trigger='Test2')), None)

    def test_register_repeated_commands_with_one_register(self):
        router = Router()
        @router.command(Command(trigger='test'))
        def test():
            return 'correct result'

        with self.assertRaises(RepeatedCommandException):
            @router.command(Command(trigger='test'))
            def test():
                return 'correct result'

    def test_register_commands_with_different_register(self):
        router = Router()
        @router.command(Command(trigger='test'))
        def test():
            return 'correct result'

        try:
            @router.command(Command(trigger='Test'))
            def test():
                return 'correct result'
        except RepeatedCommandException:
            self.fail('RepeatedCommandException should not have been thrown')

    def test_register_repeated_commands_with_one_register_and_set_ignore_command_register(self):
        router = Router()
        router.set_ignore_command_register(True)
        @router.command(Command(trigger='test'))
        def test():
            return 'correct result'

        with self.assertRaises(RepeatedCommandException):
            @router.command(Command(trigger='test'))
            def test():
                return 'correct result'

    def test_register_repeated_commands_with_different_register_and_set_ignore_command_register(self):
        router = Router()
        router.set_ignore_command_register(True)
        @router.command(Command(trigger='test'))
        def test():
            return 'correct result'

        with self.assertRaises(RepeatedCommandException):
            @router.command(Command(trigger='Test'))
            def test():
                return 'correct result'
















