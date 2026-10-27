from argenta.repl import DynamicDividingLine, StaticDividingLine


def test_static_line_has_configured_length_and_unit() -> None:
    assert StaticDividingLine("=", length=10).line() == "=" * 10


def test_static_line_defaults() -> None:
    assert StaticDividingLine().line() == "-" * 25


def test_static_line_uses_only_first_unit_char() -> None:
    assert StaticDividingLine("abc", length=3).line() == "aaa"


def test_empty_unit_part_falls_back_to_space() -> None:
    assert StaticDividingLine("", length=4).line() == "    "


def test_dynamic_line_matches_longest_content_line() -> None:
    longest = "a much longer line of output here"
    assert DynamicDividingLine("-").line_for(f"short\n{longest}\n") == "-" * len(longest)


def test_dynamic_line_ignores_ansi_escapes() -> None:
    payload = "x" * 30
    assert DynamicDividingLine("-").line_for(f"\u001b[31m{payload}\u001b[0m") == "-" * 30


def test_dynamic_line_clamped_to_min_length() -> None:
    assert DynamicDividingLine("-").line_for("") == "-" * 10


def test_dynamic_line_clamped_to_max_length() -> None:
    assert DynamicDividingLine("-").line_for("y" * 500) == "-" * 100


def test_dynamic_line_custom_bounds() -> None:
    line = DynamicDividingLine("*", min_length=3, max_length=5)
    assert line.line_for("ab") == "***"
    assert line.line_for("abcdefgh") == "*****"
