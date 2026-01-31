from argenta.app.dividing_line import DynamicDividingLine, StaticDividingLine


# ============================================================================
# Tests for StaticDividingLine - full line generation
# ============================================================================


def test_static_dividing_line_generates_default_length_with_override() -> None:
    line = StaticDividingLine('-')
    assert line.get_full_static_line(is_override=True).count('-') == 25


def test_static_dividing_line_generates_custom_length_with_formatting() -> None:
    line = StaticDividingLine('-', length=5)
    assert line.get_full_static_line(is_override=False) == '[dim]-----[/dim]'


# ============================================================================
# Tests for StaticDividingLine - unit part extraction
# ============================================================================


def test_static_dividing_line_returns_space_for_empty_unit() -> None:
    line = StaticDividingLine('')
    assert line.get_unit_part() == ' '


def test_static_dividing_line_returns_first_character_as_unit() -> None:
    line = StaticDividingLine('+-0987654321!@#$%^&*()_')
    assert line.get_unit_part() == '+'


# ============================================================================
# Tests for DynamicDividingLine - full line generation
# ============================================================================


def test_dynamic_dividing_line_generates_line_with_specified_length_and_override() -> None:
    line = DynamicDividingLine()
    assert line.get_full_dynamic_line(length=20, is_override=True).count('-') == 20


def test_dynamic_dividing_line_generates_line_with_specified_length_and_formatting() -> None:
    line = DynamicDividingLine()
    assert line.get_full_dynamic_line(length=5, is_override=False) == '[dim]-----[/dim]'


# ============================================================================
# Tests for DynamicDividingLine - unit part extraction
# ============================================================================


def test_dynamic_dividing_line_returns_space_for_empty_unit() -> None:
    line = DynamicDividingLine('')
    assert line.get_unit_part() == ' '


def test_dynamic_dividing_line_returns_first_character_as_unit() -> None:
    line = DynamicDividingLine('45n352834528&^%@&*T$G')
    assert line.get_unit_part() == '4'
