from argenta.router.exceptions import RepeatedAliasNameException
import pytest
from pytest import CaptureFixture

from argenta.app import App
from argenta.app.protocols import DescriptionMessageGenerator, NonStandardBehaviorHandler
from argenta.command.models import Command, InputCommand
from argenta.response import Response
from argenta.response.status import ResponseStatus
from argenta.router import Router


# ============================================================================
# Tests for exit command detection
# ============================================================================


def test_default_exit_command_lowercase_q_is_recognized() -> None:
    app = App()
    app._setup_system_router()
    assert app._is_exit_command(InputCommand('q')) is True


def test_default_exit_command_uppercase_q_is_recognized() -> None:
    app = App()
    app._setup_system_router()
    assert app._is_exit_command(InputCommand('Q')) is True


def test_custom_exit_command_is_recognized() -> None:
    app = App(exit_command=Command('quit'))
    app._setup_system_router()
    assert app._is_exit_command(InputCommand('quit')) is True


def test_exit_command_alias_is_recognized() -> None:
    app = App(exit_command=Command('q', aliases={'exit'}))
    app._setup_system_router()
    assert app._is_exit_command(InputCommand('exit')) is True


def test_non_exit_command_is_not_recognized() -> None:
    app = App(exit_command=Command('q', aliases={'exit'}))
    app._setup_system_router()
    assert app._is_exit_command(InputCommand('quit')) is False


# ============================================================================
# Tests for unknown command detection
# ============================================================================


def test_registered_command_is_not_unknown() -> None:
    app = App()
    app.set_unknown_command_handler(lambda command: None)
    router = Router()
    
    @router.command('fr')
    def handler(res: Response):
        pass
        
    app.include_router(router)
    assert app._is_unknown_command(InputCommand('fr')) is False


def test_unregistered_command_is_unknown() -> None:
    app = App()
    app.set_unknown_command_handler(lambda command: None)
    assert app._is_unknown_command(InputCommand('cr')) is True


# ============================================================================
# Tests for similar command suggestions
# ============================================================================


def test_most_similar_command_finds_closest_match() -> None:
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('port', aliases={'p'}))
    def handler(_res: Response) -> None:
        pass

    @router.command(Command('host', aliases={'h'}))
    def handler2(_res: Response) -> None:
        pass

    app.include_routers(router)
    app._pre_cycle_setup()
    
    assert app._most_similar_command('por') == 'port'


def test_most_similar_command_prefers_shorter_match() -> None:
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('command'))
    def handler(_res: Response) -> None:
        pass

    @router.command(Command('command_other'))
    def handler2(_res: Response) -> None:
        pass

    app.include_routers(router)
    app._pre_cycle_setup()
    
    assert app._most_similar_command('com') == 'command'


def test_most_similar_command_finds_longer_match_when_closer() -> None:
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('command'))
    def handler(_res: Response) -> None:
        pass

    @router.command(Command('command_other'))
    def handler2(_res: Response) -> None:
        pass

    app.include_routers(router)
    app._pre_cycle_setup()
    
    assert app._most_similar_command('command_') == 'command'


def test_most_similar_command_returns_none_for_no_match() -> None:
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('command'))
    def handler(_res: Response) -> None:
        pass

    @router.command(Command('command_other'))
    def handler2(_res: Response) -> None:
        pass

    app.include_routers(router)
    app._pre_cycle_setup()
    
    assert app._most_similar_command('nonexists') is None


def test_most_similar_command_matches_aliases() -> None:
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('command', aliases={'other_name'}))
    def handler(_res: Response) -> None:
        pass

    @router.command(Command('command_other', aliases={'more_name'}))
    def handler2(_res: Response) -> None:
        pass

    app.include_routers(router)
    app._pre_cycle_setup()
    
    assert app._most_similar_command('other_') == 'other_name'


# ============================================================================
# Tests for router registration
# ============================================================================


def test_include_routers_registers_multiple_routers() -> None:
    app = App()
    router = Router()
    router2 = Router()
    app.include_routers(router, router2)

    assert app.registered_routers.registered_routers == [router, router2]


