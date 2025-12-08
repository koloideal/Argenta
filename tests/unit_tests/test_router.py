import re

import pytest
from pytest import CaptureFixture

from argenta.command import Command, InputCommand
from argenta.command.flag import Flag, InputFlag
from argenta.command.flag.flags import Flags, InputFlags
from argenta.command.flag.models import PossibleValues, ValidationStatus
from argenta.response.entity import Response
from argenta.router import Router
from argenta.router.entity import _structuring_input_flags, _validate_func_args  # pyright: ignore[reportPrivateUsage]
from argenta.router.exceptions import (
    RepeatedFlagNameException,
    RepeatedTriggerNameException,
    RequiredArgumentNotPassedException,
    TriggerContainSpacesException,
)


# ============================================================================
# Tests for command validation
# ============================================================================


def test_validate_command_raises_error_for_trigger_with_spaces() -> None:
    router = Router()
    with pytest.raises(TriggerContainSpacesException):
        router._validate_command(Command(trigger='command with spaces'))
        
        
def test_validate_command_raises_error_for_same_trigger() -> None:
    router = Router()
    
    @router.command('comm')
    def handler(res: Response):
        pass
    
    with pytest.raises(RepeatedTriggerNameException):
        @router.command('comm')
        def handler2(res: Response):
            pass
        

def test_validate_command_raises_error_for_repeated_flag_names() -> None:
    router = Router()
    with pytest.raises(RepeatedFlagNameException):
        router._validate_command(Command(trigger='command', flags=Flags([Flag('test'), Flag('test')])))


# ============================================================================
# Tests for function argument validation
# ============================================================================


def test_validate_func_args_raises_error_for_missing_response_parameter() -> None:
    def handler() -> None:
        pass
    with pytest.raises(RequiredArgumentNotPassedException):
        _validate_func_args(handler)  # pyright: ignore[reportArgumentType]


def test_validate_func_args_prints_warning_for_wrong_type_hint(capsys: CaptureFixture[str]) -> None:
    class NotResponse:
        pass

    def func(_response: NotResponse) -> None:
        pass

    _validate_func_args(func)

    output = capsys.readouterr()

    assert "WARNING" in output.out


def test_validate_func_args_accepts_missing_type_hint(capsys: CaptureFixture[str]) -> None:
    def func(response) -> None:  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        pass
    _validate_func_args(func)  # pyright: ignore[reportUnknownArgumentType]
    output = capsys.readouterr()
    assert output.out == ''


# ============================================================================
# Tests for input flag structuring - undefined flags
# ============================================================================


def test_structuring_input_flags_marks_unregistered_flag_as_undefined() -> None:
    cmd = Command('cmd')
    input_flags = InputFlags([InputFlag('ssh', input_value='', status=None)])
    assert _structuring_input_flags(cmd, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='', status=ValidationStatus.UNDEFINED)])


def test_structuring_input_flags_marks_unregistered_flag_with_value_as_undefined() -> None:
    cmd = Command('cmd')
    input_flags = InputFlags([InputFlag('ssh', input_value='some', status=None)])
    assert _structuring_input_flags(cmd, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='some', status=ValidationStatus.UNDEFINED)])


def test_structuring_input_flags_marks_flag_undefined_when_different_flag_registered() -> None:
    cmd = Command('cmd', flags=Flag('port'))
    input_flags = InputFlags([InputFlag('ssh', input_value='some2', status=None)])
    assert _structuring_input_flags(cmd, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='some2', status=ValidationStatus.UNDEFINED)])


# ============================================================================
# Tests for input flag structuring - invalid flags
# ============================================================================


def test_structuring_input_flags_marks_flag_invalid_when_value_provided_for_neither() -> None:
    command = Command('cmd', flags=Flag('ssh', possible_values=PossibleValues.NEITHER))
    input_flags = InputFlags([InputFlag('ssh', input_value='some3', status=None)])
    assert _structuring_input_flags(command, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='some3', status=ValidationStatus.INVALID)])


def test_structuring_input_flags_marks_flag_invalid_when_value_not_matching_regex() -> None:
    command = Command('cmd', flags=Flag('ssh', possible_values=re.compile(r'some[1-5]$')))
    input_flags = InputFlags([InputFlag('ssh', input_value='some40', status=None)])
    assert _structuring_input_flags(command, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='some40', status=ValidationStatus.INVALID)])


