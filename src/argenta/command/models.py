__all__ = ["Command", "InputCommand"]

import shlex
from typing import Literal, Never, Self, cast, Iterable

from argenta.command.exceptions import (
    EmptyInputCommandException,
    RepeatedInputFlagsException,
    UnprocessedInputFlagException,
)
from argenta.command import Flags, InputFlags
from argenta.command.flag.models import Flag, InputFlag, ValidationStatus

ParseFlagsResult = tuple[InputFlags, str | None, str | None]
ParseResult = tuple[str, InputFlags]

MIN_FLAG_PREFIX: str = "-"
PREFIX_TYPE = Literal["-", "--", "---"]


class Command:
    def __init__(
        self,
        trigger: str,
        *,
        description: str = "Some useful command",
        flags: Flag | Flags | None = None,
        aliases: Iterable[str] | None = None,
    ):
        """
        Public. The command that can and should be registered in the Router
        :param trigger: A string trigger, which, when entered by the user, indicates that the input corresponds to the command
        :param description: the description of the command
        :param flags: processed commands
        :param aliases: string synonyms for the main trigger
        """
        pretty_flags: Flags = (
            flags if isinstance(flags, Flags)
            else Flags([flags])
            if flags is not None
            else Flags()
        )
        self.registered_flags: Flags = pretty_flags
        self.trigger: str = trigger
        self.description: str = description
        self.aliases: Iterable[str] | Iterable[Never] = aliases or set()

        self._paired_string_entity_flag: dict[str, Flag] = {
            flag.string_entity: flag for flag in pretty_flags
        }

    def validate_input_flag(self, flag: InputFlag) -> ValidationStatus:
        """
        Private. Validates the input flag
        :param flag: input flag for validation
        :return: is input flag valid as bool
        """
        if registered_flag := self._paired_string_entity_flag.get(flag.string_entity):
            is_valid = registered_flag.validate_input_flag_value(flag.input_value)
            if is_valid:
                return ValidationStatus.VALID
            else:
                return ValidationStatus.INVALID
        return ValidationStatus.UNDEFINED


class InputCommand:
    def __init__(
        self,
        trigger: str,
        *,
        input_flags: InputFlag | InputFlags | None = None,
    ):
        """
        Private. The model of the input command, after parsing
        :param trigger:the trigger of the command
        :param input_flags: the input flags
        :return: None
        """
        self.trigger: str = trigger
        self.input_flags: InputFlags = (
            input_flags
            if isinstance(input_flags, InputFlags)
            else InputFlags([input_flags])
            if input_flags is not None
            else InputFlags()
        )

    @classmethod
    def parse(cls, raw_command: str) -> Self:
        """
        Private. Parse the raw input command
        :param raw_command: raw input command
        :return: model of the input command, after parsing as InputCommand
        """
        lexer = shlex.shlex(raw_command, posix=True)
        lexer.whitespace_split = True
        lexer.commenters = ""

        try:
            tokens = list(lexer)
        except ValueError as e:
            raise UnprocessedInputFlagException from e

        if not tokens:
            raise EmptyInputCommandException

        command = tokens[0]
        flags: InputFlags = InputFlags()

        i = 1
        while i < len(tokens):
            token = tokens[i]

            if token.startswith("---"):
                prefix = "---"
                name = token[3:]
            elif token.startswith("--"):
                prefix = "--"
                name = token[2:]
            elif token.startswith("-"):
                prefix = "-"
                name = token[1:]
            else:
                raise UnprocessedInputFlagException

            if i + 1 < len(tokens) and not tokens[i + 1].startswith("-"):
                input_value = tokens[i + 1]
                i += 2
            else:
                input_value = ""
                i += 1

            input_flag = InputFlag(
                name=name,
                prefix=cast(PREFIX_TYPE, prefix),  # pyright: ignore[reportUnnecessaryCast]
                input_value=input_value,
                status=None,
            )

            if input_flag in flags:
                raise RepeatedInputFlagsException(input_flag)

            flags.add_flag(input_flag)

        return cls(command, input_flags=flags)
