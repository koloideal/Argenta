from argenta.command.flag.models import Flag, InputFlag, ValidationStatus
from argenta.command.flag.flags.models import InputFlags, Flags
from argenta.command.exceptions import (
    UnprocessedInputFlagException,
    RepeatedInputFlagsException,
    EmptyInputCommandException,
)
from typing import Never, Optional, Self, cast, Literal


ParseFlagsResult = tuple[InputFlags, str | None, str | None]
ParseResult = tuple[str, InputFlags]


class Command:
    def __init__(
        self,
        trigger: str, *, 
        description: Optional[str] = None,
        flags: Optional[Flag | Flags] = None,
        aliases: Optional[list[str]] = None,
    ):
        """
        Public. The command that can and should be registered in the Router
        :param trigger: A string trigger, which, when entered by the user, indicates that the input corresponds to the command
        :param description: the description of the command
        :param flags: processed commands
        :param aliases: string synonyms for the main trigger
        """
        self.registered_flags: Flags = flags if isinstance(flags, Flags) else Flags([flags]) if isinstance(flags, Flag) else Flags()
        self.trigger = trigger
        self.description = "Command without description" if not description else description
        self.aliases = aliases if aliases else []

    def validate_input_flag(
        self, flag: InputFlag
    ) -> ValidationStatus:
        """
        Private. Validates the input flag
        :param flag: input flag for validation
        :return: is input flag valid as bool
        """
        registered_flags: Flags = self.registered_flags
        for registered_flag in registered_flags:
            if registered_flag.string_entity == flag.string_entity:
                is_valid = registered_flag.validate_input_flag_value(flag.value)
                if is_valid:
                    return ValidationStatus.VALID
                else:
                    return ValidationStatus.INVALID
        return ValidationStatus.UNDEFINED


class InputCommand:
    def __init__(self, trigger: str, *, 
                 input_flags: Optional[InputFlag | InputFlags] = None):
        """
        Private. The model of the input command, after parsing
        :param trigger:the trigger of the command
        :param input_flags: the input flags
        :return: None
        """
        self.trigger = trigger
        self.input_flags = input_flags if isinstance(input_flags, InputFlags) else InputFlags([input_flags]) if isinstance(input_flags, InputFlag) else InputFlags()

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
    __slots__ = ("raw_command", "tokens", "trigger")

    def __init__(self, raw_command: str) -> None:
        self.raw_command = raw_command

    def parse_raw_command(self) -> ParseResult:
        if not self.raw_command:
            raise EmptyInputCommandException()
        
        self.tokens: list[str] | list[Never] = self.raw_command.split()[1:]
        self.trigger: str = self.raw_command.split()[0]

        input_flags, current_flag_name, current_flag_value = self._parse_flags()

        if any([current_flag_name, current_flag_value]):
            raise UnprocessedInputFlagException()
        else:
            return (self.trigger, input_flags)

    def _parse_flags(self) -> ParseFlagsResult:
        input_flags: InputFlags = InputFlags()
        current_flag_name, current_flag_value = None, None
        for k, _ in enumerate(self.tokens):
            if _.startswith("-"):
                if len(_) < 2 or len(_[: _.rfind("-")]) > 2:
                    raise UnprocessedInputFlagException()
                current_flag_name = _
            else:
                if not current_flag_name or current_flag_value:
                    raise UnprocessedInputFlagException()
                current_flag_value = _

            if current_flag_name:
                if k + 1 < len(self.tokens) and not self.tokens[k + 1].startswith("-"):
                    continue

                input_flag = InputFlag(
                    name=current_flag_name[current_flag_name.rfind("-") + 1:],
                    prefix=cast(
                        Literal["-", "--", "---"],
                        current_flag_name[:current_flag_name.rfind("-") + 1],
                    ),
                    value=current_flag_value,
                    status=None
                )
                
                if input_flag in input_flags:
                    raise RepeatedInputFlagsException(input_flag)
                else:
                    input_flags.add_flag(input_flag)
                    current_flag_name, current_flag_value = None, None

        return (input_flags, current_flag_name, current_flag_value)