def test_structuring_input_flags_marks_flag_invalid_when_value_not_in_list() -> None:
    command = Command('cmd', flags=Flag('ssh', possible_values=['example']))
    input_flags = InputFlags([InputFlag('ssh', input_value='example2', status=None)])
    assert _structuring_input_flags(command, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='example2', status=ValidationStatus.INVALID)])


# ============================================================================
# Tests for input flag structuring - valid flags
# ============================================================================


def test_structuring_input_flags_marks_registered_flag_as_valid() -> None:
    command = Command('cmd', flags=Flag('port'))
    input_flags = InputFlags([InputFlag('port', input_value='some2', status=None)])
    assert _structuring_input_flags(command, input_flags).input_flags == InputFlags([InputFlag('port', input_value='some2', status=ValidationStatus.VALID)])


def test_structuring_input_flags_marks_flag_valid_when_value_in_list() -> None:
    command = Command('cmd', flags=Flag('port', possible_values=['some2', 'some3']))
    input_flags = InputFlags([InputFlag('port', input_value='some2', status=None)])
    assert _structuring_input_flags(command, input_flags).input_flags == InputFlags([InputFlag('port', input_value='some2', status=ValidationStatus.VALID)])


def test_structuring_input_flags_marks_flag_valid_when_value_matches_regex() -> None:
    command = Command('cmd', flags=Flag('ssh', possible_values=re.compile(r'more[1-5]$')))
    input_flags = InputFlags([InputFlag('ssh', input_value='more5', status=None)])
    assert _structuring_input_flags(command, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='more5', status=ValidationStatus.VALID)])


def test_structuring_input_flags_marks_flag_valid_when_empty_value_for_neither() -> None:
    command = Command('cmd', flags=Flag('ssh', possible_values=PossibleValues.NEITHER))
    input_flags = InputFlags([InputFlag('ssh', input_value='', status=None)])
    assert _structuring_input_flags(command, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='', status=ValidationStatus.VALID)])


# ============================================================================
# Tests for router aliases
# ============================================================================


def test_router_aliases_returns_command_aliases() -> None:
    router = Router()
    @router.command(Command('some', aliases={'test', 'case'}))
    def handler(_response: Response) -> None:
        pass
    assert router.aliases == {'test', 'case'}


def test_router_aliases_returns_combined_aliases_from_multiple_commands() -> None:
    router = Router()
    @router.command(Command('some', aliases={'test', 'case'}))
    def handler(_response: Response) -> None:
        pass
    @router.command(Command('ext', aliases={'more', 'foo'}))
    def handler2(_response: Response) -> None:
        pass
    assert router.aliases == {'test', 'case', 'more', 'foo'}


def test_router_aliases_returns_empty_set_when_no_aliases() -> None:
    router = Router()
    @router.command(Command('some'))
    def handler(_response: Response) -> None:
        pass
    assert router.aliases == set()


# ============================================================================
# Tests for handler finding and execution
# ============================================================================


def test_finds_appropriate_handler_executes_handler_by_alias(capsys: CaptureFixture[str]) -> None:
    router = Router()

    @router.command(Command('hello', aliases={'hi'}))
    def handler(_res: Response) -> None:
        print("Hello World!")

    router.finds_appropriate_handler(InputCommand('hi'))

    output = capsys.readouterr()

    assert "Hello World!" in output.out
    
def test_finds_appropriate_handler_executes_handler_by_alias_with_differrent_register(capsys: CaptureFixture[str]) -> None:
    router = Router()

    @router.command(Command('hello', aliases={'hI'}))
    def handler(_res: Response) -> None:
        print("Hello World!")

    router.finds_appropriate_handler(InputCommand('HI'))

    output = capsys.readouterr()

    assert "Hello World!" in output.out
    
    
def test_finds_appropriate_handler_executes_handler_by_trigger_with_differrent_register(capsys: CaptureFixture[str]) -> None:
    router = Router()

    @router.command(Command('heLLo'))
    def handler(_res: Response) -> None:
        print("Hello World!")

    router.finds_appropriate_handler(InputCommand('HellO'))

    output = capsys.readouterr()

    assert "Hello World!" in output.out


def test_finds_appropriate_handler_executes_handler_with_flags_by_alias(capsys: CaptureFixture[str]) -> None:
    router = Router()

    @router.command(Command('hello', flags=Flag('flag'), aliases={'hi'}))
    def handler(_res: Response) -> None:
        print("Hello World!")

    router.finds_appropriate_handler(InputCommand('hi'))

    output = capsys.readouterr()

    assert "Hello World!" in output.out
