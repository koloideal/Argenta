from argenta.command.flag import Flag, FlagsGroup

import unittest


class TestFlagsGroup(unittest.TestCase):
    def test_get_flags(self):
        flags = FlagsGroup()
        list_of_flags = [
            Flag('test1'),
            Flag('test2'),
            Flag('test3'),
        ]
        flags.add_flags(list_of_flags)
        self.assertEqual(flags.get_flags(),
                         list_of_flags)

    def test_add_flag(self):
        flags = FlagsGroup()
        flags.add_flag(Flag('test'))
        self.assertEqual(len(flags.get_flags()), 1)

    def test_add_flags(self):
        flags = FlagsGroup()
        flags.add_flags([Flag('test'), Flag('test2')])
        self.assertEqual(len(flags.get_flags()), 2)

    def test_unparse_flags_to_dict(self):
        list_of_flags = [
            Flag('test1'),
            Flag('test2'),
            Flag('test3'),
        ]
        flags = FlagsGroup(*list_of_flags)
        serialized_flags = flags.unparse_to_dict()
        needed_result = {'test1': {'name': 'test1',
                                   'prefix': '--',
                                   'string_entity': '--test1',
                                   'value': None},
                         'test2': {'name': 'test2',
                                   'prefix': '--',
                                   'string_entity': '--test2',
                                   'value': None},
                         'test3': {'name': 'test3',
                                   'prefix': '--',
                                   'string_entity': '--test3',
                                   'value': None}}

        self.assertDictEqual(serialized_flags, needed_result)
