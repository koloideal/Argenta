import re

import pytest

from argenta.command.flag import Flag, InputFlag, PossibleValues
from argenta.command import Flags, InputFlags


# ============================================================================
# Tests for Flag - basic properties
# ============================================================================


def test_flag_string_entity_with_default_prefix() -> None:
    assert Flag(name='test').string_entity == '--test'


def test_flag_string_entity_with_custom_prefix() -> None:
    assert Flag(name='test', prefix='---').string_entity == '---test'


def test_flag_name_property() -> None:
    assert Flag(name='test').name == 'test'


def test_flag_prefix_property_default() -> None:
    assert Flag(name='test').prefix == '--'


def test_flag_prefix_property_custom() -> None:
    assert Flag(name='test', prefix='--').prefix == '--'


# ============================================================================
# Tests for Flag - string representations
# ============================================================================


def test_flag_str_representation() -> None:
    flag = Flag('two')
    assert str(flag) == '--two'


def test_flag_repr_representation() -> None:
    flag = Flag('two')
    assert repr(flag) == 'Flag<name=two, prefix=-->'


def test_flag_equality_with_non_flag_raises_error() -> None:
    flag = Flag('two')
    not_flag = object()
    with pytest.raises(NotImplementedError):
        flag == not_flag  # pyright: ignore[reportUnusedExpression]


# ============================================================================
# Tests for Flag - value validation with list of possible values
# ============================================================================


def test_flag_validates_value_in_allowed_list() -> None:
    flag = Flag(name='test', possible_values=['1', '2', '3'])
    assert flag.validate_input_flag_value('1') is True


def test_flag_rejects_value_not_in_allowed_list() -> None:
    flag = Flag(name='test', possible_values=['1', '2', '3'])
    assert flag.validate_input_flag_value('bad value') is False


# ============================================================================
# Tests for Flag - value validation with regex pattern
# ============================================================================


def test_flag_validates_value_matching_regex_pattern() -> None:
    flag = Flag(name='test', possible_values=re.compile(r'192.168.\d+.\d+'))
    assert flag.validate_input_flag_value('192.168.9.8') is True


def test_flag_rejects_value_not_matching_regex_pattern() -> None:
    flag = Flag(name='test', possible_values=re.compile(r'192.168.\d+.\d+'))
    assert flag.validate_input_flag_value('152.123.9.8') is False


# ============================================================================
# Tests for Flag - value validation with NEITHER and ALL
# ============================================================================


def test_flag_validates_empty_value_when_neither_allowed() -> None:
    flag = Flag(name='test', possible_values=PossibleValues.NEITHER)
    assert flag.validate_input_flag_value('') is True


def test_flag_rejects_non_empty_value_when_neither_allowed() -> None:
    flag = Flag(name='test', possible_values=PossibleValues.NEITHER)
    assert flag.validate_input_flag_value('random value') is False


def test_flag_validates_any_value_when_all_allowed() -> None:
    flag = Flag(name='test', possible_values=PossibleValues.ALL)
    assert flag.validate_input_flag_value('random value') is True


# ============================================================================
# Tests for InputFlag - basic properties
# ============================================================================


def test_input_flag_stores_empty_value() -> None:
    assert InputFlag(name='test', input_value='', status=None).input_value == ''


def test_input_flag_stores_provided_value() -> None:
    flag = InputFlag(name='test', input_value='example', status=None)
    assert flag.input_value == 'example'


# ============================================================================
# Tests for InputFlag - string representations
# ============================================================================


def test_input_flag_str_representation() -> None:
    flag = InputFlag('two', input_value='value')
    assert str(flag) == '--two value'


def test_input_flag_repr_representation() -> None:
    flag = InputFlag('two', input_value='some_value')
    assert repr(flag) == 'InputFlag<name=two, prefix=--, value=some_value, status=None>'


def test_input_flag_equality_with_non_flag_raises_error() -> None:
    flag = InputFlag('two', input_value='')
    not_flag = object()
    with pytest.raises(NotImplementedError):
        flag == not_flag  # pyright: ignore[reportUnusedExpression]


# ============================================================================
# Tests for InputFlags collection - retrieval
# ============================================================================


def test_input_flags_get_by_name_finds_single_flag() -> None:
    flag = InputFlag(name='test', input_value='', status=None)
    input_flags = InputFlags([flag])
    assert input_flags.get_flag_by_name('test') == flag


def test_input_flags_get_by_name_finds_flag_in_multiple() -> None:
    flag = InputFlag(name='test', input_value='', status=None)
    flag2 = InputFlag(name='some', input_value='', status=None)
    input_flags = InputFlags([flag, flag2])
    assert input_flags.get_flag_by_name('some') == flag2


def test_input_flags_get_by_name_returns_none_for_missing_flag() -> None:
    flag = InputFlag(name='test', input_value='', status=None)
    flag2 = InputFlag(name='some', input_value='', status=None)
    input_flags = InputFlags([flag, flag2])
    assert input_flags.get_flag_by_name('case') is None


def test_input_flags_get_by_name_with_status_finds_matching_flag() -> None:
    from argenta.command.flag import ValidationStatus
    
    flag1 = InputFlag(name='test', input_value='valid', status=ValidationStatus.VALID)
    flag2 = InputFlag(name='other', input_value='invalid', status=ValidationStatus.INVALID)
    input_flags = InputFlags([flag1, flag2])
    
    result = input_flags.get_flag_by_name('test', with_status=ValidationStatus.VALID)
    assert result == flag1


