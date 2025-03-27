from dataclasses import dataclass
from argenta.command.flag import Flag
import re


@dataclass
class DefaultFlags:
    HELP = Flag(flag_name='help', possible_flag_values=False)
    SHORT_HELP = Flag(flag_name='h', flag_prefix='-', possible_flag_values=False)

    INFO = Flag(flag_name='info', possible_flag_values=False)
    SHORT_INFO = Flag(flag_name='i', flag_prefix='-', possible_flag_values=False)

    ALL = Flag(flag_name='all', possible_flag_values=False)
    SHORT_ALL = Flag(flag_name='a', flag_prefix='-', possible_flag_values=False)

    HOST = Flag(flag_name='host', possible_flag_values=re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'))
    SHORT_HOST = Flag(flag_name='h', flag_prefix='-', possible_flag_values=re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'))

    PORT = Flag(flag_name='port', possible_flag_values=re.compile(r'^\d{1,5}$'))
    SHORT_PORT = Flag(flag_name='p', flag_prefix='-', possible_flag_values=re.compile(r'^\d{1,5}$'))
