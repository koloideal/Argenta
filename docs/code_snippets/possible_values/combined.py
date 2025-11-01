from argenta.command import Flag, PossibleValues
import re

# Флаг без значения
verbose_flag = Flag(
    name="verbose",
    possible_values=PossibleValues.NEITHER
)

# Флаг с любым значением
output_flag = Flag(
    name="output",
    possible_values=PossibleValues.ALL
)

# Флаг со списком допустимых значений
format_flag = Flag(
    name="format",
    possible_values=["json", "xml", "csv", "yaml"]
)

# Флаг с регулярным выражением
email_flag = Flag(
    name="email",
    possible_values=re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
)
