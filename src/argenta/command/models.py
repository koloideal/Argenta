__all__ = ["Command", "InputCommand"]

from typing import Literal, Never, Self, cast

from argenta.command.exceptions import (
    EmptyInputCommandException,
    RepeatedInputFlagsException,
    UnprocessedInputFlagException,
)
from argenta.command.flag.flags.models import Flags, InputFlags
from argenta.command.flag.models import Flag, InputFlag, ValidationStatus

ParseFlagsResult = tuple[InputFlags, str | None, str | None]
ParseResult = tuple[str, InputFlags]

MIN_FLAG_PREFIX: str = "-"
DEFAULT_WITHOUT_FLAGS: Flags = Flags()
DEFAULT_WITHOUT_ALIASES: list[Never] = []

DEFAULT_WITHOUT_INPUT_FLAGS: InputFlags = InputFlags()


class Command:
    def __init__(
        self,
        trigger: str,
        *,
        description: str = "Some useful command",
        flags: Flag | Flags = DEFAULT_WITHOUT_FLAGS,
        aliases: list[str] | list[Never] = DEFAULT_WITHOUT_ALIASES,
    ):
        """
        Public. The command that can and should be registered in the Router
        :param trigger: A string trigger, which, when entered by the user, indicates that the input corresponds to the command
        :param description: the description of the command
        :param flags: processed commands
        :param aliases: string synonyms for the main trigger
        """
        self.registered_flags: Flags = flags if isinstance(flags, Flags) else Flags([flags])
        self.trigger: str = trigger
        self.description: str = description
        self.aliases: list[str] | list[Never] = aliases

    def validate_input_flag(self, flag: InputFlag) -> ValidationStatus:
        """
        Private. Validates the input flag
        :param flag: input flag for validation
        :return: is input flag valid as bool
        """
        registered_flags: Flags = self.registered_flags
        for registered_flag in registered_flags:
            if registered_flag.string_entity == flag.string_entity:
                is_valid = registered_flag.validate_input_flag_value(flag.input_value)
                if is_valid:
                    return ValidationStatus.VALID
                else:
                    return ValidationStatus.INVALID
        return ValidationStatus.UNDEFINED


class InputCommand:
    def __init__(self, trigger: str, *, input_flags: InputFlag | InputFlags = DEFAULT_WITHOUT_INPUT_FLAGS):
        """
        Private. The model of the input command, after parsing
        :param trigger:the trigger of the command
        :param input_flags: the input flags
        :return: None
        """
        self.trigger: str = trigger
        self.input_flags: InputFlags = (
            input_flags if isinstance(input_flags, InputFlags) else InputFlags([input_flags])
        )

    @classmethod
    def parse(cls, raw_command: str) -> Self:
        """
        Private. Parse the raw input command
        :param raw_command: raw input command
        :return: model of the input command, after parsing as InputCommand
        """
        trigger, input_flags = CommandParser(raw_command).parse_raw_command()

        return cls(trigger=trigger, input_flags=input_flags)


class CommandParser:
    def __init__(self, raw_command: str) -> None:
        self.raw_command: str = raw_command
        self._parsed_input_flags: InputFlags = InputFlags()

    def parse_raw_command(self) -> ParseResult:
        if not self.raw_command:
            raise EmptyInputCommandException()

        input_flags, crnt_flag_name, crnt_flag_val = self._parse_flags(self.raw_command.split()[1:])

        if any([crnt_flag_name, crnt_flag_val]):
            raise UnprocessedInputFlagException()
        else:
            return (self.raw_command.split()[0], input_flags)

    def _parse_flags(self, _tokens: list[str] | list[Never]) -> ParseFlagsResult:
        crnt_flg_name, crnt_flg_val = None, None
        for index, token in enumerate(_tokens):
            crnt_flg_name, crnt_flg_val = _parse_single_token(token, crnt_flg_name, crnt_flg_val)

            if not crnt_flg_name or self._is_next_token_value(index, _tokens):
                continue

            input_flag = InputFlag(
                name=crnt_flg_name[crnt_flg_name.rfind(MIN_FLAG_PREFIX) + 1 :],
                prefix=cast(
                    Literal["-", "--", "---"],
                    crnt_flg_name[: crnt_flg_name.rfind(MIN_FLAG_PREFIX) + 1],
                ),
                input_value=crnt_flg_val,
                status=None,
            )

            if input_flag in self._parsed_input_flags:
                raise RepeatedInputFlagsException(input_flag)

            self._parsed_input_flags.add_flag(input_flag)
            crnt_flg_name, crnt_flg_val = None, None

        return (self._parsed_input_flags, crnt_flg_name, crnt_flg_val)

    def _is_next_token_value(self, current_index: int, _tokens: list[str] | list[Never]) -> bool:
        next_index = current_index + 1
        if next_index >= len(_tokens):
            return False

        next_token = _tokens[next_index]
        return not next_token.startswith(MIN_FLAG_PREFIX)


def _parse_single_token(
    token: str, crnt_flag_name: str | None, crnt_flag_val: str | None
) -> tuple[str | None, str | None]:
    if not token.startswith(MIN_FLAG_PREFIX):
        if not crnt_flag_name or crnt_flag_val:
            raise UnprocessedInputFlagException
        return crnt_flag_name, token

    prefix = token[: token.rfind(MIN_FLAG_PREFIX)]
    if len(token) < 2 or len(prefix) > 2:
        raise UnprocessedInputFlagException

    new_flag_name = token
    new_flag_value = None

    return new_flag_name, new_flag_value
