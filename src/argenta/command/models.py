from argenta.command.flag.models import Flag, InputFlag, ValidationStatus
from argenta.command.flag.flags.models import InputFlags, Flags
from argenta.command.exceptions import (
    UnprocessedInputFlagException,
    RepeatedInputFlagsException,
    EmptyInputCommandException,
)
from typing import Optional, Self, cast, Literal


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
        flags = flags if isinstance(flags, Flags) else Flags([flags]) if isinstance(flags, Flag) else Flags()
        self._trigger = trigger
        self._registered_flags: Flags = flags
        self._description = "Command without description" if not description else description
        self._aliases = aliases if aliases else []

    def get_registered_flags(self) -> Flags:
        """
        Private. Returns the registered flags
        :return: the registered flags as Flags
        """
        return self._registered_flags

    def get_aliases(self) -> list[str]:
        """
        Public. Returns the aliases of the command
        :return: the aliases of the command as list[str]
        """
        return self._aliases

    def validate_input_flag(
        self, flag: InputFlag
    ) -> ValidationStatus:
        """
        Private. Validates the input flag
        :param flag: input flag for validation
        :return: is input flag valid as bool
        """
        registered_flags: Flags = self.get_registered_flags()
        for registered_flag in registered_flags:
            if registered_flag.get_string_entity() == flag.get_string_entity():
                is_valid = registered_flag.validate_input_flag_value(flag.get_value())
                if is_valid:
                    return ValidationStatus.VALID
                else:
                    return ValidationStatus.INVALID
        return ValidationStatus.UNDEFINED

    def get_description(self) -> str:
        """
        Private. Returns the description of the command
        :return: the description of the command as str
        """
        return self._description
    
    def get_trigger(self) -> str:
        """
        Public. Returns the trigger of the command
        :return: the trigger of the command as str
        """
        return self._trigger


class InputCommand:
    def __init__(self, trigger: str, *, 
                 input_flags: Optional[InputFlag | InputFlags] = None):
        """
        Private. The model of the input command, after parsing
        :param trigger:the trigger of the command
        :param input_flags: the input flags
        :return: None
        """
        self._trigger = trigger
        input_flags = input_flags if isinstance(input_flags, InputFlags) else InputFlags([input_flags]) if isinstance(input_flags, InputFlag) else InputFlags()
        self._input_flags: InputFlags = input_flags

    def get_input_flags(self) -> InputFlags:
        """
        Private. Returns the input flags
        :return: the input flags as InputFlags
        """
        return self._input_flags

    @classmethod
    def parse(cls, raw_command: str) -> Self:
        """
        Private. Parse the raw input command
        :param raw_command: raw input command
        :return: model of the input command, after parsing as InputCommand
        """
        if not raw_command:
            raise EmptyInputCommandException()

        list_of_tokens: list[str] = raw_command.split()
        command: str = list_of_tokens.pop(0)

        input_flags: InputFlags = InputFlags()
        current_flag_name, current_flag_value = None, None

        for k, _ in enumerate(list_of_tokens):
            if _.startswith("-"):
                if len(_) < 2 or len(_[: _.rfind("-")]) > 2:
                    raise UnprocessedInputFlagException()
                current_flag_name = _
            else:
                if not current_flag_name or current_flag_value:
                    raise UnprocessedInputFlagException()
                current_flag_value = _

            if current_flag_name:
                if not len(list_of_tokens) == k + 1:
                    if not list_of_tokens[k + 1].startswith("-"):
                        continue

                input_flag = InputFlag(
                    name=current_flag_name[current_flag_name.rfind("-") + 1 :],
                    prefix=cast(
                        Literal["-", "--"],
                        current_flag_name[: current_flag_name.rfind("-") + 1],
                    ),
                    value=current_flag_value,
                    status=None
                )

                all_flags = [flag.get_string_entity() for flag in input_flags.get_flags()]
                
                if input_flag.get_string_entity() not in all_flags:
                    input_flags.add_flag(input_flag)
                else:
                    raise RepeatedInputFlagsException(input_flag)

                current_flag_name, current_flag_value = None, None

        if any([current_flag_name, current_flag_value]):
            raise UnprocessedInputFlagException()
        else:
            return cls(trigger=command, input_flags=input_flags)
        
    def get_trigger(self) -> str:
        """
        Public. Returns the trigger of the command
        :return: the trigger of the command as str
        """
        return self._trigger
