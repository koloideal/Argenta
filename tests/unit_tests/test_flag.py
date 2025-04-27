from argenta.command.flag.models import Flag, ValidInputFlag, InputFlags, Flags

import unittest
import re


class TestFlag(unittest.TestCase):
    def test_get_string_entity(self):
        self.assertEqual(Flag(name='test').get_string_entity(),
                         '--test')

    def test_get_string_entity2(self):
        self.assertEqual(Flag(name='test',
                              prefix='---').get_string_entity(),
                         '---test')

    def test_get_flag_name(self):
        self.assertEqual(Flag(name='test').get_name(),
                         'test')

    def test_get_flag_prefix(self):
        self.assertEqual(Flag(name='test').get_prefix(),
                         '--')

    def test_get_flag_prefix2(self):
        self.assertEqual(Flag(name='test',
                              prefix='--').get_prefix(),
                         '--')

    def test_get_flag_value_without_set(self):
        self.assertEqual(ValidInputFlag(name='test').get_value(),
                         None)

    def test_get_flag_value_with_set(self):
        flag = ValidInputFlag(name='test')
        flag.set_value('example')
        self.assertEqual(flag.get_value(), 'example')

    def test_validate_incorrect_flag_value_with_list_of_possible_flag_values(self):
        flag = Flag(name='test', possible_values=['1', '2', '3'])
        self.assertEqual(flag.validate_input_flag_value('bad value'), False)

    def test_validate_correct_flag_value_with_list_of_possible_flag_values(self):
        flag = Flag(name='test', possible_values=['1', '2', '3'])
        self.assertEqual(flag.validate_input_flag_value('1'), True)

    def test_validate_incorrect_flag_value_with_pattern_of_possible_flag_values(self):
        flag = Flag(name='test', possible_values=re.compile(r'192.168.\d+.\d+'))
        self.assertEqual(flag.validate_input_flag_value('152.123.9.8'), False)

    def test_validate_correct_flag_value_with_pattern_of_possible_flag_values(self):
        flag = Flag(name='test', possible_values=re.compile(r'192.168.\d+.\d+'))
        self.assertEqual(flag.validate_input_flag_value('192.168.9.8'), True)

    def test_validate_correct_empty_flag_value_without_possible_flag_values(self):
        flag = Flag(name='test', possible_values=False)
        self.assertEqual(flag.validate_input_flag_value(None), True)

    def test_validate_correct_empty_flag_value_with_possible_flag_values(self):
        flag = Flag(name='test', possible_values=True)
        self.assertEqual(flag.validate_input_flag_value(None), True)

    def test_validate_incorrect_random_flag_value_without_possible_flag_values(self):
        flag = Flag(name='test', possible_values=False)
        self.assertEqual(flag.validate_input_flag_value('random value'), False)

    def test_validate_correct_random_flag_value_with_possible_flag_values(self):
        flag = Flag(name='test', possible_values=True)
        self.assertEqual(flag.validate_input_flag_value('random value'), True)

    def test_get_input_flag1(self):
        flag = ValidInputFlag(name='test')
        input_flags = InputFlags(flag)
        self.assertEqual(input_flags.get_flag('test'), flag)

    def test_get_input_flag2(self):
        flag = ValidInputFlag(name='test')
        flag2 = ValidInputFlag(name='some')
        input_flags = InputFlags(flag, flag2)
        self.assertEqual(input_flags.get_flag('some'), flag2)

    def test_get_undefined_input_flag(self):
        flag = ValidInputFlag(name='test')
        flag2 = ValidInputFlag(name='some')
        input_flags = InputFlags(flag, flag2)
        self.assertEqual(input_flags.get_flag('case'), None)

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






















