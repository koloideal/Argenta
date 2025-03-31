from argenta.command.flag.models import Flag, InputFlag, Flags, InputFlags
from argenta.command.exceptions import (UnprocessedInputFlagException,
                                         RepeatedInputFlagsException,
                                         EmptyInputCommandException)
from typing import Generic, TypeVar, cast, Literal


BaseCommandType = TypeVar('BaseCommandType')


class BaseCommand(Generic[BaseCommandType]):
    def __init__(self, trigger: str,
                 description: str = None,
                 flags: Flag | Flags = None):
        self._trigger = trigger
        self._description = f'description for "{self._trigger}" command' if not description else description

    def get_trigger(self) -> str:
        return self._trigger

    def get_description(self) -> str:
        return self._description



class Command(BaseCommand):
    def __init__(self, trigger: str,
                 description: str = None,
                 flags: Flag | Flags = None):
        super().__init__(trigger, description)
        self._registered_flags: Flags = flags if isinstance(flags, Flags) else Flags(flags) if isinstance(flags, Flag) else Flags()

    def get_registered_flags(self) -> Flags:
        return self._registered_flags

    def validate_input_flag(self, flag: InputFlag):
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



class InputCommand(BaseCommand):
    def __init__(self, trigger: str,
                 description: str = None,
                 input_flags: InputFlag | InputFlags = None):
        super().__init__(trigger, description)
        self._input_flags: InputFlags = input_flags if isinstance(input_flags, InputFlags) else InputFlags(input_flags) if isinstance(input_flags, InputFlag) else InputFlags()

    def _set_input_flags(self, input_flags: InputFlags):
        self._input_flags = input_flags

    def get_input_flags(self) -> InputFlags:
        return self._input_flags

    @staticmethod
    def parse_input_command(raw_command: str) -> BaseCommandType:
        if not raw_command:
            raise EmptyInputCommandException()
        list_of_tokens = raw_command.split()
        command = list_of_tokens[0]
        list_of_tokens.pop(0)

        input_flags: InputFlags = InputFlags()
        current_flag_name = None
        current_flag_value = None
        for k, _ in enumerate(list_of_tokens):
            if _.startswith('-'):
                flag_prefix_last_symbol_index = _.rfind('-')
                if current_flag_name or len(_) < 2 or len(_[:flag_prefix_last_symbol_index]) > 3:
                    raise UnprocessedInputFlagException()
                else:
                    current_flag_name = _
            else:
                if not current_flag_name:
                    raise UnprocessedInputFlagException()
                else:
                    current_flag_value = _
            if current_flag_name:
                if not len(list_of_tokens) == k + 1:
                    if not list_of_tokens[k + 1].startswith('-'):
                        continue
                flag_prefix_last_symbol_index = current_flag_name.rfind('-')
                flag_prefix = current_flag_name[:flag_prefix_last_symbol_index + 1]
                flag_name = current_flag_name[flag_prefix_last_symbol_index + 1:]
                input_flag = InputFlag(name=flag_name,
                                       prefix=cast(Literal['-', '--', '---'], flag_prefix))
                input_flag.set_value(current_flag_value)

                all_flags = [x.get_string_entity() for x in input_flags.get_flags()]
                if input_flag.get_string_entity() not in all_flags:
                    input_flags.add_flag(input_flag)
                else:
                    raise RepeatedInputFlagsException(input_flag)

                current_flag_name = None
                current_flag_value = None
        if any([current_flag_name, current_flag_value]):
            raise UnprocessedInputFlagException()
        if len(input_flags.get_flags()) == 0:
            return InputCommand(trigger=command)
        else:
            input_command = InputCommand(trigger=command)
            input_command._set_input_flags(input_flags)
            return input_command

