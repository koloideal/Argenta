from argenta.command.models import InputCommand
from argenta.command.exceptions import (UnprocessedInputFlagException,
                                        RepeatedInputFlagsException,
                                        EmptyInputCommandException)

import unittest


class TestInputCommand(unittest.TestCase):
    def test_parse_correct_raw_command(self):
        self.assertEqual(InputCommand.parse_input_command('ssh --host 192.168.0.3').get_trigger(), 'ssh')

    def test_parse_raw_command_without_flag_name_with_value(self):
        with self.assertRaises(UnprocessedInputFlagException):
            InputCommand.parse_input_command('ssh 192.168.0.3')

    def test_parse_raw_command_with_repeated_flag_name(self):
        with self.assertRaises(RepeatedInputFlagsException):
            InputCommand.parse_input_command('ssh --host 192.168.0.3 --host 172.198.0.43')

    def test_parse_empty_raw_command(self):
        with self.assertRaises(EmptyInputCommandException):
            InputCommand.parse_input_command('')

