import re
import pytest

from argenta.command import Command, InputCommand
from argenta.command.flag import Flag, InputFlag
from argenta.command.flag.flags import Flags, InputFlags
from argenta.command.flag.models import PossibleValues, ValidationStatus
from argenta.response.entity import Response
from argenta.router import Router
from argenta.router.entity import _structuring_input_flags, _validate_func_args  # pyright: ignore[reportPrivateUsage]
from argenta.router.exceptions import (RepeatedFlagNameException,
                                       RequiredArgumentNotPassedException,
                                       TriggerContainSpacesException)


def test_register_command_with_spaces_in_trigger():
    router = Router()
    with pytest.raises(TriggerContainSpacesException):
        router._validate_command(Command(trigger='command with spaces'))

def test_register_command_with_repeated_flags():
    router = Router()
    with pytest.raises(RepeatedFlagNameException):
        router._validate_command(Command(trigger='command', flags=Flags([Flag('test'), Flag('test')])))

def test_structuring_input_flags1():
    cmd = Command('cmd')
    input_flags = InputFlags([InputFlag('ssh', input_value='', status=None)])
    assert _structuring_input_flags(cmd, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='', status=ValidationStatus.UNDEFINED)])

def test_structuring_input_flags2():
    cmd = Command('cmd')
    input_flags = InputFlags([InputFlag('ssh', input_value='some', status=None)])
    assert _structuring_input_flags(cmd, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='some', status=ValidationStatus.UNDEFINED)])

def test_structuring_input_flags3():
    cmd = Command('cmd', flags=Flag('port'))
    input_flags = InputFlags([InputFlag('ssh', input_value='some2', status=None)])
    assert _structuring_input_flags(cmd, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='some2', status=ValidationStatus.UNDEFINED)])

def test_structuring_input_flags4():
    command = Command('cmd', flags=Flag('ssh', possible_values=PossibleValues.NEITHER))
    input_flags = InputFlags([InputFlag('ssh', input_value='some3', status=None)])
    assert _structuring_input_flags(command, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='some3', status=ValidationStatus.INVALID)])

def test_structuring_input_flags5():
    command = Command('cmd', flags=Flag('ssh', possible_values=re.compile(r'some[1-5]$')))
    input_flags = InputFlags([InputFlag('ssh', input_value='some40', status=None)])
    assert _structuring_input_flags(command, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='some40', status=ValidationStatus.INVALID)])

def test_structuring_input_flags6():
    command = Command('cmd', flags=Flag('ssh', possible_values=['example']))
    input_flags = InputFlags([InputFlag('ssh', input_value='example2', status=None)])
    assert _structuring_input_flags(command, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='example2', status=ValidationStatus.INVALID)])

def test_structuring_input_flags7():
    command = Command('cmd', flags=Flag('port'))
    input_flags = InputFlags([InputFlag('port', input_value='some2', status=None)])
    assert _structuring_input_flags(command, input_flags).input_flags == InputFlags([InputFlag('port', input_value='some2', status=ValidationStatus.VALID)])

def test_structuring_input_flags8():
    command = Command('cmd', flags=Flag('port', possible_values=['some2', 'some3']))
    input_flags = InputFlags([InputFlag('port', input_value='some2', status=None)])
    assert _structuring_input_flags(command, input_flags).input_flags == InputFlags([InputFlag('port', input_value='some2', status=ValidationStatus.VALID)])

def test_structuring_input_flags9():
    command = Command('cmd', flags=Flag('ssh', possible_values=re.compile(r'more[1-5]$')))
    input_flags = InputFlags([InputFlag('ssh', input_value='more5', status=None)])
    assert _structuring_input_flags(command, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='more5', status=ValidationStatus.VALID)])

def test_structuring_input_flags10():
    command = Command('cmd', flags=Flag('ssh', possible_values=PossibleValues.NEITHER))
    input_flags = InputFlags([InputFlag('ssh', input_value='', status=None)])
    assert _structuring_input_flags(command, input_flags).input_flags == InputFlags([InputFlag('ssh', input_value='', status=ValidationStatus.VALID)])

def test_validate_incorrect_func_args1():
    def handler():
        pass
    with pytest.raises(RequiredArgumentNotPassedException):
        _validate_func_args(handler) # pyright: ignore[reportArgumentType]

def test_get_router_aliases():
    router = Router()
    @router.command(Command('some', aliases={'test', 'case'}))
    def handler(response: Response) -> None:
        pass
    assert router.aliases == {'test', 'case'}

def test_get_router_aliases2():
    router = Router()
    @router.command(Command('some', aliases={'test', 'case'}))
    def handler(response: Response): 
        pass
    @router.command(Command('ext', aliases={'more', 'foo'}))
    def handler2(response: Response): 
        pass
    assert router.aliases == {'test', 'case', 'more', 'foo'}

def test_get_router_aliases3():
    router = Router()
    @router.command(Command('some'))
    def handler(response: Response): 
        pass
    assert router.aliases == set()
    
def test_find_appropiate_handler(capsys: pytest.CaptureFixture[str]):
    router = Router()
    
    @router.command(Command('hello', aliases={'hi'}))
    def handler(res: Response):
        print("Hello World!")
        
    router.finds_appropriate_handler(InputCommand('hi'))
    
    output = capsys.readouterr()
    
    assert "Hello World!" in output.out
    
def test_find_appropiate_handler2(capsys: CaptureFixture[str]):
    router = Router()
    
    @router.command(Command('hello', flags=Flag('flag'), aliases={'hi'}))
    def handler(res: Response):
        print("Hello World!")
        
    router.finds_appropriate_handler(InputCommand('hi'))
    
    output = capsys.readouterr()
    
    assert "Hello World!" in output.out
    
def test_wrong_typehint(capsys: pytest.CaptureFixture[str]):
    class NotResponse: pass
    
    def func(response: NotResponse): pass
    
    _validate_func_args(func)
    
    output = capsys.readouterr()
    
    assert "WARNING" in output.out
    
def test_missing_typehint(capsys: pytest.CaptureFixture[str]):
    def func(response): pass  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
    
    _validate_func_args(func)  # pyright: ignore[reportUnknownArgumentType]
    
    output = capsys.readouterr()
    
    assert output.out == ''
        
    
