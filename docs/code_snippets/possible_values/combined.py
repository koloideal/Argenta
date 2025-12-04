import re
from argenta.command import Flag, PossibleValues

# Flag without value
verbose_flag = Flag(name="verbose", possible_values=PossibleValues.NEITHER)

# Flag with any value
output_flag = Flag(name="output", possible_values=PossibleValues.ALL)

# Flag with a list of valid values
format_flag = Flag(name="format", possible_values=["json", "xml", "csv", "yaml"])

# Flag with regular expression
email_flag = Flag(name="email", possible_values=re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$"))
