import re

import pytest

from argenta.command.exceptions import (EmptyInputCommandException,
                                        RepeatedInputFlagsException,
                                        UnprocessedInputFlagException)
from argenta.command.flag import Flag, InputFlag
from argenta.command.flag.flags import Flags
from argenta.command.flag.models import PossibleValues, ValidationStatus
from argenta.command.models import Command, InputCommand


def test_parse_correct_raw_command():
    assert InputCommand.parse('ssh --host 192.168.0.3').trigger == 'ssh'


def test_parse_raw_command_without_flag_name_with_value():
    with pytest.raises(UnprocessedInputFlagException):
        InputCommand.parse('ssh 192.168.0.3')


def test_parse_raw_command_with_repeated_flag_name():
    with pytest.raises(RepeatedInputFlagsException):
        InputCommand.parse('ssh --host 192.168.0.3 --host 172.198.0.43')
        
        
def test_parse_raw_command_with_triple_prefix():
    assert InputCommand.parse(
        'ssh ---host 192.168.0.0'
    ).input_flags.get_flag_by_name('host') == \
    InputFlag('host', input_value='192.168.0.0', prefix='---')
    
    
def test_parse_raw_command_with_unprocessed_entity():
    with pytest.raises(UnprocessedInputFlagException):
        InputCommand.parse('ssh --host 192.168.0.3 9977')


def test_parse_empty_raw_command():
    with pytest.raises(EmptyInputCommandException):
        InputCommand.parse('')


def test_validate_invalid_input_flag1():
    command = Command('some', flags=Flag('test'))
    assert command.validate_input_flag(InputFlag('test', input_value='', status=None)) == ValidationStatus.INVALID


def test_validate_valid_input_flag2():
    command = Command('some', flags=Flags([Flag('test'), Flag('more')]))
    assert command.validate_input_flag(InputFlag('more', input_value='random-value', status=None)) == ValidationStatus.VALID


def test_validate_undefined_input_flag1():
    command = Command('some', flags=Flag('test'))
    assert command.validate_input_flag(InputFlag('more', input_value='', status=None)) == ValidationStatus.UNDEFINED


def test_validate_undefined_input_flag2():
    command = Command('some', flags=Flags([Flag('test'), Flag('more')]))
    assert command.validate_input_flag(InputFlag('case', input_value='', status=None)) == ValidationStatus.UNDEFINED


def test_validate_undefined_input_flag3():
    command = Command('some')
    assert command.validate_input_flag(InputFlag('case', input_value='', status=None)) == ValidationStatus.UNDEFINED


def test_invalid_input_flag1():
    command = Command('some', flags=Flag('test', possible_values=PossibleValues.NEITHER))
    assert command.validate_input_flag(InputFlag('test', input_value='example', status=None)) == ValidationStatus.INVALID


def test_invalid_input_flag2():
    command = Command('some', flags=Flag('test', possible_values=['some', 'case']))
    assert command.validate_input_flag(InputFlag('test', input_value='slay', status=None)) == ValidationStatus.INVALID


def test_invalid_input_flag3():
    command = Command('some', flags=Flag('test', possible_values=re.compile(r'^ex\d{, 2}op$')))
    assert command.validate_input_flag(InputFlag('test', input_value='example', status=None)) == ValidationStatus.INVALID


def test_isinstance_parse_correct_raw_command():
    cmd = InputCommand.parse('ssh --host 192.168.0.3')
    assert isinstance(cmd, InputCommand)
