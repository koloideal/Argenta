__all__ = ["PredefinedFlags"]

from typing import Literal
from argenta.command.flag.models import Flag, PossibleValues
import re


DEFAULT_PREFIX: Literal["-", "--", "---"] = "-"


class PredefinedFlags:
	HELP = Flag(name="help", possible_values=PossibleValues.NEITHER)
	SHORT_HELP = Flag(name="H", prefix=DEFAULT_PREFIX, possible_values=PossibleValues.NEITHER)

	INFO = Flag(name="info", possible_values=PossibleValues.NEITHER) # noqa: WPS110
	SHORT_INFO = Flag(name="I", prefix=DEFAULT_PREFIX, possible_values=PossibleValues.NEITHER)

	ALL = Flag(name="all", possible_values=PossibleValues.NEITHER)
	SHORT_ALL = Flag(name="A", prefix=DEFAULT_PREFIX, possible_values=PossibleValues.NEITHER)

	HOST = Flag(
	    name="host", possible_values=re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
	)
	SHORT_HOST = Flag(
	    name="H",
	    prefix=DEFAULT_PREFIX,
	    possible_values=re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
	)

	PORT = Flag(name="port", possible_values=re.compile(r"^\d{1,5}$"))
	SHORT_PORT = Flag(name="P", prefix=DEFAULT_PREFIX, possible_values=re.compile(r"^\d{1,5}$"))
