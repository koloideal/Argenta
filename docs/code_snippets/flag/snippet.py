import re
from argenta.command import Flag, PossibleValues

# Simple flag with any values
verbose_flag = Flag(name="verbose")

# Flag with short prefix
short_flag = Flag(name="v", prefix="-")

# Flag that does not take a value
help_flag = Flag(name="help", possible_values=PossibleValues.NEITHER)

# Flag with list of possible values
format_flag = Flag(name="format", possible_values=["json", "xml", "csv"])

# Flag with regexp for validation input value
email_flag = Flag(
    name="email",
    possible_values=re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
)
