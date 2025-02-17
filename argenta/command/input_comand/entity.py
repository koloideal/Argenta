from argenta.command.input_comand.exceptions import InvalidInputFlagsException
from ..entity import Command
from ..params.flags_group.entity import FlagsGroup
from ..params.input_flag.entity import InputFlag


class InputCommand(Command):
    def set_input_flags(self, input_flags: list[InputFlag]):
        self._input_flags = input_flags

    def get_input_flags(self) -> list[InputFlag]:
        return self._input_flags

    @staticmethod
    def parse(raw_command: str) -> Command:
        list_of_tokens = raw_command.split()
        command = list_of_tokens[0]
        list_of_tokens.pop(0)

        flags = []
        current_flag_name = None
        current_flag_value = None
        for _ in list_of_tokens:
            flag_prefix_last_symbol_index = _.rfind('-')
            if _.startswith('-'):
                if current_flag_name or len(_) < 2 or len(_[:flag_prefix_last_symbol_index]) > 3:
                    raise InvalidInputFlagsException
                else:
                    current_flag_name = _
            else:
                if not current_flag_name:
                    raise InvalidInputFlagsException
                else:
                    current_flag_value = _
            if current_flag_name and current_flag_value:
                flag_prefix = _[:flag_prefix_last_symbol_index]
                flag_name = _[flag_prefix_last_symbol_index:]

                input_flag = InputFlag(flag_name=flag_name,
                                       flag_prefix=flag_prefix)
                input_flag.set_value(current_flag_value)

                flags.append(input_flag)

                current_flag_name = None
                current_flag_value = None

        if len(flags) == 0:
            return Command(command=command)
        else:
            flags = FlagsGroup(flags=flags)
            return Command(command=command, flags=flags)


