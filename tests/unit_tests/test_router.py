import re
import unittest

from argenta.command import Command
from argenta.command.flag import Flag, InputFlag
from argenta.command.flag.flags import Flags, InputFlags
from argenta.command.flag.models import PossibleValues, ValidationStatus
from argenta.response.entity import Response
from argenta.router import Router
from argenta.router.entity import (  # pyright: ignore[reportPrivateUsage]
    _structuring_input_flags, _validate_command, _validate_func_args)
from argenta.router.exceptions import (RepeatedFlagNameException,
                                       RequiredArgumentNotPassedException,
                                       TriggerContainSpacesException)


class TestRouter(unittest.TestCase):
    def test_register_command_with_spaces_in_trigger(self):
        with self.assertRaises(TriggerContainSpacesException):
            _validate_command(Command(trigger='command with spaces'))

    def test_register_command_with_repeated_flags(self):
        with self.assertRaises(RepeatedFlagNameException):
            _validate_command(Command(trigger='command', flags=Flags([Flag('test'), Flag('test')])))

    def test_structuring_input_flags1(self):
        cmd = Command('cmd')
        input_flags = InputFlags([InputFlag('ssh', input_value=None, status=None)])
        self.assertEqual(_structuring_input_flags(cmd, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value=None, status=ValidationStatus.UNDEFINED)]))

    def test_structuring_input_flags2(self):
        cmd = Command('cmd')
        input_flags = InputFlags([InputFlag('ssh', input_value='some', status=None)])
        self.assertEqual(_structuring_input_flags(cmd, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value='some', status=ValidationStatus.UNDEFINED)]))

    def test_structuring_input_flags3(self):
        cmd = Command('cmd', flags=Flag('port'))
        input_flags = InputFlags([InputFlag('ssh', input_value='some2', status=None)])
        self.assertEqual(_structuring_input_flags(cmd, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value='some2', status=ValidationStatus.UNDEFINED)]))

    def test_structuring_input_flags4(self):
        command = Command('cmd', flags=Flag('ssh', possible_values=PossibleValues.NEITHER))
        input_flags = InputFlags([InputFlag('ssh', input_value='some3', status=None)])
        self.assertEqual(_structuring_input_flags(command, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value='some3', status=ValidationStatus.INVALID)]))

    def test_structuring_input_flags5(self):
        command = Command('cmd', flags=Flag('ssh', possible_values=re.compile(r'some[1-5]$')))
        input_flags = InputFlags([InputFlag('ssh', input_value='some40', status=None)])
        self.assertEqual(_structuring_input_flags(command, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value='some40', status=ValidationStatus.INVALID)]))

    def test_structuring_input_flags6(self):
        command = Command('cmd', flags=Flag('ssh', possible_values=['example']))
        input_flags = InputFlags([InputFlag('ssh', input_value='example2', status=None)])
        self.assertEqual(_structuring_input_flags(command, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value='example2', status=ValidationStatus.INVALID)]))

    def test_structuring_input_flags7(self):
        command = Command('cmd', flags=Flag('port'))
        input_flags = InputFlags([InputFlag('port', input_value='some2', status=None)])
        self.assertEqual(_structuring_input_flags(command, input_flags).input_flags, InputFlags([InputFlag('port', input_value='some2', status=ValidationStatus.VALID)]))

    def test_structuring_input_flags8(self):
        command = Command('cmd', flags=Flag('port', possible_values=['some2', 'some3']))
        input_flags = InputFlags([InputFlag('port', input_value='some2', status=None)])
        self.assertEqual(_structuring_input_flags(command, input_flags).input_flags, InputFlags([InputFlag('port', input_value='some2', status=ValidationStatus.VALID)]))

    def test_structuring_input_flags9(self):
        command = Command('cmd', flags=Flag('ssh', possible_values=re.compile(r'more[1-5]$')))
        input_flags = InputFlags([InputFlag('ssh', input_value='more5', status=None)])
        self.assertEqual(_structuring_input_flags(command, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value='more5', status=ValidationStatus.VALID)]))

    def test_structuring_input_flags10(self):
        command = Command('cmd', flags=Flag('ssh', possible_values=PossibleValues.NEITHER))
        input_flags = InputFlags([InputFlag('ssh', input_value=None, status=None)])
        self.assertEqual(_structuring_input_flags(command, input_flags).input_flags, InputFlags([InputFlag('ssh', input_value=None, status=ValidationStatus.VALID)]))

    def test_validate_incorrect_func_args1(self):
        def handler():
            pass
        with self.assertRaises(RequiredArgumentNotPassedException):
            _validate_func_args(handler) # pyright: ignore[reportArgumentType]

    def test_get_router_aliases(self):
        router = Router()
        @router.command(Command('some', aliases=['test', 'case']))
        def handler(response: Response) -> None: # pyright: ignore[reportUnusedFunction]
            pass
        self.assertListEqual(router.aliases, ['test', 'case'])

    def test_get_router_aliases2(self):
        router = Router()
        @router.command(Command('some', aliases=['test', 'case']))
        def handler(response: Response): # pyright: ignore[reportUnusedFunction]
            pass
        @router.command(Command('ext', aliases=['more', 'foo']))
        def handler2(response: Response): # pyright: ignore[reportUnusedFunction]
            pass
        self.assertListEqual(router.aliases, ['test', 'case', 'more', 'foo'])

    def test_get_router_aliases3(self):
        router = Router()
        @router.command(Command('some'))
        def handler(response: Response): # pyright: ignore[reportUnusedFunction]
            pass
        self.assertListEqual(router.aliases, [])