def test_overlapping_aliases_raises_exception() -> None:
    router = Router()

    @router.command(Command('test', aliases={'alias'}))
    def handler(_res: Response) -> None:
        pass

    with pytest.raises(RepeatedAliasNameException):
        @router.command(Command('test2', aliases={'alias'}))
        def handler2(_res: Response) -> None:
            pass


def test_app_detects_trigger_collision_between_routers() -> None:
    from argenta.router.exceptions import RepeatedTriggerNameException
    
    app = App()
    router1 = Router()
    router2 = Router()

    @router1.command('hello')
    def handler1(_res: Response) -> None:
        pass

    @router2.command('hello')
    def handler2(_res: Response) -> None:
        pass

    app.include_router(router1)
    app.include_router(router2)

    with pytest.raises(RepeatedTriggerNameException):
        app._pre_cycle_setup()


def test_app_detects_alias_collision_between_routers() -> None:
    app = App()
    router1 = Router()
    router2 = Router()

    @router1.command(Command('hello', aliases={'hi'}))
    def handler1(_res: Response) -> None:
        pass

    @router2.command(Command('world', aliases={'hi'}))
    def handler2(_res: Response) -> None:
        pass

    app.include_router(router1)
    app.include_router(router2)

    with pytest.raises(RepeatedAliasNameException):
        app._pre_cycle_setup()


def test_app_detects_trigger_alias_collision_between_routers() -> None:
    app = App()
    router1 = Router()
    router2 = Router()

    @router1.command('hello')
    def handler1(_res: Response) -> None:
        pass

    @router2.command(Command('world', aliases={'hello'}))
    def handler2(_res: Response) -> None:
        pass

    app.include_router(router1)
    app.include_router(router2)

    with pytest.raises(RepeatedAliasNameException):
        app._pre_cycle_setup()


def test_app_detects_collision_case_insensitive() -> None:
    from argenta.router.exceptions import RepeatedTriggerNameException
    
    app = App()
    router1 = Router()
    router2 = Router()

    @router1.command('Hello')
    def handler1(_res: Response) -> None:
        pass

    @router2.command('hELLo')
    def handler2(_res: Response) -> None:
        pass

    app.include_router(router1)
    app.include_router(router2)

    with pytest.raises(RepeatedTriggerNameException):
        app._pre_cycle_setup()


# ============================================================================
# Tests for startup messages
# ============================================================================


def test_add_message_on_startup_stores_message() -> None:
    app = App()
    app.add_message_on_startup('Some message')
    assert app._messages_on_startup == ['Some message']


def test_pre_cycle_setup_prints_startup_messages(capsys: CaptureFixture[str]) -> None:
    app = App()
    app.add_message_on_startup('some message')
    app._pre_cycle_setup()
    stdout = capsys.readouterr()
    
    assert 'some message' in stdout.out


# ============================================================================
# Tests for handler configuration
# ============================================================================


def test_set_description_message_pattern_stores_generator() -> None:
    app = App()
    descr_gen: DescriptionMessageGenerator = lambda command, description: command + '-+-' + description
    app.set_description_message_pattern(descr_gen)
    
    assert app._description_message_generator is descr_gen


def test_set_exit_command_handler_stores_handler() -> None:
    app = App()
    handler: NonStandardBehaviorHandler[Response] = lambda response: print('goodbye')
    app.set_exit_command_handler(handler)
    
    assert app._exit_command_handler is handler


# ============================================================================
# Tests for command processing
# ============================================================================


def test_process_command_with_router_with_disabled_stdout_redirect(capsys: CaptureFixture[str]) -> None:
    app = App(repeat_command_groups_printing=True)
    router = Router(disable_redirect_stdout=True)
    
    @router.command('command')
    def handler(_res: Response) -> None:
        print("Hello!")
        
    app.include_router(router)
    
    app._pre_cycle_setup()
    app._process_exist_and_valid_command(InputCommand('command'))
    
    stdout = capsys.readouterr()
    
    assert 'Hello!' in stdout.out


# ============================================================================
# Tests for handler setters and execution
# ============================================================================


def test_set_unknown_command_handler_stores_handler() -> None:
    app = App()
    call_tracker = {'called': False}
    
    def custom_handler(_command: InputCommand) -> None:
        call_tracker['called'] = True
    
    app.set_unknown_command_handler(custom_handler)
    app._unknown_command_handler(InputCommand('test'))
    
    assert call_tracker['called']


