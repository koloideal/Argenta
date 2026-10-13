import re
import shlex
from contextlib import suppress

import pytest
from hypothesis import given
from hypothesis import strategies as st

from argenta.command.exceptions import (
    EmptyInputCommandException,
    InputCommandException,
    RepeatedInputFlagsException,
    UnprocessedInputFlagException,
)
from argenta.command.flag.models import Flag, PossibleValues
from argenta.command.models import InputCommand

# ============================================================================
# Strategies
# ============================================================================

PREFIXES = ["-", "--", "---"]

# A token is never a flag value if it looks like a flag itself,
# unless it is a negative number.
negative_numbers = st.from_regex(r"-\d+(\.\d+)?", fullmatch=True)

# Flag names must not start with "-": the longest-prefix rule in
# _split_flag_prefix would re-interpret them as a longer prefix.
flag_names = st.text(min_size=1).filter(lambda name: not name.startswith("-"))

# Values must not look like a flag token.
flag_values = st.one_of(
    negative_numbers,
    st.text().filter(lambda value: not value.startswith("-")),
)

_numeric_name = re.compile(r"\d+(\.\d+)?")

# A single-dash flag with a numeric name ("-5") is ambiguous: it is
# simultaneously flag "5" and a negative number, and the parser always
# consumes it as the previous flag's value — so it cannot round-trip.
flag_specs = st.lists(
    st.tuples(st.sampled_from(PREFIXES), flag_names, flag_values).filter(
        lambda spec: spec[0] != "-" or not _numeric_name.fullmatch(spec[1])
    ),
    # InputFlag equality is name-based, so equal names would raise
    # RepeatedInputFlagsException instead of round-tripping.
    unique_by=lambda spec: spec[1],
)


def _render_command(trigger: str, flags: list[tuple[str, str, str]]) -> str:
    parts = [shlex.quote(trigger)]
    for prefix, name, value in flags:
        parts.append(shlex.quote(prefix + name))
        if value:
            parts.append(shlex.quote(value))
    return " ".join(parts)


# ============================================================================
# InputCommand.parse — exception discipline
# ============================================================================


@given(raw=st.text())
def test_parse_never_raises_unexpected_exceptions(raw: str) -> None:
    with suppress(InputCommandException):
        InputCommand.parse(raw)


# shlex only treats " \t\n\r" as whitespace — e.g. NBSP or \f is a
# valid trigger, not an empty command.
shlex_whitespace = st.sampled_from(" \t\n\r")


@given(raw=st.text(alphabet=shlex_whitespace))
def test_parse_whitespace_only_raises_empty(raw: str) -> None:
    with pytest.raises(EmptyInputCommandException):
        InputCommand.parse(raw)


# ============================================================================
# InputCommand.parse — round-trip
# ============================================================================


@given(trigger=st.text(min_size=1), flags=flag_specs)
def test_parse_round_trips_quoted_tokens(trigger: str, flags: list[tuple[str, str, str]]) -> None:
    parsed = InputCommand.parse(_render_command(trigger, flags))

    assert parsed.trigger == trigger
    assert len(parsed.input_flags) == len(flags)
    for prefix, name, value in flags:
        flag = parsed.input_flags.get_flag_by_name(name)
        assert flag is not None
        assert flag.prefix == prefix
        assert flag.input_value == value


@given(trigger=st.text(min_size=1))
def test_parse_bare_trigger_has_no_flags(trigger: str) -> None:
    parsed = InputCommand.parse(shlex.quote(trigger))
    assert parsed.trigger == trigger
    assert len(parsed.input_flags) == 0


# ============================================================================
# InputCommand.parse — flag-token edge cases
# ============================================================================


@given(stray=st.text(min_size=1).filter(lambda token: not token.startswith("-")))
def test_parse_rejects_bare_token_as_flag(stray: str) -> None:
    with pytest.raises(UnprocessedInputFlagException):
        InputCommand.parse(f"cmd {shlex.quote(stray)}")


@given(
    stray=st.text(min_size=1).filter(lambda token: not token.startswith("-")),
    value=flag_values,
)
def test_parse_rejects_bare_token_after_flag_value(stray: str, value: str) -> None:
    command = f"cmd --flag {shlex.quote(value or 'x')} {shlex.quote(stray)}"
    with pytest.raises(UnprocessedInputFlagException):
        InputCommand.parse(command)


@given(
    # A numeric name would make "-N" look like a negative-number value
    # instead of a flag token.
    name=flag_names.filter(lambda name: not _numeric_name.fullmatch(name)),
    prefixes=st.tuples(st.sampled_from(PREFIXES), st.sampled_from(PREFIXES)).filter(
        lambda pair: pair[0] != pair[1]
    ),
)
def test_parse_rejects_same_flag_name_across_prefixes(name: str, prefixes: tuple[str, str]) -> None:
    command = f"cmd {shlex.quote(prefixes[0] + name)} {shlex.quote(prefixes[1] + name)}"
    with pytest.raises(RepeatedInputFlagsException):
        InputCommand.parse(command)


@given(value=negative_numbers)
def test_parse_consumes_negative_number_as_flag_value(value: str) -> None:
    parsed = InputCommand.parse(f"cmd --offset {value}")
    flag = parsed.input_flags.get_flag_by_name("offset")
    assert flag is not None
    assert flag.input_value == value


@given(
    suffix=st.text(
        min_size=1,
        alphabet=st.characters(blacklist_characters=".0123456789"),
    ).filter(lambda s: not s.startswith("-") and s != "first")
)
def test_parse_treats_dash_non_number_as_flag_not_value(suffix: str) -> None:
    parsed = InputCommand.parse(f"cmd --first {shlex.quote('-' + suffix)}")
    first = parsed.input_flags.get_flag_by_name("first")
    other = parsed.input_flags.get_flag_by_name(suffix)
    assert first is not None
    assert first.input_value == ""
    assert other is not None


# ============================================================================
# Flag.validate_input_flag_value
# ============================================================================


@given(value=st.text())
def test_possible_values_all_means_any_non_empty(value: str) -> None:
    assert Flag("f").validate_input_flag_value(value) == (value != "")


@given(value=st.text())
def test_possible_values_neither_means_only_empty(value: str) -> None:
    flag = Flag("f", possible_values=PossibleValues.NEITHER)
    assert flag.validate_input_flag_value(value) == (value == "")


@given(container=st.sets(st.text()), value=st.text())
def test_possible_values_container_means_membership(container: set[str], value: str) -> None:
    flag = Flag("f", possible_values=container)
    assert flag.validate_input_flag_value(value) == (value in container)


@given(value=st.text())
def test_possible_values_pattern_uses_match_semantics(value: str) -> None:
    flag = Flag("f", possible_values=re.compile(r"\d+"))
    assert flag.validate_input_flag_value(value) == bool(re.match(r"\d+", value))
