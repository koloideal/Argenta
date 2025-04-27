from argenta.command.flag import InputFlags, ValidInputFlag, Flag, Flags
from argenta.router import Router
from argenta.command import Command
from argenta.router.exceptions import (TriggerContainSpacesException,
                                       RepeatedFlagNameException,
                                       TooManyTransferredArgsException,
                                       RequiredArgumentNotPassedException)

import unittest
import re


class TestRouter(unittest.TestCase):
    def test_get_router_title(self):
        self.assertEqual(Router(title='test title').get_title(), 'test title')

    def test_register_command_with_spaces_in_trigger(self):
        router = Router()
        with self.assertRaises(TriggerContainSpacesException):
            router._validate_command(Command(trigger='command with spaces'))

    def test_register_command_with_repeated_flags(self):
        router = Router()
        with self.assertRaises(RepeatedFlagNameException):
            router._validate_command(Command(trigger='command', flags=Flags(Flag('test'), Flag('test'))))

    def test_validate_incorrect_input_flag1(self):
        router = Router()
        router.set_invalid_input_flag_handler(lambda flag: None)
        self.assertEqual(router._validate_input_flags(Command('cmd'), InputFlags(ValidInputFlag('ssh'))), False)

    def test_validate_incorrect_input_flag2(self):
        router = Router()
        router.set_invalid_input_flag_handler(lambda flag: None)
        self.assertEqual(router._validate_input_flags(Command('cmd'), InputFlags(ValidInputFlag('ssh', value='some'))), False)

    def test_validate_incorrect_input_flag3(self):
        router = Router()
        router.set_invalid_input_flag_handler(lambda flag: None)
        command = Command('cmd', flags=Flag('port'))
        input_flags = InputFlags(ValidInputFlag('ssh', value='some2'))
        self.assertEqual(router._validate_input_flags(command, input_flags), False)

    def test_validate_incorrect_input_flag4(self):
        router = Router()
        router.set_invalid_input_flag_handler(lambda flag: None)
        command = Command('cmd', flags=Flag('ssh', possible_values=False))
        input_flags = InputFlags(ValidInputFlag('ssh', value='some3'))
        self.assertEqual(router._validate_input_flags(command, input_flags), False)

    def test_validate_incorrect_input_flag5(self):
        router = Router()
        router.set_invalid_input_flag_handler(lambda flag: None)
        command = Command('cmd', flags=Flag('ssh', possible_values=re.compile(r'some[1-5]$')))
        input_flags = InputFlags(ValidInputFlag('ssh', value='some40'))
        self.assertEqual(router._validate_input_flags(command, input_flags), False)

    def test_validate_incorrect_input_flag6(self):
        router = Router()
        router.set_invalid_input_flag_handler(lambda flag: None)
        command = Command('cmd', flags=Flag('ssh', possible_values=['example']))
        input_flags = InputFlags(ValidInputFlag('ssh', value='example2'))
        self.assertEqual(router._validate_input_flags(command, input_flags), False)

    def test_validate_incorrect_input_flag7(self):
        router = Router()
        router.set_invalid_input_flag_handler(lambda flag: None)
        command = Command('cmd', flags=Flag('ssh', possible_values=['example']))
        input_flags = InputFlags(ValidInputFlag('ssh'))
        self.assertEqual(router._validate_input_flags(command, input_flags), False)

    def test_validate_correct_input_flag1(self):
        command = Command('cmd', flags=Flag('port'))
        input_flags = InputFlags(ValidInputFlag('port', value='some2'))
        self.assertEqual(Router()._validate_input_flags(command, input_flags), True)

    def test_validate_correct_input_flag2(self):
        command = Command('cmd', flags=Flag('port', possible_values=['some2', 'some3']))
        input_flags = InputFlags(ValidInputFlag('port', value='some2'))
        self.assertEqual(Router()._validate_input_flags(command, input_flags), True)

    def test_validate_correct_input_flag3(self):
        command = Command('cmd', flags=Flag('ssh', possible_values=re.compile(r'more[1-5]$')))
        input_flags = InputFlags(ValidInputFlag('ssh', value='more5'))
        self.assertEqual(Router()._validate_input_flags(command, input_flags), True)

    def test_validate_correct_input_flag4(self):
        command = Command('cmd', flags=Flag('ssh', possible_values=False))
        input_flags = InputFlags(ValidInputFlag('ssh'))
        self.assertEqual(Router()._validate_input_flags(command, input_flags), True)

    def test_validate_incorrect_func_args1(self):
        command = Command('cmd', flags=Flag('port'))
        def handler():
            pass
        with self.assertRaises(RequiredArgumentNotPassedException):
            Router()._validate_func_args(command, handler)

    def test_validate_incorrect_func_args2(self):
        command = Command('cmd', flags=Flag('port'))
        def handler(args, kwargs):
            pass
        with self.assertRaises(TooManyTransferredArgsException):
            Router()._validate_func_args(command, handler)

    def test_validate_incorrect_func_args3(self):
        command = Command('cmd')
        def handler(args):
            pass
        with self.assertRaises(TooManyTransferredArgsException):
            Router()._validate_func_args(command, handler)

    def test_get_router_aliases(self):
        router = Router()
        @router.command(Command('some', aliases=['test', 'case']))
        def handler():
            pass
        self.assertListEqual(router.get_aliases(), ['test', 'case'])

    def test_get_router_aliases2(self):
        router = Router()
        @router.command(Command('some', aliases=['test', 'case']))
        def handler():
            pass
        @router.command(Command('ext', aliases=['more', 'foo']))
        def handler2():
            pass
        self.assertListEqual(router.get_aliases(), ['test', 'case', 'more', 'foo'])

    def test_get_router_aliases3(self):
        router = Router()
        @router.command(Command('some'))
        def handler():
            pass
        self.assertListEqual(router.get_aliases(), [])









