from .params.flag.entity import Flag
from .params.flag.flags_group.entity import FlagsGroup
from .exceptions import (InvalidCommandInstanceException,
                         InvalidDescriptionInstanceException,
                         InvalidFlagsInstanceException, UnprocessedInputFlagException, RepeatedInputFlagsException)

from typing import Generic, TypeVar


T = TypeVar('T')


class Command(Generic[T]):
    def __init__(self, command: str,
                 description: str | None = None,
                 flags: Flag | FlagsGroup | None = None):
        self._command = command
        self._description = description
        self._flags: FlagsGroup | None = flags if isinstance(flags, FlagsGroup) else FlagsGroup([flags]) if isinstance(flags, Flag) else flags

        self._input_flags: FlagsGroup | None = None


    def get_string_entity(self):
        return self._command


    def get_description(self):
        if not self._description:
            description = f'description for "{self._command}" command'
            return description
        else:
            return self._description


    def get_registered_flags(self):
        return self._flags


    def validate_commands_params(self):
        if not isinstance(self._command, str):
            raise InvalidCommandInstanceException(self._command)
        if not isinstance(self._description, str):
            raise InvalidDescriptionInstanceException()
        if not any([(isinstance(self._flags, FlagsGroup)), not self._flags]):
            raise InvalidFlagsInstanceException


    def validate_input_flag(self, flag: Flag):
        registered_flags: FlagsGroup | None = self.get_registered_flags()
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


    def set_input_flags(self, input_flags: FlagsGroup):
        self._input_flags = input_flags

    def get_input_flags(self) -> FlagsGroup:
        return self._input_flags

    @staticmethod
    def parse_input_command(raw_command: str) -> 'Command[T]':
        list_of_tokens = raw_command.split()
        command = list_of_tokens[0]
        list_of_tokens.pop(0)

        flags: FlagsGroup = FlagsGroup()
        current_flag_name = None
        current_flag_value = None
        for _ in list_of_tokens:
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
            if current_flag_name and current_flag_value:
                flag_prefix_last_symbol_index = current_flag_name.rfind('-')
                flag_prefix = current_flag_name[:flag_prefix_last_symbol_index]
                flag_name = current_flag_name[flag_prefix_last_symbol_index:]

                input_flag = Flag(flag_name=flag_name,
                                  flag_prefix=flag_prefix)
                input_flag.set_value(current_flag_value)

                all_flags = [x.get_string_entity() for x in flags.get_flags()]
                if input_flag.get_string_entity() not in all_flags:
                    flags.add_flag(input_flag)
                else:
                    raise RepeatedInputFlagsException(input_flag)

                current_flag_name = None
                current_flag_value = None
        if any([current_flag_name, current_flag_value]):
            raise UnprocessedInputFlagException()
        if len(flags.get_flags()) == 0:
            return Command(command=command)
        else:
            input_command = Command(command=command)
            input_command.set_input_flags(flags)
            return input_command



