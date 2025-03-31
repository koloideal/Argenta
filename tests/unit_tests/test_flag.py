from argenta.command.flag.models import Flag, InputFlag

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
        self.assertEqual(InputFlag(name='test').get_value(),
                         None)

    def test_get_flag_value_with_set(self):
        flag = InputFlag(name='test')
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






















