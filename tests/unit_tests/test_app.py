import pytest
from pytest import CaptureFixture

from argenta.app import App
from argenta.app.dividing_line import DynamicDividingLine, StaticDividingLine
from argenta.app.protocols import DescriptionMessageGenerator, NonStandardBehaviorHandler
from argenta.command.models import Command, InputCommand
from argenta.response import Response
from argenta.router import Router


# ============================================================================
# Tests for exit command detection
# ============================================================================


def test_default_exit_command_lowercase_q_is_recognized() -> None:
    app = App()
    assert app._is_exit_command(InputCommand('q')) is True


def test_default_exit_command_uppercase_q_is_recognized() -> None:
    app = App()
    assert app._is_exit_command(InputCommand('Q')) is True


def test_exit_command_not_recognized_when_case_sensitivity_enabled() -> None:
    app = App(ignore_command_register=False)
    assert app._is_exit_command(InputCommand('q')) is False


def test_custom_exit_command_is_recognized() -> None:
    app = App(exit_command=Command('quit'))
    assert app._is_exit_command(InputCommand('quit')) is True


def test_custom_exit_command_case_insensitive_by_default() -> None:
    app = App(exit_command=Command('quit'))
    assert app._is_exit_command(InputCommand('qUIt')) is True


def test_custom_exit_command_case_sensitive_when_enabled() -> None:
    app = App(ignore_command_register=False, exit_command=Command('quit'))
    assert app._is_exit_command(InputCommand('qUIt')) is False


def test_exit_command_alias_is_recognized() -> None:
    app = App(exit_command=Command('q', aliases={'exit'}))
    assert app._is_exit_command(InputCommand('exit')) is True


def test_exit_command_alias_case_sensitive_when_enabled() -> None:
    app = App(exit_command=Command('q', aliases={'exit'}), ignore_command_register=False)
    assert app._is_exit_command(InputCommand('exit')) is True


def test_non_exit_command_is_not_recognized() -> None:
    app = App(exit_command=Command('q', aliases={'exit'}))
    assert app._is_exit_command(InputCommand('quit')) is False


def test_non_exit_command_with_wrong_case_is_not_recognized() -> None:
    app = App(exit_command=Command('q', aliases={'exit'}), ignore_command_register=False)
    assert app._is_exit_command(InputCommand('Exit')) is False


# ============================================================================
# Tests for unknown command detection
# ============================================================================


def test_registered_command_is_not_unknown() -> None:
    app = App()
    app.set_unknown_command_handler(lambda command: None)
    app._current_matching_triggers_with_routers = {'fr': Router(), 'tr': Router(), 'de': Router()}
    assert app._is_unknown_command(InputCommand('fr')) is False


def test_unregistered_command_is_unknown() -> None:
    app = App()
    app.set_unknown_command_handler(lambda command: None)
    app._current_matching_triggers_with_routers = {'fr': Router(), 'tr': Router(), 'de': Router()}
    assert app._is_unknown_command(InputCommand('cr')) is True


def test_command_with_wrong_case_is_unknown_when_case_sensitivity_enabled() -> None:
    app = App(ignore_command_register=False)
    app.set_unknown_command_handler(lambda command: None)
    app._current_matching_triggers_with_routers = {'Pr': Router(), 'tW': Router(), 'deQW': Router()}
    assert app._is_unknown_command(InputCommand('pr')) is True


def test_command_with_exact_case_is_not_unknown_when_case_sensitivity_enabled() -> None:
    app = App(ignore_command_register=False)
    app.set_unknown_command_handler(lambda command: None)
    app._current_matching_triggers_with_routers = {'Pr': Router(), 'tW': Router(), 'deQW': Router()}
    assert app._is_unknown_command(InputCommand('tW')) is False


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
    
    assert app._most_similar_command('command_') == 'command_other'


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
    
    assert app._most_similar_command('othe') == 'other_name'


# ============================================================================
# Tests for router registration
# ============================================================================


def test_include_routers_registers_multiple_routers() -> None:
    app = App()
    router = Router()
    router2 = Router()
    app.include_routers(router, router2)

    assert app.registered_routers.registered_routers == [router, router2]


def test_overlapping_aliases_prints_warning(capsys: CaptureFixture[str]) -> None:
    app = App(override_system_messages=True)
    router = Router()

    @router.command(Command('test', aliases={'alias'}))
    def handler(_res: Response) -> None:
        pass

    @router.command(Command('test2', aliases={'alias'}))
    def handler2(_res: Response) -> None:
        pass

    app.include_routers(router)
    app._pre_cycle_setup()

    captured = capsys.readouterr()

    assert "Overlapping" in captured.out


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
# Tests for framed text printing
# ============================================================================


def test_print_framed_text_with_static_dividing_line(capsys: CaptureFixture[str]) -> None:
    app = App(override_system_messages=True, dividing_line=StaticDividingLine(length=5))
    app._print_framed_text('test')

    captured = capsys.readouterr()

    assert '\n-----\n\ntest\n\n-----\n' in captured.out


def test_print_framed_text_with_dynamic_dividing_line_short_text(capsys: CaptureFixture[str]) -> None:
    app = App(override_system_messages=True, dividing_line=DynamicDividingLine())
    app._print_framed_text('some long test')

    captured = capsys.readouterr()

    assert '\n--------------\n\nsome long test\n\n--------------\n' in captured.out


def test_print_framed_text_with_dynamic_dividing_line_long_text(capsys: CaptureFixture[str]) -> None:
    app = App(override_system_messages=True, dividing_line=DynamicDividingLine())
    app._print_framed_text('test as test as test')

    captured = capsys.readouterr()

    assert '\n' + '-'*20 + '\n\ntest as test as test\n\n' + '-'*20 + '\n' in captured.out


def test_print_framed_text_with_unsupported_dividing_line_raises_error() -> None:
    class OtherDividingLine:
        pass
        
    app = App(override_system_messages=True, dividing_line=OtherDividingLine())  # pyright: ignore[reportArgumentType]
    
    with pytest.raises(NotImplementedError):
        app._print_framed_text('some long test')


# ============================================================================
# Tests for handler configuration
# ============================================================================


def test_set_description_message_pattern_stores_generator() -> None:
    app = App()
    descr_gen: DescriptionMessageGenerator = lambda command, description: command + '-+-' + description
    app.set_description_message_pattern(descr_gen)
    
    assert app._description_message_gen is descr_gen


def test_set_exit_command_handler_stores_handler() -> None:
    app = App()
    handler: NonStandardBehaviorHandler[Response] = lambda response: print('goodbye')
    app.set_exit_command_handler(handler)
    
    assert app._exit_command_handler is handler


# ============================================================================
# Tests for default view setup
# ============================================================================


def test_setup_default_view_formats_prompt() -> None:
    app = App(prompt='>>')
    app._setup_default_view()
    
    assert app._prompt == '[italic dim bold]>>'


def test_setup_default_view_sets_default_unknown_command_handler() -> None:
    app = App()
    app._setup_default_view()
    assert app._unknown_command_handler(InputCommand('nonexists')) is None


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
