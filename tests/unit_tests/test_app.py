from argenta.command.models import InputCommand, Command
from argenta.app import App

import unittest


class MyTestCase(unittest.TestCase):
    def test_is_exit_command1(self):
        app = App()
        self.assertEqual(app._is_exit_command(InputCommand('q')), True)

    def test_is_exit_command5(self):
        app = App()
        self.assertEqual(app._is_exit_command(InputCommand('Q')), True)

    def test_is_exit_command2(self):
        app = App(ignore_command_register=False)
        self.assertEqual(app._is_exit_command(InputCommand('q')), False)

    def test_is_exit_command3(self):
        app = App(exit_command=Command('quit'))
        self.assertEqual(app._is_exit_command(InputCommand('quit')), True)

    def test_is_exit_command4(self):
        app = App(exit_command=Command('quit'))
        self.assertEqual(app._is_exit_command(InputCommand('qUIt')), True)

    def test_is_exit_command6(self):
        app = App(ignore_command_register=False,
                  exit_command=Command('quit'))
        self.assertEqual(app._is_exit_command(InputCommand('qUIt')), False)

    def test_is_unknown_command1(self):
        app = App()
        app.set_unknown_command_handler(lambda command: None)
        app._all_registered_triggers_in_lower_case = ['fr', 'tr', 'de']
        self.assertEqual(app._is_unknown_command(InputCommand('fr')), False)

    def test_is_unknown_command2(self):
        app = App()
        app.set_unknown_command_handler(lambda command: None)
        app._all_registered_triggers_in_lower_case = ['fr', 'tr', 'de']
        self.assertEqual(app._is_unknown_command(InputCommand('cr')), True)

    def test_is_unknown_command3(self):
        app = App(ignore_command_register=False)
        app.set_unknown_command_handler(lambda command: None)
        app._all_registered_triggers_in_default_case = ['Pr', 'tW', 'deQW']
        self.assertEqual(app._is_unknown_command(InputCommand('pr')), True)

    def test_is_unknown_command4(self):
        app = App(ignore_command_register=False)
        app.set_unknown_command_handler(lambda command: None)
        app._all_registered_triggers_in_default_case = ['Pr', 'tW', 'deQW']
        self.assertEqual(app._is_unknown_command(InputCommand('tW')), False)


















