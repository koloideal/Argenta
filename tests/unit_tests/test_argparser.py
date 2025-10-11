import unittest
from unittest.mock import MagicMock, patch
from argparse import Namespace

from argenta.orchestrator.argparser.entity import ArgParser, ArgSpace
from argenta.orchestrator.argparser.arguments.models import (
    ValueArgument,
    BooleanArgument,
    InputArgument,
    BaseArgument
)


class TestArgumentClasses(unittest.TestCase):
    def test_value_argument_creation(self):
        arg = ValueArgument(
            name="test_arg",
            prefix="--",
            help="A test argument.",
            possible_values=["one", "two"],
            default="one",
            is_required=True,
            is_deprecated=False
        )
        self.assertEqual(arg.name, "test_arg")
        self.assertEqual(arg.prefix, "--")
        self.assertEqual(arg.help, "A test argument.")
        self.assertEqual(arg.possible_values, ["one", "two"])
        self.assertEqual(arg.default, "one")
        self.assertTrue(arg.is_required)
        self.assertFalse(arg.is_deprecated)
        self.assertEqual(arg.action, "store")
        self.assertEqual(arg.string_entity, "--test_arg")

    def test_boolean_argument_creation(self):
        arg = BooleanArgument(
            name="verbose",
            prefix="-",
            help="Enable verbose mode.",
            is_deprecated=True
        )
        self.assertEqual(arg.name, "verbose")
        self.assertEqual(arg.prefix, "-")
        self.assertEqual(arg.help, "Enable verbose mode.")
        self.assertTrue(arg.is_deprecated)
        self.assertEqual(arg.action, "store_true")
        self.assertEqual(arg.string_entity, "-verbose")

    def test_input_argument_creation(self):
        arg = InputArgument(
            name="file",
            value="/path/to/file",
            founder_class=ValueArgument
        )
        self.assertEqual(arg.name, "file")
        self.assertEqual(arg.value, "/path/to/file")
        self.assertEqual(arg.founder_class, ValueArgument)


class TestArgParser(unittest.TestCase):
    def setUp(self):
        self.value_arg = ValueArgument(name="config", help="Path to config file")
        self.bool_arg = BooleanArgument(name="debug", help="Enable debug mode")
        self.processed_args = [self.value_arg, self.bool_arg]

    def test_argparser_initialization(self):
        parser = ArgParser(
            processed_args=self.processed_args,
            name="TestApp",
            description="A test application.",
            epilog="Test epilog."
        )
        self.assertEqual(parser.name, "TestApp")
        self.assertEqual(parser.description, "A test application.")
        self.assertEqual(parser.epilog, "Test epilog.")
        self.assertEqual(parser.processed_args, self.processed_args)

    @patch('argenta.orchestrator.argparser.entity.ArgumentParser.parse_args')
    def test_parse_args(self, mock_parse_args: MagicMock):
        mock_namespace = Namespace(config='config.json', debug=True)
        mock_parse_args.return_value = mock_namespace

        parser = ArgParser(processed_args=self.processed_args)
        arg_space = parser.parse_args()

        self.assertIsInstance(arg_space, ArgSpace)
        self.assertEqual(len(arg_space.all_arguments), 2)

        config_arg = arg_space.get_by_name('config')
        debug_arg = arg_space.get_by_name('debug')

        self.assertIsNotNone(config_arg)
        if config_arg:
            self.assertEqual(config_arg.value, 'config.json')
            self.assertEqual(config_arg.founder_class, ValueArgument)

        self.assertIsNotNone(debug_arg)
        if debug_arg:
            self.assertTrue(debug_arg.value)
            self.assertEqual(debug_arg.founder_class, BooleanArgument)


class TestArgSpace(unittest.TestCase):
    def setUp(self):
        self.input_arg1 = InputArgument(name="arg1", value="val1", founder_class=ValueArgument)
        self.input_arg2 = InputArgument(name="arg2", value="val2", founder_class=BooleanArgument)
        self.input_arg3 = InputArgument(name="arg3", value="val3", founder_class=ValueArgument)
        self.arg_space = ArgSpace(all_arguments=[self.input_arg1, self.input_arg2, self.input_arg3])

    def test_argspace_initialization(self):
        self.assertEqual(len(self.arg_space.all_arguments), 3)
        self.assertIn(self.input_arg1, self.arg_space.all_arguments)
        self.assertIn(self.input_arg2, self.arg_space.all_arguments)
        self.assertIn(self.input_arg3, self.arg_space.all_arguments)

    def test_get_by_name(self):
        found_arg = self.arg_space.get_by_name("arg1")
        self.assertIsNotNone(found_arg)
        if found_arg:
            self.assertEqual(found_arg, self.input_arg1)

    def test_get_by_name_not_found(self):
        found_arg = self.arg_space.get_by_name("non_existent_arg")
        self.assertIsNone(found_arg)

    def test_get_by_type(self):
        value_args = self.arg_space.get_by_type(ValueArgument)
        self.assertEqual(len(value_args), 2)
        self.assertIn(self.input_arg1, value_args)
        self.assertIn(self.input_arg3, value_args)

        bool_args = self.arg_space.get_by_type(BooleanArgument)
        self.assertEqual(len(bool_args), 1)
        self.assertIn(self.input_arg2, bool_args)

    def test_get_by_type_not_found(self):
        class OtherArgument(BaseArgument):
            pass

        other_args = self.arg_space.get_by_type(OtherArgument)
        self.assertEqual(len(other_args), 0)

    def test_from_namespace(self):
        namespace = Namespace(arg1="val1", debug=True)
        processed_args = [
            ValueArgument(name="arg1", prefix="--"),
            BooleanArgument(name="debug", prefix="-")
        ]

        arg_space = ArgSpace.from_namespace(namespace, processed_args)
        self.assertEqual(len(arg_space.all_arguments), 2)

        arg1 = arg_space.get_by_name('arg1')
        debug_arg = arg_space.get_by_name('debug')

        self.assertIsNotNone(arg1)
        if arg1:
            self.assertEqual(arg1.value, "val1")
            self.assertEqual(arg1.founder_class, ValueArgument)

        self.assertIsNotNone(debug_arg)
        if debug_arg:
            self.assertTrue(debug_arg.value)
            self.assertEqual(debug_arg.founder_class, BooleanArgument)
