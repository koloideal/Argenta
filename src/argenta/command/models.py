__all__ = ["Command", "InputCommand"]

import shlex
from typing import Never, Self, cast, Literal

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
PREFIX_TYPE = Literal["-", "--", "---"]
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
        tokens = shlex.split(raw_command)
        
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
            
            if not name:
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
                status=None
            )
                
            if input_flag in flags:
                raise RepeatedInputFlagsException(input_flag)
            
            flags.add_flag(input_flag)
        
        return cls(command, input_flags=flags)
