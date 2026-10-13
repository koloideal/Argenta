from unittest.mock import Mock

import pytest

from argenta.app.behavior_handlers.models import (
    BehaviorHandlersFabric,
    BehaviorHandlersSettersMixin,
)
from argenta.app.presentation.renderers import PlainRenderer
from argenta.command.models import InputCommand
from argenta.response import Response, ResponseStatus


@pytest.fixture
def mock_printer() -> Mock:
    return Mock()


@pytest.fixture
def mock_most_similar_getter() -> Mock:
    return Mock(return_value="similar_cmd")


@pytest.fixture
def behavior_fabric(mock_printer: Mock, mock_most_similar_getter: Mock) -> BehaviorHandlersFabric:
    renderer = PlainRenderer()
    return BehaviorHandlersFabric(mock_printer, renderer, mock_most_similar_getter)


class TestBehaviorHandlersFabric:
    def test_initialization(self, mock_printer: Mock, mock_most_similar_getter: Mock):
        renderer = PlainRenderer()
        fabric = BehaviorHandlersFabric(mock_printer, renderer, mock_most_similar_getter)

        assert fabric._printer == mock_printer
        assert fabric._renderer == renderer
        assert fabric._most_similar_command_getter == mock_most_similar_getter

    def test_generate_incorrect_input_syntax_handler(
        self, behavior_fabric: BehaviorHandlersFabric, mock_printer: Mock
    ):
        handler = behavior_fabric.generate_incorrect_input_syntax_handler()

        handler("bad --flag")

        mock_printer.assert_called_once()
        call_arg = mock_printer.call_args[0][0]
        assert "Incorrect flag syntax" in call_arg
        assert "bad --flag" in call_arg

    def test_incorrect_input_syntax_handler_escapes_markup(
        self, behavior_fabric: BehaviorHandlersFabric, mock_printer: Mock
    ):
        handler = behavior_fabric.generate_incorrect_input_syntax_handler()

        handler("bad [bold]flag")

        call_arg = mock_printer.call_args[0][0]
        assert "\\[bold]" in call_arg

    def test_generate_repeated_input_flags_handler(
        self, behavior_fabric: BehaviorHandlersFabric, mock_printer: Mock
    ):
        handler = behavior_fabric.generate_repeated_input_flags_handler()

        handler("cmd --flag --flag")

        mock_printer.assert_called_once()
        call_arg = mock_printer.call_args[0][0]
        assert "Repeated input flags" in call_arg
        assert "cmd --flag --flag" in call_arg

    def test_repeated_input_flags_handler_escapes_markup(
        self, behavior_fabric: BehaviorHandlersFabric, mock_printer: Mock
    ):
        handler = behavior_fabric.generate_repeated_input_flags_handler()

        handler("cmd --flag [red]x")

        call_arg = mock_printer.call_args[0][0]
        assert "\\[red]" in call_arg

    def test_generate_empty_input_command_handler(
        self, behavior_fabric: BehaviorHandlersFabric, mock_printer: Mock
    ):
        handler = behavior_fabric.generate_empty_input_command_handler()

        handler()

        mock_printer.assert_called_once()
        call_arg = mock_printer.call_args[0][0]
        assert "Empty input command" in call_arg

    def test_generate_unknown_command_handler(
        self,
        behavior_fabric: BehaviorHandlersFabric,
        mock_printer: Mock,
        mock_most_similar_getter: Mock,
    ):
        handler = behavior_fabric.generate_unknown_command_handler()

        input_command = InputCommand("unknown")
        handler(input_command)

        mock_most_similar_getter.assert_called_once_with("unknown")
        mock_printer.assert_called_once()
        call_arg = mock_printer.call_args[0][0]
        assert "Unknown command" in call_arg
        assert "unknown" in call_arg
        assert "similar_cmd" in call_arg

    def test_generate_unknown_command_handler_no_similar(self, mock_printer: Mock):
        renderer = PlainRenderer()
        most_similar_getter = Mock(return_value=None)
        fabric = BehaviorHandlersFabric(mock_printer, renderer, most_similar_getter)

        handler = fabric.generate_unknown_command_handler()
        input_command = InputCommand("unknown")
        handler(input_command)

        most_similar_getter.assert_called_once_with("unknown")
        mock_printer.assert_called_once()
        call_arg = mock_printer.call_args[0][0]
        assert "Unknown command" in call_arg
        assert "unknown" in call_arg
        assert "most similar" not in call_arg

    def test_generate_exit_command_handler(
        self, behavior_fabric: BehaviorHandlersFabric, mock_printer: Mock
    ):
        handler = behavior_fabric.generate_exit_command_handler("Goodbye!")

        response = Response(ResponseStatus.ALL_FLAGS_VALID)
        handler(response)

        mock_printer.assert_called_once_with("Goodbye!")

    def test_generate_description_message_generator(self, behavior_fabric: BehaviorHandlersFabric):
        generator = behavior_fabric.generate_description_message_generator()

        result = generator("test", "Test command")

        assert "test" in result
        assert "Test command" in result


