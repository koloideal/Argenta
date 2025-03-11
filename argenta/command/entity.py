from argenta.command.flag.entity import Flag
from argenta.command.flag.flags_group import FlagsGroup
from .exceptions import (UnprocessedInputFlagException,
                         RepeatedInputFlagsException,
                         EmptyInputCommandException)

from typing import Generic, TypeVar, cast, Literal


CommandType = TypeVar('CommandType')


class Command(Generic[CommandType]):
    def __init__(self, trigger: str,
                 description: str = None,
                 flags: Flag | FlagsGroup = None):
        self._trigger = trigger
        self._description = f'description for "{self._trigger}" command' if not description else description
        self._registered_flags: FlagsGroup | None = flags if isinstance(flags, FlagsGroup) else FlagsGroup(flags) if isinstance(flags, Flag) else flags
        self._input_flags: FlagsGroup | None = None


    def get_trigger(self) -> str:
        return self._trigger


    def get_description(self) -> str:
        return self._description


    def get_registered_flags(self) -> FlagsGroup | None:
        return self._registered_flags


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


    def _set_input_flags(self, input_flags: FlagsGroup):
        self._input_flags = input_flags

    def get_input_flags(self) -> FlagsGroup:
        return self._input_flags

    @staticmethod
    def parse_input_command(raw_command: str) -> CommandType:
        if not raw_command:
            raise EmptyInputCommandException()
        list_of_tokens = raw_command.split()
        command = list_of_tokens[0]
        list_of_tokens.pop(0)

        flags: FlagsGroup = FlagsGroup()
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
                if not len(list_of_tokens) == k+1:
                    if not list_of_tokens[k+1].startswith('-'):
                        continue
                flag_prefix_last_symbol_index = current_flag_name.rfind('-')
                flag_prefix = current_flag_name[:flag_prefix_last_symbol_index+1]
                flag_name = current_flag_name[flag_prefix_last_symbol_index+1:]
                input_flag = Flag(flag_name=flag_name,
                                  flag_prefix=cast(Literal['-', '--', '---'], flag_prefix))
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
            return Command(trigger=command)
        else:
            input_command = Command(trigger=command)
            input_command._set_input_flags(flags)
            return input_command