def test_set_exit_handler_stores_handler() -> None:
    app = App()
    call_tracker = {'called': False}
    
    def custom_handler(_response: Response) -> None:
        call_tracker['called'] = True
    
    app.set_exit_command_handler(custom_handler)
    app._exit_command_handler(Response(ResponseStatus.ALL_FLAGS_VALID))
    
    assert call_tracker['called']


def test_set_empty_command_handler_stores_handler() -> None:
    app = App()
    call_tracker = {'called': False}
    
    def custom_handler() -> None:
        call_tracker['called'] = True
    
    app.set_empty_command_handler(custom_handler)
    app._empty_input_command_handler()
    
    assert call_tracker['called']


def test_set_incorrect_input_syntax_handler_stores_handler() -> None:
    app = App()
    call_tracker = {'called': False}
    
    def custom_handler(_command: str) -> None:
        call_tracker['called'] = True
    
    app.set_incorrect_input_syntax_handler(custom_handler)
    app._incorrect_input_syntax_handler('test --flag')
    
    assert call_tracker['called']


def test_set_repeated_input_flags_handler_stores_handler() -> None:
    app = App()
    call_tracker = {'called': False}
    
    def custom_handler(_command: str) -> None:
        call_tracker['called'] = True
    
    app.set_repeated_input_flags_handler(custom_handler)
    app._repeated_input_flags_handler('test --flag --flag')
    
    assert call_tracker['called']


# ============================================================================
# Tests for handler execution with output
# ============================================================================


def test_unknown_command_handler_prints_custom_message(capsys: CaptureFixture[str]) -> None:
    app = App(override_system_messages=True)
    
    def custom_handler(command: InputCommand) -> None:
        print(f'Command not found: {command.trigger}')
    
    app.set_unknown_command_handler(custom_handler)
    app._unknown_command_handler(InputCommand('unknown'))
    
    output = capsys.readouterr()
    assert 'Command not found: unknown' in output.out


def test_exit_command_handler_prints_custom_message(capsys: CaptureFixture[str]) -> None:
    app = App(override_system_messages=True)
    
    def custom_handler(_response: Response) -> None:
        print('Goodbye!')
    
    app.set_exit_command_handler(custom_handler)
    app._exit_command_handler(Response(ResponseStatus.ALL_FLAGS_VALID))
    
    output = capsys.readouterr()
    assert 'Goodbye!' in output.out


def test_empty_command_handler_prints_custom_message(capsys: CaptureFixture[str]) -> None:
    app = App(override_system_messages=True)
    
    def custom_handler() -> None:
        print('Please enter a command')
    
    app.set_empty_command_handler(custom_handler)
    app._empty_input_command_handler()
    
    output = capsys.readouterr()
    assert 'Please enter a command' in output.out


def test_incorrect_syntax_handler_prints_custom_message(capsys: CaptureFixture[str]) -> None:
    app = App(override_system_messages=True)
    
    def custom_handler(command: str) -> None:
        print(f'Syntax error in: {command}')
    
    app.set_incorrect_input_syntax_handler(custom_handler)
    app._incorrect_input_syntax_handler('test --flag')
    
    output = capsys.readouterr()
    assert 'Syntax error in: test --flag' in output.out


def test_repeated_flags_handler_prints_custom_message(capsys: CaptureFixture[str]) -> None:
    app = App(override_system_messages=True)
    
    def custom_handler(command: str) -> None:
        print(f'Duplicate flags in: {command}')
    
    app.set_repeated_input_flags_handler(custom_handler)
    app._repeated_input_flags_handler('test --flag --flag')
    
    output = capsys.readouterr()
    assert 'Duplicate flags in: test --flag --flag' in output.out


# ============================================================================
# Tests for default handler behavior
# ============================================================================


def test_default_unknown_command_handler_prints_message(capsys: CaptureFixture[str]) -> None:
    app = App(override_system_messages=True)
    app._unknown_command_handler(InputCommand('unknown'))
    
    output = capsys.readouterr()
    assert 'Unknown command: unknown' in output.out


def test_default_empty_command_handler_prints_message(capsys: CaptureFixture[str]) -> None:
    app = App(override_system_messages=True)
    app._empty_input_command_handler()
    
    output = capsys.readouterr()
    assert 'Empty input command' in output.out


