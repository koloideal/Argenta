import re

from argenta.command.flag import Flag, InputFlag, PossibleValues
from argenta.command.flag.flags import Flags, InputFlags


def test_get_string_entity():
    assert Flag(name='test').string_entity == '--test'


def test_get_string_entity2():
    assert Flag(name='test', prefix='---').string_entity == '---test'


def test_get_flag_name():
    assert Flag(name='test').name == 'test'


def test_get_flag_prefix():
    assert Flag(name='test').prefix == '--'


def test_get_flag_prefix2():
    assert Flag(name='test', prefix='--').prefix == '--'


def test_get_flag_value_without_set():
    assert InputFlag(name='test', input_value='', status=None).input_value == ''


def test_get_flag_value_with_set():
    flag = InputFlag(name='test', input_value='example', status=None)
    assert flag.input_value == 'example'


def test_validate_incorrect_flag_value_with_list_of_possible_flag_values():
    flag = Flag(name='test', possible_values=['1', '2', '3'])
    assert flag.validate_input_flag_value('bad value') is False


def test_validate_correct_flag_value_with_list_of_possible_flag_values():
    flag = Flag(name='test', possible_values=['1', '2', '3'])
    assert flag.validate_input_flag_value('1') is True


def test_validate_incorrect_flag_value_with_pattern_of_possible_flag_values():
    flag = Flag(name='test', possible_values=re.compile(r'192.168.\d+.\d+'))
    assert flag.validate_input_flag_value('152.123.9.8') is False


def test_validate_correct_flag_value_with_pattern_of_possible_flag_values():
    flag = Flag(name='test', possible_values=re.compile(r'192.168.\d+.\d+'))
    assert flag.validate_input_flag_value('192.168.9.8') is True


def test_validate_correct_empty_flag_value_without_possible_flag_values():
    flag = Flag(name='test', possible_values=PossibleValues.NEITHER)
    assert flag.validate_input_flag_value('') is True


def test_validate_correct_empty_flag_value_with_possible_flag_values():
    flag = Flag(name='test', possible_values=PossibleValues.NEITHER)
    assert flag.validate_input_flag_value('') is True


def test_validate_incorrect_random_flag_value_without_possible_flag_values():
    flag = Flag(name='test', possible_values=PossibleValues.NEITHER)
    assert flag.validate_input_flag_value('random value') is False


def test_validate_correct_random_flag_value_with_possible_flag_values():
    flag = Flag(name='test', possible_values=PossibleValues.ALL)
    assert flag.validate_input_flag_value('random value') is True


def test_get_input_flag1():
    flag = InputFlag(name='test', input_value='', status=None)
    input_flags = InputFlags([flag])
    assert input_flags.get_flag_by_name('test') == flag


def test_get_input_flag2():
    flag = InputFlag(name='test', input_value='', status=None)
    flag2 = InputFlag(name='some', input_value='', status=None)
    input_flags = InputFlags([flag, flag2])
    assert input_flags.get_flag_by_name('some') == flag2


def test_get_undefined_input_flag():
    flag = InputFlag(name='test', input_value='', status=None)
    flag2 = InputFlag(name='some', input_value='', status=None)
    input_flags = InputFlags([flag, flag2])
    assert input_flags.get_flag_by_name('case') is None


def test_get_flags():
    flags = Flags()
    list_of_flags = [
        Flag('test1'),
        Flag('test2'),
        Flag('test3'),
    ]
    flags.add_flags(list_of_flags)
    assert flags.flags == list_of_flags


def test_add_flag():
    flags = Flags()
    flags.add_flag(Flag('test'))
    assert len(flags.flags) == 1


def test_add_flags():
    flags = Flags()
    flags.add_flags([Flag('test'), Flag('test2')])
    assert len(flags.flags) == 2
