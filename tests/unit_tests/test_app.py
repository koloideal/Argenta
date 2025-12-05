from argenta.app.dividing_line import DynamicDividingLine, StaticDividingLine
from argenta.app.protocols import DescriptionMessageGenerator, NonStandardBehaviorHandler
from pytest import CaptureFixture

from argenta.app import App
from argenta.response import Response
from argenta.command.models import Command, InputCommand
from argenta.router import Router
import pytest


def test_is_exit_command1():
    app = App()
    assert app._is_exit_command(InputCommand('q')) is True


def test_is_exit_command5():
    app = App()
    assert app._is_exit_command(InputCommand('Q')) is True


def test_is_exit_command2():
    app = App(ignore_command_register=False)
    assert app._is_exit_command(InputCommand('q')) is False


def test_is_exit_command3():
    app = App(exit_command=Command('quit'))
    assert app._is_exit_command(InputCommand('quit')) is True


def test_is_exit_command4():
    app = App(exit_command=Command('quit'))
    assert app._is_exit_command(InputCommand('qUIt')) is True


def test_is_exit_command6():
    app = App(ignore_command_register=False,
              exit_command=Command('quit'))
    assert app._is_exit_command(InputCommand('qUIt')) is False


def test_is_unknown_command1():
    app = App()
    app.set_unknown_command_handler(lambda command: None)
    app._current_matching_triggers_with_routers = {'fr': Router(), 'tr': Router(), 'de': Router()}
    assert app._is_unknown_command(InputCommand('fr')) is False


def test_is_unknown_command2():
    app = App()
    app.set_unknown_command_handler(lambda command: None)
    app._current_matching_triggers_with_routers = {'fr': Router(), 'tr': Router(), 'de': Router()}
    assert app._is_unknown_command(InputCommand('cr')) is True

def test_is_unknown_command3():
    app = App(ignore_command_register=False)
    app.set_unknown_command_handler(lambda command: None)
    app._current_matching_triggers_with_routers = {'Pr': Router(), 'tW': Router(), 'deQW': Router()}
    assert app._is_unknown_command(InputCommand('pr')) is True


def test_is_unknown_command4():
    app = App(ignore_command_register=False)
    app.set_unknown_command_handler(lambda command: None)
    app._current_matching_triggers_with_routers = {'Pr': Router(), 'tW': Router(), 'deQW': Router()}
    assert app._is_unknown_command(InputCommand('tW')) is False

def test_add_messages_on_startup():
    app = App()
    app.add_message_on_startup('Some message')
    assert app._messages_on_startup == ['Some message']

def test_include_routers():
    app = App()
    router = Router()
    router2 = Router()
    app.include_routers(router, router2)

    assert app.registered_routers.registered_routers == [router, router2]

def test_overlapping_aliases(capsys: CaptureFixture[str]):
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('test', aliases={'alias'}))
    def handler(res: Response):
        pass

    @router.command(Command('test2', aliases={'alias'}))
    def handler2(res: Response):
        pass

    app.include_routers(router)
    app._pre_cycle_setup()

    captured = capsys.readouterr()

    assert "Overlapping" in captured.out

def test_print_framed_text(capsys: CaptureFixture[str]):
    app = App(
        override_system_messages=True,
        dividing_line=StaticDividingLine(length=5)
    )
    app._print_framed_text('test')

    captured = capsys.readouterr()

    assert '\n-----\n\ntest\n\n-----\n' in captured.out
    
def test_print_framed_text2(capsys: CaptureFixture[str]):
    app = App(
        override_system_messages=True,
        dividing_line=DynamicDividingLine()
    )
    app._print_framed_text('test as test as test')

    captured = capsys.readouterr()

    assert '\n' + '-'*20 + '\n\ntest as test as test\n\n' + '-'*20 + '\n' in captured.out
    
def test_print_framed_text3(capsys: CaptureFixture[str]):
    app = App(
        override_system_messages=True,
        dividing_line=DynamicDividingLine()
    )
    app._print_framed_text('some long test')

    captured = capsys.readouterr()

    assert '\n--------------\n\nsome long test\n\n--------------\n' in captured.out
    
def test_print_framed_text4(capsys: CaptureFixture[str]):
    class OtherDividingLine:
        pass
        
    app = App(
        override_system_messages=True,
        dividing_line=OtherDividingLine()  # pyright: ignore[reportArgumentType]
    )
    
    with pytest.raises(NotImplementedError):
        app._print_framed_text('some long test')
        
def test_most_similiar_command():
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('port', aliases={'p'}))
    def handler(res: Response):
        pass

    @router.command(Command('host', aliases={'h'}))
    def handler2(res: Response):
        pass

    app.include_routers(router)
    app._pre_cycle_setup()
    
    assert app._most_similar_command('por') == 'port'
    
def test_most_similiar_command2():
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('command'))
    def handler(res: Response):
        pass

    @router.command(Command('command_other'))
    def handler2(res: Response):
        pass

    app.include_routers(router)
    app._pre_cycle_setup()
    
    assert app._most_similar_command('com') == 'command'
    
def test_most_similiar_command3():
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('command'))
    def handler(res: Response):
        pass

    @router.command(Command('command_other'))
    def handler2(res: Response):
        pass

    app.include_routers(router)
    app._pre_cycle_setup()
    
    assert app._most_similar_command('command_') == 'command_other'
    
def test_most_similiar_command4():
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('command'))
    def handler(res: Response):
        pass

    @router.command(Command('command_other'))
    def handler2(res: Response):
        pass

    app.include_routers(router)
    app._pre_cycle_setup()
    
    assert app._most_similar_command('nonexists') is None
    
def test_most_similiar_command3():
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('command', aliases={'other_name'}))
    def handler(res: Response):
        pass

    @router.command(Command('command_other', aliases={'more_name'}))
    def handler2(res: Response):
        pass

    app.include_routers(router)
    app._pre_cycle_setup()
    
    assert app._most_similar_command('othe') == 'other_name'
    
def test_app_set_description_message_gen():
    app = App()
    descr_gen: DescriptionMessageGenerator = lambda command, description: print(command + '-+-' + description)
    app.set_description_message_pattern(descr_gen)
    
    assert app._description_message_gen is descr_gen
    
def test_app_set_exit_handler():
    app = App()
    handler: NonStandardBehaviorHandler[Response] = lambda response: print('goodbye')
    app.set_exit_command_handler(handler)
    
    assert app._exit_command_handler is handler
    
