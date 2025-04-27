from argenta.command.flag.models import Flag, ValidInputFlag, Flags, InputFlags
from argenta.command.exceptions import (UnprocessedInputFlagException,
                                        RepeatedInputFlagsException,
                                        EmptyInputCommandException)
from typing import Generic, TypeVar, cast, Literal


InputCommandType = TypeVar('InputCommandType')


class BaseCommand:
    def __init__(self, trigger: str) -> None:
        """
        Private. Base class for all commands
        :param trigger: A string trigger, which, when entered by the user, indicates that the input corresponds to the command
        """
        self._trigger = trigger

    def get_trigger(self) -> str:
        """
        Public. Returns the trigger of the command
        :return: the trigger of the command as str
        """
        return self._trigger


class Command(BaseCommand):
    def __init__(self, trigger: str,
                 description: str = None,
                 flags: Flag | Flags = None,
                 aliases: list[str] = None):
        """
        Public. The command that can and should be registered in the Router
        :param trigger: A string trigger, which, when entered by the user, indicates that the input corresponds to the command
        :param description: the description of the command
        :param flags: processed commands
        :param aliases: string synonyms for the main trigger
        """
        super().__init__(trigger)
        self._registered_flags: Flags = flags if isinstance(flags, Flags) else Flags(flags) if isinstance(flags, Flag) else Flags()
        self._description = f'Description for "{self._trigger}" command' if not description else description
        self._aliases = aliases if isinstance(aliases, list) else []

    def get_registered_flags(self) -> Flags:
        """
        Private. Returns the registered flags
        :return: the registered flags as Flags
        """
        return self._registered_flags

    def get_aliases(self) -> list[str] | list:
        """
        Public. Returns the aliases of the command
        :return: the aliases of the command as list[str] | list
        """
        return self._aliases

    def validate_input_flag(self, flag: ValidInputFlag) -> bool:
        """
        Private. Validates the input flag
        :param flag: input flag for validation
        :return: is input flag valid as bool
        """
        registered_flags: Flags | None = self.get_registered_flags()
        if registered_flags:
            if isinstance(registered_flags, Flag):
                if registered_flags.get_string_entity() == flag.get_string_entity():
                    is_valid = registered_flags.validate_input_flag_value(flag.get_value())
                    if is_valid:
                        return True
            else:
                for registered_flag in registered_flags:
                    if registered_flag.get_string_entity() == flag.get_string_entity():
                        is_valid = registered_flag.validate_input_flag_value(flag.get_value())
                        if is_valid:
                            return True
        return False

    def get_description(self) -> str:
        """
        Private. Returns the description of the command
        :return: the description of the command as str
        """
        return self._description



class InputCommand(BaseCommand, Generic[InputCommandType]):
    def __init__(self, trigger: str,
                 input_flags: ValidInputFlag | InputFlags = None):
        """
        Private. The model of the input command, after parsing
        :param trigger:the trigger of the command
        :param input_flags: the input flags
        :return: None
        """
        super().__init__(trigger)
        self._input_flags: InputFlags = input_flags if isinstance(input_flags, InputFlags) else InputFlags(input_flags) if isinstance(input_flags, ValidInputFlag) else InputFlags()

    def _set_input_flags(self, input_flags: InputFlags) -> None:
        """
        Private. Sets the input flags
        :param input_flags: the input flags to set
        :return: None
        """
        self._input_flags = input_flags

    def get_input_flags(self) -> InputFlags:
        """
        Private. Returns the input flags
        :return: the input flags as InputFlags
        """
        return self._input_flags


    @staticmethod
    def parse(raw_command: str) -> InputCommandType:
        """
        Private. Parse the raw input command
        :param raw_command: raw input command
        :return: model of the input command, after parsing as InputCommand
        """
        if not raw_command:
            raise EmptyInputCommandException()

        list_of_tokens = raw_command.split()
        command = list_of_tokens.pop(0)

        input_flags: InputFlags = InputFlags()
        current_flag_name, current_flag_value = None, None

        for k, _ in enumerate(list_of_tokens):
            if _.startswith('-'):
                if current_flag_name or len(_) < 2 or len(_[:_.rfind('-')]) > 3:
                    raise UnprocessedInputFlagException()
                current_flag_name = _
            else:
                if not current_flag_name:
                    raise UnprocessedInputFlagException()
                current_flag_value = _

            if current_flag_name:
                if not len(list_of_tokens) == k+1:
                    if not list_of_tokens[k+1].startswith('-'):
                        continue

                input_flag = ValidInputFlag(name=current_flag_name[current_flag_name.rfind('-') + 1:],
                                            prefix=cast(Literal['-', '--', '---'],
                                                   current_flag_name[:current_flag_name.rfind('-')+1]),
                                            value=current_flag_value)

                all_flags = [flag.get_string_entity() for flag in input_flags.get_flags()]
                if input_flag.get_string_entity() not in all_flags:
                    input_flags.add_flag(input_flag)
                else:
                    raise RepeatedInputFlagsException(input_flag)

                current_flag_name, current_flag_value = None, None

        if any([current_flag_name, current_flag_value]):
            raise UnprocessedInputFlagException()
        else:
            return InputCommand(trigger=command, input_flags=input_flags)