def test_default_incorrect_syntax_handler_prints_message(capsys: CaptureFixture[str]) -> None:
    app = App(override_system_messages=True)
    app._incorrect_input_syntax_handler('test --flag')
    
    output = capsys.readouterr()
    assert 'Incorrect flag syntax: test --flag' in output.out


def test_default_repeated_flags_handler_prints_message(capsys: CaptureFixture[str]) -> None:
    app = App(override_system_messages=True)
    app._repeated_input_flags_handler('test --flag --flag')
    
    output = capsys.readouterr()
    assert 'Repeated input flags: test --flag --flag' in output.out


# ============================================================================
# Tests for handler chaining and multiple calls
# ============================================================================


def test_handler_can_be_replaced_multiple_times() -> None:
    app = App()
    call_tracker = {'count': 0}
    
    def handler1(_command: InputCommand) -> None:
        call_tracker['count'] += 1
    
    def handler2(_command: InputCommand) -> None:
        call_tracker['count'] += 10
    
    app.set_unknown_command_handler(handler1)
    app._unknown_command_handler(InputCommand('test'))
    assert call_tracker['count'] == 1
    
    app.set_unknown_command_handler(handler2)
    app._unknown_command_handler(InputCommand('test'))
    assert call_tracker['count'] == 11


def test_handler_receives_correct_parameters() -> None:
    app = App()
    received_data: dict[str, None | str] = {'trigger': None}
    
    def custom_handler(command: InputCommand) -> None:
        received_data['trigger'] = command.trigger
    
    app.set_unknown_command_handler(custom_handler)
    app._unknown_command_handler(InputCommand('mycommand'))
    
    assert received_data['trigger'] == 'mycommand'


def test_exit_handler_receives_response_object() -> None:
    app = App()
    received_data: dict[str, None | Response] = {'response': None}
    
    def custom_handler(response: Response) -> None:
        received_data['response'] = response
    
    app.set_exit_command_handler(custom_handler)
    test_response = Response(ResponseStatus.ALL_FLAGS_VALID)
    app._exit_command_handler(test_response)
    
    assert received_data['response'] is test_response


# ============================================================================
# Tests for handler integration with routers
# ============================================================================


def test_app_with_router_and_custom_unknown_handler(capsys: CaptureFixture[str]) -> None:
    app = App(override_system_messages=True)
    router = Router()
    
    @router.command(Command('test'))
    def handler(_res: Response) -> None:
        print('test executed')
    
    app.include_router(router)
    
    def custom_unknown_handler(command: InputCommand) -> None:
        print(f'Not found: {command.trigger}')
    
    app.set_unknown_command_handler(custom_unknown_handler)
    
    # Test that unknown command uses custom handler
    assert app._is_unknown_command(InputCommand('unknown'))
    app._unknown_command_handler(InputCommand('unknown'))
    
    output = capsys.readouterr()
    assert 'Not found: unknown' in output.out


def test_app_handlers_work_with_multiple_routers() -> None:
    app = App(override_system_messages=True)
    router1 = Router()
    router2 = Router()
    
    @router1.command(Command('cmd1'))
    def handler1(_res: Response) -> None:
        pass
    
    @router2.command(Command('cmd2'))
    def handler2(_res: Response) -> None:
        pass
    
    app.include_routers(router1, router2)
    app._pre_cycle_setup()
    
    call_tracker = {'called': False}
    
    def custom_handler(_command: InputCommand) -> None:
        call_tracker['called'] = True
    
    app.set_unknown_command_handler(custom_handler)
    
    assert not app._is_unknown_command(InputCommand('cmd1'))
    assert not app._is_unknown_command(InputCommand('cmd2'))
    
    assert app._is_unknown_command(InputCommand('unknown'))
    app._unknown_command_handler(InputCommand('unknown'))
    assert call_tracker['called']


def test_process_exist_and_valid_command_raises_runtime_error_when_router_not_found() -> None:
    app = App()
    app._pre_cycle_setup()
    
    with pytest.raises(RuntimeError, match="Router for 'nonexistent' not found. Panic!"):
        app._process_exist_and_valid_command(InputCommand('nonexistent'))
