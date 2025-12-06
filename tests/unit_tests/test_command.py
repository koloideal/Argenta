import re

import pytest

from argenta.command.exceptions import (
    EmptyInputCommandException,
    RepeatedInputFlagsException,
    UnprocessedInputFlagException,
)
from argenta.command.flag import Flag, InputFlag
from argenta.command.flag.flags import Flags
from argenta.command.flag.models import PossibleValues, ValidationStatus
from argenta.command.models import Command, InputCommand


# ============================================================================
# Tests for InputCommand parsing - successful cases
# ============================================================================


def test_parse_extracts_trigger_from_command_with_flags() -> None:
    assert InputCommand.parse('ssh --host 192.168.0.3').trigger == 'ssh'


def test_parse_returns_input_command_instance() -> None:
    cmd = InputCommand.parse('ssh --host 192.168.0.3')
    assert isinstance(cmd, InputCommand)


def test_parse_handles_triple_prefix_flags() -> None:
    assert InputCommand.parse(
        'ssh ---host 192.168.0.0'
    ).input_flags.get_flag_by_name('host') == \
    InputFlag('host', input_value='192.168.0.0', prefix='---')


# ============================================================================
# Tests for InputCommand parsing - error cases
# ============================================================================


def test_parse_raises_error_for_value_without_flag_name() -> None:
    with pytest.raises(UnprocessedInputFlagException):
        InputCommand.parse('ssh 192.168.0.3')


def test_parse_raises_error_for_repeated_flag_names() -> None:
    with pytest.raises(RepeatedInputFlagsException):
        InputCommand.parse('ssh --host 192.168.0.3 --host 172.198.0.43')


def test_parse_raises_error_for_unprocessed_entity_after_flags() -> None:
    with pytest.raises(UnprocessedInputFlagException):
        InputCommand.parse('ssh --host 192.168.0.3 9977')


def test_parse_raises_error_for_empty_command() -> None:
    with pytest.raises(EmptyInputCommandException):
        InputCommand.parse('')


# ============================================================================
# Tests for flag validation - valid flags
# ============================================================================


def test_validate_input_flag_returns_valid_for_registered_flag() -> None:
    command = Command('some', flags=Flags([Flag('test'), Flag('more')]))
    assert command.validate_input_flag(InputFlag('more', input_value='random-value', status=None)) == ValidationStatus.VALID


# ============================================================================
# Tests for flag validation - invalid flags
# ============================================================================


def test_validate_input_flag_returns_invalid_for_flag_with_empty_value() -> None:
    command = Command('some', flags=Flag('test'))
    assert command.validate_input_flag(InputFlag('test', input_value='', status=None)) == ValidationStatus.INVALID


def test_validate_input_flag_returns_invalid_when_value_provided_for_neither_flag() -> None:
    command = Command('some', flags=Flag('test', possible_values=PossibleValues.NEITHER))
    assert command.validate_input_flag(InputFlag('test', input_value='example', status=None)) == ValidationStatus.INVALID


def test_validate_input_flag_returns_invalid_when_value_not_in_allowed_list() -> None:
    command = Command('some', flags=Flag('test', possible_values=['some', 'case']))
    assert command.validate_input_flag(InputFlag('test', input_value='slay', status=None)) == ValidationStatus.INVALID


def test_validate_input_flag_returns_invalid_when_value_does_not_match_regex() -> None:
    command = Command('some', flags=Flag('test', possible_values=re.compile(r'^ex\d{1,2}op$')))
    assert command.validate_input_flag(InputFlag('test', input_value='example', status=None)) == ValidationStatus.INVALID


# ============================================================================
# Tests for flag validation - undefined flags
# ============================================================================


def test_validate_input_flag_returns_undefined_for_unregistered_flag_name() -> None:
    command = Command('some', flags=Flag('test'))
    assert command.validate_input_flag(InputFlag('more', input_value='', status=None)) == ValidationStatus.UNDEFINED


def test_validate_input_flag_returns_undefined_for_unregistered_flag_in_multiple_flags() -> None:
    command = Command('some', flags=Flags([Flag('test'), Flag('more')]))
    assert command.validate_input_flag(InputFlag('case', input_value='', status=None)) == ValidationStatus.UNDEFINED


def test_validate_input_flag_returns_undefined_when_command_has_no_flags() -> None:
    command = Command('some')
    assert command.validate_input_flag(InputFlag('case', input_value='', status=None)) == ValidationStatus.UNDEFINED
