from dataclasses import dataclass
from argenta.command.flag.models import Flag
import re


@dataclass
class PredefinedFlags:
    """
    Public. A dataclass with predefined flags and most frequently used flags for quick use
    """
    HELP = Flag(name='help', possible_values=False)
    SHORT_HELP = Flag(name='h', prefix='-', possible_values=False)

    INFO = Flag(name='info', possible_values=False)
    SHORT_INFO = Flag(name='i', prefix='-', possible_values=False)

    ALL = Flag(name='all', possible_values=False)
    SHORT_ALL = Flag(name='a', prefix='-', possible_values=False)

    HOST = Flag(name='host', possible_values=re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'))
    SHORT_HOST = Flag(name='h', prefix='-', possible_values=re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'))

    PORT = Flag(name='port', possible_values=re.compile(r'^\d{1,5}$'))
    SHORT_PORT = Flag(name='p', prefix='-', possible_values=re.compile(r'^\d{1,5}$'))
