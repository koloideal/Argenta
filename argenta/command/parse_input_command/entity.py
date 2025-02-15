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
        list_of__ = raw_command.split()
        command = list_of__[0]
        list_of__.pop(0)

        flags = []
        for k, _ in enumerate(list_of__):
            if not _.startswith('-') or len( _[:len(_.lstrip('-'))]) > 3:
                raise InvalidInputFlagsException()
            else:
                flag_name: str = _.lstrip('-')
                flag_prefix = _[:len(flag_name)]

                parse_flag = Flag(flag_name=flag_name,
                                  flag_prefix=flag_prefix)

                flags.append(parse_flag)

        if len(flags) == 0:
            return Command(command=command)
        elif len(flags) == 1:
            return Command(command=command, flags=flags[0])
        else:
            flags = FlagsGroup(flags=flags)
            return Command(command=command, flags=flags)
