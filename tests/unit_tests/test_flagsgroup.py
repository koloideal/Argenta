from argenta.command.flag.models import Flag, Flags

import unittest


class TestFlags(unittest.TestCase):
    def test_get_flags(self):
        flags = Flags()
        list_of_flags = [
            Flag('test1'),
            Flag('test2'),
            Flag('test3'),
        ]
        flags.add_flags(list_of_flags)
        self.assertEqual(flags.get_flags(),
                         list_of_flags)

    def test_add_flag(self):
        flags = Flags()
        flags.add_flag(Flag('test'))
        self.assertEqual(len(flags.get_flags()), 1)

    def test_add_flags(self):
        flags = Flags()
        flags.add_flags([Flag('test'), Flag('test2')])
        self.assertEqual(len(flags.get_flags()), 2)
