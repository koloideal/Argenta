from argenta.command.flag import InputFlag, Flag
from argenta.command.flag.flags import Flags, InputFlags
from argenta.command.flag.models import PossibleValues, ValidationStatus
from argenta.router import Router
from argenta.command import Command
from argenta.router.exceptions import (TriggerContainSpacesException,
                                       RepeatedFlagNameException,
                                       TooManyTransferredArgsException,
                                       RequiredArgumentNotPassedException)

import unittest
import re


class TestRouter(unittest.TestCase):
    def test_register_command_with_spaces_in_trigger(self):
        router = Router()
        with self.assertRaises(TriggerContainSpacesException):
            router._validate_command(Command(trigger='command with spaces'))

    def test_register_command_with_repeated_flags(self):
        router = Router()
        with self.assertRaises(RepeatedFlagNameException):
            router._validate_command(Command(trigger='command', flags=Flags([Flag('test'), Flag('test')])))

    def test_structuring_input_flags1(self):
        router = Router()
        cmd = Command('cmd')
        input_flags = InputFlags([InputFlag('ssh', input_value=None, status=None)])
        self.assertEqual(router._structuring_input_flags(cmd, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value=None, status=ValidationStatus.UNDEFINED)]))

    def test_structuring_input_flags2(self):
        router = Router()
        cmd = Command('cmd')
        input_flags = InputFlags([InputFlag('ssh', input_value='some', status=None)])
        self.assertEqual(router._structuring_input_flags(cmd, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value='some', status=ValidationStatus.UNDEFINED)]))

    def test_structuring_input_flags3(self):
        router = Router()
        cmd = Command('cmd', flags=Flag('port'))
        input_flags = InputFlags([InputFlag('ssh', input_value='some2', status=None)])
        self.assertEqual(router._structuring_input_flags(cmd, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value='some2', status=ValidationStatus.UNDEFINED)]))

    def test_structuring_input_flags4(self):
        router = Router()
        command = Command('cmd', flags=Flag('ssh', possible_values=PossibleValues.NEITHER))
        input_flags = InputFlags([InputFlag('ssh', input_value='some3', status=None)])
        self.assertEqual(router._structuring_input_flags(command, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value='some3', status=ValidationStatus.INVALID)]))

    def test_structuring_input_flags5(self):
        router = Router()
        command = Command('cmd', flags=Flag('ssh', possible_values=re.compile(r'some[1-5]$')))
        input_flags = InputFlags([InputFlag('ssh', input_value='some40', status=None)])
        self.assertEqual(router._structuring_input_flags(command, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value='some40', status=ValidationStatus.INVALID)]))

    def test_structuring_input_flags6(self):
        router = Router()
        command = Command('cmd', flags=Flag('ssh', possible_values=['example']))
        input_flags = InputFlags([InputFlag('ssh', input_value='example2', status=None)])
        self.assertEqual(router._structuring_input_flags(command, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value='example2', status=ValidationStatus.INVALID)]))

    def test_structuring_input_flags7(self):
        command = Command('cmd', flags=Flag('port'))
        input_flags = InputFlags([InputFlag('port', input_value='some2', status=None)])
        self.assertEqual(Router()._structuring_input_flags(command, input_flags).input_flags, InputFlags([InputFlag('port', input_value='some2', status=ValidationStatus.VALID)]))

    def test_structuring_input_flags8(self):
        command = Command('cmd', flags=Flag('port', possible_values=['some2', 'some3']))
        input_flags = InputFlags([InputFlag('port', input_value='some2', status=None)])
        self.assertEqual(Router()._structuring_input_flags(command, input_flags).input_flags, InputFlags([InputFlag('port', input_value='some2', status=ValidationStatus.VALID)]))

    def test_structuring_input_flags9(self):
        command = Command('cmd', flags=Flag('ssh', possible_values=re.compile(r'more[1-5]$')))
        input_flags = InputFlags([InputFlag('ssh', input_value='more5', status=None)])
        self.assertEqual(Router()._structuring_input_flags(command, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value='more5', status=ValidationStatus.VALID)]))

    def test_structuring_input_flags10(self):
        command = Command('cmd', flags=Flag('ssh', possible_values=PossibleValues.NEITHER))
        input_flags = InputFlags([InputFlag('ssh', input_value=None, status=None)])
        self.assertEqual(Router()._structuring_input_flags(command, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value=None, status=ValidationStatus.VALID)]))

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









