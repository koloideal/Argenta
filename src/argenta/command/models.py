import shlex
from collections.abc import Iterable
from typing import Literal, Never, Self

from argenta.command import Flags, InputFlags
from argenta.command.exceptions import (
    EmptyInputCommandException,
    RepeatedInputFlagsException,
    UnprocessedInputFlagException,
)
from argenta.command.flag.models import Flag, InputFlag, ValidationStatus

ParseFlagsResult = tuple[InputFlags, str | None, str | None]
ParseResult = tuple[str, InputFlags]

PREFIX_TYPE = Literal["-", "--", "---"]
MIN_FLAG_PREFIX: PREFIX_TYPE = "-"


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
        :param trigger: A string trigger, which, when entered by the user,
               indicates that the input corresponds to the command
        :param description: the description of the command
        :param flags: processed commands
        :param aliases: string synonyms for the main trigger
        """
        pretty_flags: Flags
        if isinstance(flags, Flags):
            pretty_flags = flags
        elif flags:
            pretty_flags = Flags([flags])
        else:
            pretty_flags = Flags()
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
        registered_flag = self._paired_string_entity_flag.get(flag.string_entity)
        if registered_flag:
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
        if isinstance(input_flags, InputFlags):
            self.input_flags: InputFlags = input_flags
        elif input_flags:
            self.input_flags = InputFlags([input_flags])
        else:
            self.input_flags = InputFlags()

    @classmethod
    def parse(cls, raw_command: str) -> Self:
        """
        Private. Parse the raw input command
        :param raw_command: raw input command
        :return: model of the input command, after parsing as InputCommand
        """
        tokens = _tokenize_command(raw_command)

        if not tokens:
            raise EmptyInputCommandException

        return cls(tokens[0], input_flags=_parse_flag_tokens(tokens[1:]))


def _tokenize_command(raw_command: str) -> list[str]:
    lexer = shlex.shlex(raw_command, posix=True)
    lexer.whitespace_split = True
    lexer.commenters = ""

    try:
        return list(lexer)
    except ValueError as error:
        raise UnprocessedInputFlagException from error


def _parse_flag_tokens(tokens: list[str]) -> InputFlags:
    flags: InputFlags = InputFlags()
    token_index = 0

    while token_index < len(tokens):
        input_flag, token_index = _parse_flag_token(tokens, token_index)

        if input_flag in flags:
            raise RepeatedInputFlagsException(input_flag)

        flags.add_flag(input_flag)

    return flags


def _split_flag_prefix(token: str) -> tuple[PREFIX_TYPE, str]:
    if token.startswith("---"):
        return "---", token[3:]
    if token.startswith("--"):
        return "--", token[2:]
    if token.startswith(MIN_FLAG_PREFIX):
        return MIN_FLAG_PREFIX, token[1:]
    raise UnprocessedInputFlagException


def _parse_flag_token(tokens: list[str], token_index: int) -> tuple[InputFlag, int]:
    prefix, name = _split_flag_prefix(tokens[token_index])

    next_index = token_index + 1
    if next_index < len(tokens) and not tokens[next_index].startswith(MIN_FLAG_PREFIX):
        input_flag = InputFlag(name=name, prefix=prefix, input_value=tokens[next_index])
        return input_flag, token_index + 2

    input_flag = InputFlag(name=name, prefix=prefix, input_value="")
    return input_flag, token_index + 1
