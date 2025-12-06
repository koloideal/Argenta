import sys
from argparse import Namespace
from typing import TYPE_CHECKING

import pytest
from pytest_mock import MockerFixture

from argenta.orchestrator.argparser.arguments.models import (
    BaseArgument,
    BooleanArgument,
    InputArgument,
    ValueArgument,
)
from argenta.orchestrator.argparser.entity import ArgParser, ArgSpace

if TYPE_CHECKING:
    from pytest_mock.plugin import MockType


# ============================================================================
# Tests for argument model creation
# ============================================================================


def test_value_argument_stores_all_properties() -> None:
    arg: ValueArgument = ValueArgument(
        name="test_arg",
        prefix="--",
        help="A test argument.",
        possible_values=["one", "two"],
        default="one",
        is_required=True,
        is_deprecated=False,
    )
    assert arg.name == "test_arg"
    assert arg.prefix == "--"
    assert arg.help == "A test argument."
    assert arg.possible_values == ["one", "two"]
    assert arg.default == "one"
    assert arg.is_required is True
    assert arg.is_deprecated is False
    assert arg.action == "store"
    assert arg.string_entity == "--test_arg"


def test_boolean_argument_stores_all_properties() -> None:
    arg: BooleanArgument = BooleanArgument(
        name="verbose", prefix="-", help="Enable verbose mode.", is_deprecated=True
    )
    assert arg.name == "verbose"
    assert arg.prefix == "-"
    assert arg.help == "Enable verbose mode."
    assert arg.is_deprecated is True
    assert arg.action == "store_true"
    assert arg.string_entity == "-verbose"


def test_input_argument_stores_all_properties() -> None:
    arg: InputArgument = InputArgument(
        name="file", value="/path/to/file", founder_class=ValueArgument
    )
    assert arg.name == "file"
    assert arg.value == "/path/to/file"
    assert arg.founder_class is ValueArgument


def test_input_argument_str_representation() -> None:
    arg = InputArgument('host', value='192.168.0.0', founder_class=ValueArgument)
    assert str(arg) == 'InputArgument(host=192.168.0.0)'


def test_input_argument_repr_representation() -> None:
    arg = InputArgument('host', value='192.168.0.0', founder_class=ValueArgument)
    assert repr(arg) == "InputArgument<name=host, value=192.168.0.0, founder_class=ValueArgument>"


# ============================================================================
# Fixtures for ArgSpace tests
# ============================================================================


@pytest.fixture
def mock_arguments() -> list[InputArgument]:
    return [
        InputArgument(name="arg1", value="val1", founder_class=ValueArgument),
        InputArgument(name="arg2", value=True, founder_class=BooleanArgument),
        InputArgument(name="arg3", value="val3", founder_class=ValueArgument),
    ]


@pytest.fixture
def arg_space(mock_arguments: list[InputArgument]) -> ArgSpace:
    return ArgSpace(all_arguments=mock_arguments)


# ============================================================================
# Tests for ArgSpace initialization and basic operations
# ============================================================================


def test_argspace_initializes_with_arguments(arg_space: ArgSpace, mock_arguments: list[InputArgument]) -> None:
    assert len(arg_space.all_arguments) == 3
    assert arg_space.all_arguments == mock_arguments


def test_argspace_get_by_name_finds_existing_argument(arg_space: ArgSpace, mock_arguments: list[InputArgument]) -> None:
    found_arg: InputArgument | None = arg_space.get_by_name("arg1")
    assert found_arg is not None
    assert found_arg == mock_arguments[0]


def test_argspace_get_by_name_returns_none_for_missing_argument(arg_space: ArgSpace) -> None:
    found_arg: InputArgument | None = arg_space.get_by_name("non_existent_arg")
    assert found_arg is None


def test_argspace_get_by_type_filters_value_arguments(arg_space: ArgSpace, mock_arguments: list[InputArgument]) -> None:
    value_args = arg_space.get_by_type(ValueArgument)
    assert len(value_args) == 2
    assert mock_arguments[0] in value_args
    assert mock_arguments[2] in value_args


def test_argspace_get_by_type_filters_boolean_arguments(arg_space: ArgSpace, mock_arguments: list[InputArgument]) -> None:
    bool_args = arg_space.get_by_type(BooleanArgument)
    assert len(bool_args) == 1
    assert mock_arguments[1] in bool_args


def test_argspace_get_by_type_returns_empty_list_for_unknown_type(arg_space: ArgSpace) -> None:
    class OtherArgument(BaseArgument):
        pass

    other_args = arg_space.get_by_type(OtherArgument)  # pyright: ignore[reportAssignmentType]
    assert other_args == []


def test_argspace_from_namespace_creates_argspace_from_parsed_namespace() -> None:
    namespace: Namespace = Namespace(config="config.json", debug=True, verbose=False)
    processed_args: list[ValueArgument | BooleanArgument] = [
        ValueArgument(name="config", prefix="--"),
        BooleanArgument(name="debug", prefix="-"),
        BooleanArgument(name="verbose", prefix="-"),
    ]

    arg_space: ArgSpace = ArgSpace.from_namespace(namespace, processed_args)
    assert len(arg_space.all_arguments) == 3

    config_arg: InputArgument | None = arg_space.get_by_name('config')
    debug_arg: InputArgument | None = arg_space.get_by_name('debug')

    assert config_arg is not None
    assert config_arg.value == "config.json"
    assert config_arg.founder_class is ValueArgument

    assert debug_arg is not None
    assert debug_arg.value is True
    assert debug_arg.founder_class is BooleanArgument


# ============================================================================
# Fixtures for ArgParser tests
# ============================================================================


