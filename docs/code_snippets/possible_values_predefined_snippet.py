from argenta.command.flag.defaults import PredefinedFlags

# Проверка типа possible_values в предопределенных флагах
print(PredefinedFlags.HELP.possible_values)       # PossibleValues.NEITHER
print(PredefinedFlags.INFO.possible_values)       # PossibleValues.NEITHER
print(PredefinedFlags.ALL.possible_values)        # PossibleValues.NEITHER

# Сетевые флаги используют регулярные выражения, а не PossibleValues
# PredefinedFlags.HOST использует Pattern для валидации IP
# PredefinedFlags.PORT использует Pattern для валидации порта
