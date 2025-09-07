from argenta.command.flag.models import Flag, InputFlag, ValidationStatus
from argenta.command.flag.flags.models import InputFlags, Flags
from argenta.command.exceptions import (
    UnprocessedInputFlagException,
    RepeatedInputFlagsException,
    EmptyInputCommandException,
)
from typing import Never, Optional, Self, cast, Literal


ParseFlagsResult = tuple[InputFlags, Optional[str], Optional[str]]
ParseResult = tuple[str, InputFlags]
MIN_FLAG_PREFIX: str = "-"


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
        match flags:
            case Flags() as flags_obj:
                self.registered_flags = flags_obj
            case Flag() as single_flag:
                self.registered_flags = Flags([single_flag])
            case None:
                self.registered_flags = Flags()

        self.trigger = trigger
        self.description =  description if description else "Command without description"
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
                is_valid = registered_flag.validate_input_flag_value(flag.input_value)
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
        match input_flags:
            case InputFlags() as flags_obj:
                self.input_flags = flags_obj
            case InputFlag() as single_flag:
                self.input_flags = InputFlags([single_flag])
            case None: 
                self.input_flags = InputFlags()

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
    __slots__ = ("raw_command", "tokens", "trigger", "_parsed_input_flags")

    def __init__(self, raw_command: str) -> None:
        self.raw_command = raw_command
        self._parsed_input_flags = InputFlags()

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
        current_flag_name, current_flag_value = None, None
        for index, token in enumerate(self.tokens):
            current_flag_name, current_flag_value = _parse_single_token(token, current_flag_name, current_flag_value)

            if not current_flag_name or self._is_next_token_value(index):
                continue

            input_flag = InputFlag(
                name=current_flag_name[current_flag_name.rfind(MIN_FLAG_PREFIX) + 1:],
                prefix=cast(
                    Literal["-", "--", "---"],
                    current_flag_name[:current_flag_name.rfind(MIN_FLAG_PREFIX) + 1],
                ),
                input_value=current_flag_value,
                status=None
            )
            
            if input_flag in self._parsed_input_flags:
                raise RepeatedInputFlagsException(input_flag)
            
            self._parsed_input_flags.add_flag(input_flag)
            current_flag_name, current_flag_value = None, None

        return (self._parsed_input_flags, current_flag_name, current_flag_value)
    
    def _is_next_token_value(self, current_index: int) -> bool:
        next_index = current_index + 1
        if next_index >= len(self.tokens):
            return False  
        
        next_token = self.tokens[next_index]
        return not next_token.startswith(MIN_FLAG_PREFIX)
    
def _parse_single_token(
    token: str,
    current_flag_name: Optional[str],
    current_flag_value: Optional[str]
) -> tuple[Optional[str], Optional[str]]:
    if not token.startswith(MIN_FLAG_PREFIX):
        if not current_flag_name or current_flag_value:
            raise UnprocessedInputFlagException
        return current_flag_name, token

    prefix = token[:token.rfind(MIN_FLAG_PREFIX)]
    if len(token) < 2 or len(prefix) > 2:
        raise UnprocessedInputFlagException

    new_flag_name = token
    new_flag_value = None

    return new_flag_name, new_flag_value