@pytest.fixture
def value_arg() -> ValueArgument:
    return ValueArgument(
        name="config",
        help="Path to config file",
        default="dev.json",
        is_required=False,
        possible_values=["dev.json", "prod.json"],
    )


@pytest.fixture
def bool_arg() -> BooleanArgument:
    return BooleanArgument(name="debug", help="Enable debug mode")


@pytest.fixture
def processed_args(value_arg: ValueArgument, bool_arg: BooleanArgument) -> list[ValueArgument | BooleanArgument]:
    return [value_arg, bool_arg]


# ============================================================================
# Tests for ArgParser initialization
# ============================================================================


def test_argparser_initializes_with_all_properties(processed_args: list[ValueArgument | BooleanArgument]) -> None:
    parser: ArgParser = ArgParser(
        processed_args=processed_args,
        name="TestApp",
        description="A test application.",
        epilog="Test epilog.",
    )
    assert parser.name == "TestApp"
    assert parser.description == "A test application."
    assert parser.epilog == "Test epilog."
    assert parser.processed_args == processed_args
    assert isinstance(parser.parsed_argspace, ArgSpace)
    assert parser.parsed_argspace.all_arguments == []


# ============================================================================
# Tests for ArgParser argument registration (Python version specific)
# ============================================================================


@pytest.mark.skipif(sys.version_info < (3, 13), reason="requires python3.13 or higher")
def test_argparser_registers_arguments_with_deprecated_flag_py313(
    mocker: MockerFixture, value_arg: ValueArgument, bool_arg: BooleanArgument
) -> None:
    mock_add_argument: MockType = mocker.patch("argparse.ArgumentParser.add_argument")

    _parser: ArgParser = ArgParser(processed_args=[value_arg, bool_arg])

    # ArgParser may add additional arguments (like help), so check at least 2
    assert mock_add_argument.call_count >= 2
    
    # Check that value_arg was registered correctly
    value_arg_call = None
    bool_arg_call = None
    
    for call_args in mock_add_argument.call_args_list:
        args, kwargs = call_args
        if len(args) > 0 and args[0] == value_arg.string_entity:
            value_arg_call = (args, kwargs)
        elif len(args) > 0 and args[0] == bool_arg.string_entity:
            bool_arg_call = (args, kwargs)
    
    assert value_arg_call is not None, "value_arg was not registered"
    _, value_kwargs = value_arg_call
    assert value_kwargs['action'] == value_arg.action
    assert value_kwargs['help'] == value_arg.help
    assert value_kwargs['default'] == value_arg.default
    assert value_kwargs['choices'] == value_arg.possible_values
    assert value_kwargs['required'] == value_arg.is_required
    assert value_kwargs['deprecated'] == value_arg.is_deprecated
    
    assert bool_arg_call is not None, "bool_arg was not registered"
    _, bool_kwargs = bool_arg_call
    assert bool_kwargs['action'] == bool_arg.action
    assert bool_kwargs['help'] == bool_arg.help
    assert bool_kwargs['deprecated'] == bool_arg.is_deprecated


@pytest.mark.skipif(sys.version_info > (3, 12), reason="for more latest python version has been other test")
def test_argparser_registers_arguments_without_deprecated_flag_py312(
    mocker: MockerFixture, value_arg: ValueArgument, bool_arg: BooleanArgument
) -> None:
    mock_add_argument: MockType = mocker.patch("argparse.ArgumentParser.add_argument")

    _parser: ArgParser = ArgParser(processed_args=[value_arg, bool_arg])

    # ArgParser may add additional arguments (like help), so check at least 2
    assert mock_add_argument.call_count >= 2
    
    # Check that value_arg was registered correctly
    value_arg_call = None
    bool_arg_call = None
    
    for call_args in mock_add_argument.call_args_list:
        args, kwargs = call_args
        if len(args) > 0 and args[0] == value_arg.string_entity:
            value_arg_call = (args, kwargs)
        elif len(args) > 0 and args[0] == bool_arg.string_entity:
            bool_arg_call = (args, kwargs)
    
    assert value_arg_call is not None, "value_arg was not registered"
    _, value_kwargs = value_arg_call
    assert value_kwargs['action'] == value_arg.action
    assert value_kwargs['help'] == value_arg.help
    assert value_kwargs['default'] == value_arg.default
    assert value_kwargs['choices'] == value_arg.possible_values
    assert value_kwargs['required'] == value_arg.is_required
    assert 'deprecated' not in value_kwargs
    
    assert bool_arg_call is not None, "bool_arg was not registered"
    _, bool_kwargs = bool_arg_call
    assert bool_kwargs['action'] == bool_arg.action
    assert bool_kwargs['help'] == bool_arg.help
    assert 'deprecated' not in bool_kwargs


# ============================================================================
# Tests for ArgParser argument parsing
# ============================================================================


def test_argparser_parse_args_populates_argspace_correctly(
    mocker: MockerFixture, processed_args: list[ValueArgument | BooleanArgument]
) -> None:
    mock_namespace: Namespace = Namespace(config='config.json', debug=True)
    mocker.patch('argparse.ArgumentParser.parse_args', return_value=mock_namespace)

    parser: ArgParser = ArgParser(processed_args=processed_args)
    parser._parse_args()

    arg_space: ArgSpace = parser.parsed_argspace
    assert isinstance(arg_space, ArgSpace)
    assert len(arg_space.all_arguments) == 2

    config_arg: InputArgument | None = arg_space.get_by_name('config')
    debug_arg: InputArgument | None = arg_space.get_by_name('debug')

    assert config_arg is not None
    assert config_arg.value == 'config.json'
    assert config_arg.founder_class is ValueArgument

    assert debug_arg is not None
    assert debug_arg.value is True
    assert debug_arg.founder_class is BooleanArgument
