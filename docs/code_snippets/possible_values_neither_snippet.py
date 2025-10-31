from argenta.command import Flag, PossibleValues

# Создание флагов без значений
help_flag = Flag(name="help", possible_values=PossibleValues.NEITHER)
verbose_flag = Flag(name="verbose", possible_values=PossibleValues.NEITHER)
force_flag = Flag(name="force", possible_values=PossibleValues.NEITHER)

# Такие флаги используются как переключатели
# Правильно: myapp --help
# Неправильно: myapp --help something