def test_input_flags_get_by_name_with_status_returns_none_when_status_mismatch() -> None:
    from argenta.command.flag import ValidationStatus
    
    flag = InputFlag(name='test', input_value='value', status=ValidationStatus.VALID)
    input_flags = InputFlags([flag])
    
    result = input_flags.get_flag_by_name('test', with_status=ValidationStatus.INVALID)
    assert result is None


def test_input_flags_get_by_name_with_status_returns_default_when_not_found() -> None:
    from argenta.command.flag import ValidationStatus
    
    flag = InputFlag(name='test', input_value='value', status=ValidationStatus.VALID)
    input_flags = InputFlags([flag])
    
    result = input_flags.get_flag_by_name('missing', with_status=ValidationStatus.VALID, default='default_value')
    assert result == 'default_value'


def test_input_flags_get_by_name_with_status_filters_by_both_name_and_status() -> None:
    from argenta.command.flag import ValidationStatus
    
    flag1 = InputFlag(name='test', input_value='value1', status=ValidationStatus.VALID)
    flag2 = InputFlag(name='test', input_value='value2', status=ValidationStatus.INVALID)
    flag3 = InputFlag(name='other', input_value='value3', status=ValidationStatus.VALID)
    input_flags = InputFlags([flag1, flag2, flag3])
    
    result = input_flags.get_flag_by_name('test', with_status=ValidationStatus.INVALID)
    assert result == flag2


# ============================================================================
# Tests for InputFlags collection - equality and containment
# ============================================================================


def test_input_flags_not_equal_when_different_length() -> None:
    flags = InputFlags([InputFlag('some', input_value='')])
    flags2 = InputFlags([
        InputFlag('some', input_value=''), 
        InputFlag('some2', input_value='')
    ])
    assert flags != flags2


def test_input_flags_not_equal_to_non_input_flags() -> None:
    flags = InputFlags([InputFlag('some', input_value='')])
    not_flags = object()
    assert flags != not_flags


def test_input_flags_contains_existing_flag() -> None:
    flag = InputFlag('some', input_value='')
    flags = InputFlags([flag])
    assert flag in flags


def test_input_flags_does_not_contain_missing_flag() -> None:
    flags = InputFlags([InputFlag('some', input_value='')])
    flag = InputFlag('nonexists', input_value='')
    assert flag not in flags


def test_input_flags_contains_raises_error_for_non_flag() -> None:
    flags = InputFlags([InputFlag('some', input_value='')])
    not_flag = object
    with pytest.raises(TypeError):
        not_flag in flags  # pyright: ignore[reportUnusedExpression]


# ============================================================================
# Tests for Flags collection - adding flags
# ============================================================================


def test_flags_add_single_flag() -> None:
    flags = Flags()
    flags.add_flag(Flag('test'))
    assert len(flags.flags) == 1


def test_flags_add_multiple_flags() -> None:
    flags = Flags()
    flags.add_flags([Flag('test'), Flag('test2')])
    assert len(flags.flags) == 2


def test_flags_stores_added_flags() -> None:
    flags = Flags()
    list_of_flags = [
        Flag('test1'),
        Flag('test2'),
        Flag('test3'),
    ]
    flags.add_flags(list_of_flags)
    assert flags.flags == list_of_flags


# ============================================================================
# Tests for Flags collection - retrieval
# ============================================================================


def test_flags_get_by_name_finds_flag() -> None:
    flags = Flags([Flag('some')])
    assert flags.get_flag_by_name('some') == Flag('some')


# ============================================================================
# Tests for Flags collection - equality and containment
# ============================================================================


def test_flags_equal_when_same_flags() -> None:
    flags = Flags([Flag('some')])
    flags2 = Flags([Flag('some')])
    assert flags == flags2


def test_flags_not_equal_when_different_flags() -> None:
    flags = Flags([Flag('some')])
    flags2 = Flags([Flag('other')])
    assert flags != flags2


def test_flags_not_equal_when_different_length() -> None:
    flags = Flags([Flag('some')])
    flags2 = Flags([Flag('some'), Flag('other')])
    assert flags != flags2


def test_flags_not_equal_to_non_flags() -> None:
    flags = Flags([Flag('some')])
    not_flags = object()
    assert flags != not_flags


def test_flags_contains_existing_flag() -> None:
    flags = Flags([Flag('some')])
    flag = Flag('some')
    assert flag in flags


def test_flags_does_not_contain_missing_flag() -> None:
    flags = Flags([Flag('some')])
    flag = Flag('nonexists')
    assert flag not in flags


def test_flags_contains_raises_error_for_non_flag() -> None:
    flags = Flags([Flag('some')])
    not_flag = object
    with pytest.raises(TypeError):
        not_flag in flags  # pyright: ignore[reportUnusedExpression]


# ============================================================================
# Tests for Flags collection - special methods
# ============================================================================


def test_flags_len_returns_count() -> None:
    flags = Flags([Flag('one'), Flag('two')])
    assert len(flags) == 2


def test_flags_bool_returns_true_when_not_empty() -> None:
    flags = Flags([Flag('one'), Flag('two')])
    assert bool(flags)


def test_flags_bool_returns_false_when_empty() -> None:
    flags = Flags([])
    assert not bool(flags)


def test_flags_getitem_returns_flag_at_index() -> None:
    flags = Flags([Flag('one'), Flag('two')])
    assert flags[1] == Flag('two')
