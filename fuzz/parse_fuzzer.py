"""Atheris fuzz target for ``InputCommand.parse``.

Any exception other than the three documented parser errors is a bug and
should crash the fuzzer.
"""

import contextlib
import sys

import atheris

with atheris.instrument_imports(include=["argenta"]):
    from argenta.command.exceptions import (
        EmptyInputCommandException,
        RepeatedInputFlagsException,
        UnprocessedInputFlagException,
    )
    from argenta.command.models import InputCommand

EXPECTED_EXCEPTIONS = (
    EmptyInputCommandException,
    RepeatedInputFlagsException,
    UnprocessedInputFlagException,
)


@atheris.instrument_func
def test_one_input(data: bytes) -> None:
    fdp = atheris.FuzzedDataProvider(data)
    raw = fdp.ConsumeUnicodeNoSurrogates(256)
    with contextlib.suppress(*EXPECTED_EXCEPTIONS):
        InputCommand.parse(raw)


def main() -> None:
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
