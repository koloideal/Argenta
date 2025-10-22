import pytest
from argparse import Namespace
from unittest.mock import MagicMock, call

from argenta.orchestrator.argparser.entity import ArgParser, ArgSpace
from argenta.orchestrator.argparser.arguments.models import (
    ValueArgument,
    BooleanArgument,
    InputArgument,
    BaseArgument,
)


class TestArgumentCreation:
    """Tests for the creation and attribute validation of argument model classes."""

    def test_value_argument_creation(self):
        """Ensures ValueArgument instances are created with correct attributes."""
        arg = ValueArgument(
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

    def test_boolean_argument_creation(self):
        """Ensures BooleanArgument instances are created with correct attributes."""
        arg = BooleanArgument(
            name="verbose", prefix="-", help="Enable verbose mode.", is_deprecated=True
        )
        assert arg.name == "verbose"
        assert arg.prefix == "-"
        assert arg.help == "Enable verbose mode."
        assert arg.is_deprecated is True
        assert arg.action == "store_true"
        assert arg.string_entity == "-verbose"

    def test_input_argument_creation(self):
        """Ensures InputArgument instances are created with correct attributes."""
        arg = InputArgument(
            name="file", value="/path/to/file", founder_class=ValueArgument
        )
        assert arg.name == "file"
        assert arg.value == "/path/to/file"
        assert arg.founder_class is ValueArgument


class TestArgSpace:
    """Tests for the ArgSpace class, which holds parsed argument values."""

    @pytest.fixture
    def mock_arguments(self) -> list[InputArgument]:
        """Provides a list of mock InputArgument objects for testing."""
        return [
            InputArgument(name="arg1", value="val1", founder_class=ValueArgument),
            InputArgument(name="arg2", value=True, founder_class=BooleanArgument),
            InputArgument(name="arg3", value="val3", founder_class=ValueArgument),
        ]

    @pytest.fixture
    def arg_space(self, mock_arguments: list[InputArgument]) -> ArgSpace:
        """Provides a pre-populated ArgSpace instance."""
        return ArgSpace(all_arguments=mock_arguments)

    def test_initialization(self, arg_space: ArgSpace, mock_arguments: list[InputArgument]):
        """Tests if ArgSpace is initialized correctly with a list of arguments."""
        assert len(arg_space.all_arguments) == 3
        assert arg_space.all_arguments == mock_arguments

    def test_get_by_name(self, arg_space: ArgSpace, mock_arguments: list[InputArgument]):
        """Tests retrieving an argument by its name."""
        found_arg = arg_space.get_by_name("arg1")
        assert found_arg is not None
        assert found_arg == mock_arguments[0]

    def test_get_by_name_not_found(self, arg_space: ArgSpace):
        """Tests that get_by_name returns None for a non-existent argument."""
        found_arg = arg_space.get_by_name("non_existent_arg")
        assert found_arg is None

    def test_get_by_type(self, arg_space: ArgSpace, mock_arguments: list[InputArgument]):
        """Tests retrieving arguments based on their founder class type."""
        value_args = arg_space.get_by_type(ValueArgument)
        assert len(value_args) == 2
        assert mock_arguments[0] in value_args
        assert mock_arguments[2] in value_args

        bool_args = arg_space.get_by_type(BooleanArgument)
        assert len(bool_args) == 1
        assert mock_arguments[1] in bool_args

    def test_get_by_type_not_found(self, arg_space: ArgSpace):
        """Tests that get_by_type returns an empty list for an unused argument type."""
        class OtherArgument(BaseArgument):
            pass
        other_args = arg_space.get_by_type(OtherArgument)
        assert other_args == []

    def test_from_namespace(self):
        """Tests the class method for creating an ArgSpace from an argparse.Namespace."""
        namespace = Namespace(config="config.json", debug=True, verbose=False)
        processed_args = [
            ValueArgument(name="config", prefix="--"),
            BooleanArgument(name="debug", prefix="-"),
            BooleanArgument(name="verbose", prefix="-"),
        ]

        arg_space = ArgSpace.from_namespace(namespace, processed_args)
        assert len(arg_space.all_arguments) == 3

        config_arg = arg_space.get_by_name('config')
        debug_arg = arg_space.get_by_name('debug')

        assert config_arg is not None
        assert config_arg.value == "config.json"
        assert config_arg.founder_class is ValueArgument

        assert debug_arg is not None
        assert debug_arg.value is True
        assert debug_arg.founder_class is BooleanArgument


class TestArgParser:
    """Tests for the ArgParser class, which orchestrates argument parsing."""

    @pytest.fixture
    def value_arg(self) -> ValueArgument:
        """Provides a sample ValueArgument."""
        return ValueArgument(name="config", help="Path to config file", default="dev.json", is_required=False, possible_values=["dev.json", "prod.json"])

    @pytest.fixture
    def bool_arg(self) -> BooleanArgument:
        """Provides a sample BooleanArgument."""
        return BooleanArgument(name="debug", help="Enable debug mode")

    @pytest.fixture
    def processed_args(self, value_arg: ValueArgument, bool_arg: BooleanArgument) -> list:
        """Provides a list of processed arguments."""
        return [value_arg, bool_arg]

    def test_initialization(self, processed_args: list):
        """Tests that the ArgParser constructor correctly assigns attributes."""
        parser = ArgParser(
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

    def test_register_args(self, mocker, value_arg: ValueArgument, bool_arg: BooleanArgument):
        """Tests that arguments are correctly registered with the underlying ArgumentParser."""
        mock_add_argument = mocker.patch("argparse.ArgumentParser.add_argument")

        parser = ArgParser(processed_args=[value_arg, bool_arg])

        expected_calls = [
            # Call for the ValueArgument
            call(
                value_arg.string_entity,
                action=value_arg.action,
                help=value_arg.help,
                default=value_arg.default,
                choices=value_arg.possible_values,
                required=value_arg.is_required,
                deprecated=value_arg.is_deprecated
            ),
            # Call for the BooleanArgument
            call(
                bool_arg.string_entity,
                action=bool_arg.action,
                help=bool_arg.help,
                deprecated=bool_arg.is_deprecated
            )
        ]
        mock_add_argument.assert_has_calls(expected_calls, any_order=True)

    def test_parse_args_populates_argspace(self, mocker, processed_args: list):
        """Tests that _parse_args correctly calls the parser and populates the ArgSpace."""
        # 1. Mock the return value of the internal argparse instance
        mock_namespace = Namespace(config='config.json', debug=True)
        mocker.patch(
            'argparse.ArgumentParser.parse_args',
            return_value=mock_namespace
        )

        # 2. Initialize the parser and call the method under test
        parser = ArgParser(processed_args=processed_args)
        parser._parse_args()  # Test the private method that contains the logic

        # 3. Assert the results
        arg_space = parser.parsed_argspace
        assert isinstance(arg_space, ArgSpace)
        assert len(arg_space.all_arguments) == 2

        config_arg = arg_space.get_by_name('config')
        debug_arg = arg_space.get_by_name('debug')

        assert config_arg is not None
        assert config_arg.value == 'config.json'
        assert config_arg.founder_class is ValueArgument

        assert debug_arg is not None
        assert debug_arg.value is True
        assert debug_arg.founder_class is BooleanArgument