class TestBehaviorHandlersSettersMixin:
    def test_initialization(self):
        def desc_gen(cmd, desc):
            return f"{cmd}: {desc}"

        def incorrect_handler(raw):
            return None

        def repeated_handler(raw):
            return None

        def empty_handler():
            return None

        def unknown_handler(cmd):
            return None

        def exit_handler(resp):
            return None

        mixin = BehaviorHandlersSettersMixin(
            desc_gen,
            incorrect_handler,
            repeated_handler,
            empty_handler,
            unknown_handler,
            exit_handler,
        )

        assert mixin._description_message_generator == desc_gen
        assert mixin._incorrect_input_syntax_handler == incorrect_handler
        assert mixin._repeated_input_flags_handler == repeated_handler
        assert mixin._empty_input_command_handler == empty_handler
        assert mixin._unknown_command_handler == unknown_handler
        assert mixin._exit_command_handler == exit_handler

    def test_set_description_message_pattern(self):
        def initial_gen(cmd, desc):
            return f"{cmd}: {desc}"

        mixin = BehaviorHandlersSettersMixin(
            initial_gen,
            lambda raw: None,
            lambda raw: None,
            lambda: None,
            lambda cmd: None,
            lambda resp: None,
        )

        def new_gen(cmd, desc):
            return f"{cmd} -> {desc}"

        mixin.set_description_message_pattern(new_gen)

        assert mixin._description_message_generator == new_gen

    def test_set_incorrect_input_syntax_handler(self):
        def initial_handler(raw):
            return None

        mixin = BehaviorHandlersSettersMixin(
            lambda cmd, desc: f"{cmd}: {desc}",
            initial_handler,
            lambda raw: None,
            lambda: None,
            lambda cmd: None,
            lambda resp: None,
        )

        def new_handler(raw):
            print(f"Error: {raw}")

        mixin.set_incorrect_input_syntax_handler(new_handler)

        assert mixin._incorrect_input_syntax_handler == new_handler

    def test_set_repeated_input_flags_handler(self):
        def initial_handler(raw):
            return None

        mixin = BehaviorHandlersSettersMixin(
            lambda cmd, desc: f"{cmd}: {desc}",
            lambda raw: None,
            initial_handler,
            lambda: None,
            lambda cmd: None,
            lambda resp: None,
        )

        def new_handler(raw):
            print(f"Repeated: {raw}")

        mixin.set_repeated_input_flags_handler(new_handler)

        assert mixin._repeated_input_flags_handler == new_handler

    def test_set_unknown_command_handler(self):
        def initial_handler(cmd):
            return None

        mixin = BehaviorHandlersSettersMixin(
            lambda cmd, desc: f"{cmd}: {desc}",
            lambda raw: None,
            lambda raw: None,
            lambda: None,
            initial_handler,
            lambda resp: None,
        )

        def new_handler(cmd):
            print(f"Unknown: {cmd.trigger}")

        mixin.set_unknown_command_handler(new_handler)

        assert mixin._unknown_command_handler == new_handler

    def test_set_empty_command_handler(self):
        def initial_handler():
            return None

        mixin = BehaviorHandlersSettersMixin(
            lambda cmd, desc: f"{cmd}: {desc}",
            lambda raw: None,
            lambda raw: None,
            initial_handler,
            lambda cmd: None,
            lambda resp: None,
        )

        def new_handler():
            print("Empty command")

        mixin.set_empty_command_handler(new_handler)

        assert mixin._empty_input_command_handler == new_handler

    def test_set_exit_command_handler(self):
        def initial_handler(resp):
            return None

        mixin = BehaviorHandlersSettersMixin(
            lambda cmd, desc: f"{cmd}: {desc}",
            lambda raw: None,
            lambda raw: None,
            lambda: None,
            lambda cmd: None,
            initial_handler,
        )

        def new_handler(resp):
            print("Exiting...")

        mixin.set_exit_command_handler(new_handler)

        assert mixin._exit_command_handler == new_handler
