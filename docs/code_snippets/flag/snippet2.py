import re

from argenta.command.flag.models import Flag, PossibleValues

# Флаг со списком допустимых значений
format_flag = Flag(name="format", possible_values=["json", "xml", "csv"])

# Валидация значений
print(format_flag.validate_input_flag_value("json"))  # True
print(format_flag.validate_input_flag_value("pdf"))   # False

# Флаг без значения
help_flag = Flag(name="help", possible_values=PossibleValues.NEITHER)
print(help_flag.validate_input_flag_value(None))      # True
print(help_flag.validate_input_flag_value("value"))   # False

# Флаг с регулярным выражением
port_flag = Flag(name="port", possible_values=re.compile(r"^\d{1,5}$"))
print(port_flag.validate_input_flag_value("8080"))    # True
print(port_flag.validate_input_flag_value("abc"))     # False
