from dataclasses import dataclass
from argenta.command.flag.models import Flag, PossibleValues
import re



@dataclass
class PredefinedFlags:
    """
    Public. A dataclass with predefined flags and most frequently used flags for quick use
    """

    HELP = Flag(name="help", possible_values=PossibleValues.DISABLE)
    SHORT_HELP = Flag(name="H", prefix="-", possible_values=PossibleValues.DISABLE)

    INFO = Flag(name="info", possible_values=PossibleValues.DISABLE)
    SHORT_INFO = Flag(name="I", prefix="-", possible_values=PossibleValues.DISABLE)

    ALL = Flag(name="all", possible_values=PossibleValues.DISABLE)
    SHORT_ALL = Flag(name="A", prefix="-", possible_values=PossibleValues.DISABLE)

    HOST = Flag(
        name="host", possible_values=re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    )
    SHORT_HOST = Flag(
        name="H",
        prefix="-",
        possible_values=re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    )

    PORT = Flag(name="port", possible_values=re.compile(r"^\d{1,5}$"))
    SHORT_PORT = Flag(name="P", prefix="-", possible_values=re.compile(r"^\d{1,5}$"))
