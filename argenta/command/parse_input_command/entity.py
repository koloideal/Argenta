from typing import Literal, LiteralString
from argenta.command.entity import Command
from argenta.command.params.flag.entity import Flag
from argenta.command.params.flags_group.entity import FlagsGroup
from .exceptions import InvalidInputFlagsException


class ParseInputCommand:
    def __new__(cls, *args, **kwargs):
        raw_command = kwargs['raw_command']
        return ParseInputCommand.parse(raw_command)

    @staticmethod
    def parse(raw_command: str) -> Command:
        list_of_tokens = raw_command.split()
        command_name = list_of_tokens[0]
        list_of_tokens.pop(0)

        flags = []
        current_flag_name = None
        current_flag_value = None
        for _ in list_of_tokens:
            flag_prefix_last_symbol_index = _.rfind('-')
            if _.startswith('-'):
                if current_flag_name or len(_) < 2 or len(_[:flag_prefix_last_symbol_index]) > 3:
                    raise
                else:
                    current_flag_name = _
            else:
                if not current_flag_name:
                    raise
                else:
                    current_flag_value = _
            if current_flag_name and current_flag_value:
                flag_prefix = _[:flag_prefix_last_symbol_index]
                flag_name = _[flag_prefix_last_symbol_index:]

                flags.append(Flag(flag_name=flag_name, flag_prefix=flag_prefix))

                current_flag_name = None
                current_flag_value = None

        command = Command(command_name, flags)

        return command



        if len(flags) == 0:
            return Command(command=command)
        elif len(flags) == 1:
            return Command(command=command, flags=flags[0])
        else:
            flags = FlagsGroup(flags=flags)
            return Command(command=command, flags=flags)
