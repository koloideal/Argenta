from pytest import CaptureFixture

from argenta.app import App
from argenta.response import Response
from argenta.command.models import Command, InputCommand
from argenta.router import Router


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
    
    @router.command(Command('test', aliases=['alias']))
    def handler(res: Response):
        pass
        
    @router.command(Command('test2', aliases=['alias']))
    def handler2(res: Response):
        pass

    app.include_routers(router)
    app._pre_cycle_setup()
    
    captured = capsys.readouterr()
    
    assert "Overlapping" in captured.out

