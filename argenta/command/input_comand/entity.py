from ..input_comand.exceptions import IncorrectInputFlagException
from ..entity import Command
from ..params.flag.flags_group.entity import FlagsGroup
from ..params.flag.input_flag.entity import InputFlag

from typing import Generic, TypeVar


T = TypeVar('T')


class InputCommand(Command, Generic[T]):
    def set_input_flags(self, input_flags: FlagsGroup):
        self._input_flags = input_flags

    def get_input_flags(self) -> FlagsGroup:
        return self._input_flags

    @staticmethod
    def parse(raw_command: str) -> 'InputCommand[T]':
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
                    raise IncorrectInputFlagException()
                else:
                    current_flag_name = _
            else:
                if not current_flag_name:
                    raise IncorrectInputFlagException()
                else:
                    current_flag_value = _
            if current_flag_name and current_flag_value:
                flag_prefix_last_symbol_index = current_flag_name.rfind('-')
                flag_prefix = current_flag_name[:flag_prefix_last_symbol_index]
                flag_name = current_flag_name[flag_prefix_last_symbol_index:]

                input_flag = InputFlag(flag_name=flag_name,
                                       flag_prefix=flag_prefix)
                input_flag.set_value(current_flag_value)

                flags.add_flag(input_flag)

                current_flag_name = None
                current_flag_value = None
        if any([current_flag_name, current_flag_value]):
            raise IncorrectInputFlagException()
        if len(flags.get_flags()) == 0:
            return InputCommand(command=command)
        else:
            input_command = InputCommand(command=command)
            input_command.set_input_flags(flags)
            return input_command


