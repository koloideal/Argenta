from argenta.command.flag import InputFlag, Flag
from argenta.command.flags import Flags, InputFlags, UndefinedInputFlags, InvalidValueInputFlags, ValidInputFlags
from argenta.response import Response
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

    def test_structuring_input_flags1(self):
        router = Router()
        cmd = Command('cmd')
        input_flags = InputFlags(InputFlag('ssh'))
        self.assertEqual(router._structuring_input_flags(cmd, input_flags).undefined_flags, UndefinedInputFlags(InputFlag('ssh')))

    def test_structuring_input_flags2(self):
        router = Router()
        cmd = Command('cmd')
        input_flags = InputFlags(InputFlag('ssh', value='some'))
        self.assertEqual(router._structuring_input_flags(cmd, input_flags).undefined_flags, UndefinedInputFlags(InputFlag('ssh', value='some')))

    def test_structuring_input_flags3(self):
        router = Router()
        cmd = Command('cmd', flags=Flag('port'))
        input_flags = InputFlags(InputFlag('ssh', value='some2'))
        self.assertEqual(router._structuring_input_flags(cmd, input_flags).undefined_flags, UndefinedInputFlags(InputFlag('ssh', value='some2')))

    def test_structuring_input_flags4(self):
        router = Router()
        command = Command('cmd', flags=Flag('ssh', possible_values=False))
        input_flags = InputFlags(InputFlag('ssh', value='some3'))
        self.assertEqual(router._structuring_input_flags(command, input_flags).invalid_value_flags, InvalidValueInputFlags(InputFlag('ssh', value='some3')))

    def test_structuring_input_flags5(self):
        router = Router()
        command = Command('cmd', flags=Flag('ssh', possible_values=re.compile(r'some[1-5]$')))
        input_flags = InputFlags(InputFlag('ssh', value='some40'))
        self.assertEqual(router._structuring_input_flags(command, input_flags).invalid_value_flags, InvalidValueInputFlags(InputFlag('ssh', value='some40')))

    def test_structuring_input_flags6(self):
        router = Router()
        command = Command('cmd', flags=Flag('ssh', possible_values=['example']))
        input_flags = InputFlags(InputFlag('ssh', value='example2'))
        self.assertEqual(router._structuring_input_flags(command, input_flags).invalid_value_flags, InvalidValueInputFlags(InputFlag('ssh', value='example2')))

    def test_structuring_input_flags7(self):
        command = Command('cmd', flags=Flag('port'))
        input_flags = InputFlags(InputFlag('port', value='some2'))
        self.assertEqual(Router()._structuring_input_flags(command, input_flags).valid_flags, ValidInputFlags(InputFlag('port', value='some2')))

    def test_structuring_input_flags8(self):
        command = Command('cmd', flags=Flag('port', possible_values=['some2', 'some3']))
        input_flags = InputFlags(InputFlag('port', value='some2'))
        self.assertEqual(Router()._structuring_input_flags(command, input_flags).valid_flags, ValidInputFlags(InputFlag('port', value='some2')))

    def test_structuring_input_flags9(self):
        command = Command('cmd', flags=Flag('ssh', possible_values=re.compile(r'more[1-5]$')))
        input_flags = InputFlags(InputFlag('ssh', value='more5'))
        self.assertEqual(Router()._structuring_input_flags(command, input_flags).valid_flags, ValidInputFlags(InputFlag('ssh', value='more5')))

    def test_structuring_input_flags10(self):
        command = Command('cmd', flags=Flag('ssh', possible_values=False))
        input_flags = InputFlags(InputFlag('ssh'))
        self.assertEqual(Router()._structuring_input_flags(command, input_flags).valid_flags, ValidInputFlags(InputFlag('ssh')))

    def test_validate_incorrect_func_args1(self):
        def handler():
            pass
        with self.assertRaises(RequiredArgumentNotPassedException):
            Router()._validate_func_args(handler)

    def test_validate_incorrect_func_args2(self):
        def handler(args, kwargs):
            pass
        with self.assertRaises(TooManyTransferredArgsException):
            Router()._validate_func_args(handler)

    def test_get_router_aliases(self):
        router = Router()
        @router.command(Command('some', aliases=['test', 'case']))
        def handler(response):
            pass
        self.assertListEqual(router.get_aliases(), ['test', 'case'])

    def test_get_router_aliases2(self):
        router = Router()
        @router.command(Command('some', aliases=['test', 'case']))
        def handler(response):
            pass
        @router.command(Command('ext', aliases=['more', 'foo']))
        def handler2(response):
            pass
        self.assertListEqual(router.get_aliases(), ['test', 'case', 'more', 'foo'])

    def test_get_router_aliases3(self):
        router = Router()
        @router.command(Command('some'))
        def handler(response):
            pass
        self.assertListEqual(router.get_aliases(), [])









