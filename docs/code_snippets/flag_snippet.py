from argenta.command import Flag, PossibleValues
import re

# Простой флаг с любыми значениями
verbose_flag = Flag(name="verbose")

# Флаг с коротким префиксом
short_flag = Flag(name="v", prefix="-")

# Флаг без значения
help_flag = Flag(name="help", possible_values=PossibleValues.NEITHER)

# Флаг со списком допустимых значений
format_flag = Flag(
    name="format",
    possible_values=["json", "xml", "csv"]
)

# Флаг с регулярным выражением для валидации
email_flag = Flag(
    name="email",
    possible_values=re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
)
