from argenta.command import Flags
from argenta.command.flag.defaults import PredefinedFlags

# Использование предопределенных флагов при создании команды
command_flags = Flags([
    PredefinedFlags.HELP,
    PredefinedFlags.SHORT_HELP,
    PredefinedFlags.INFO,
])

# Использование сетевых флагов
network_flags = Flags([
    PredefinedFlags.HOST,
    PredefinedFlags.PORT,
])

# Валидация значений предопределенных флагов
print(PredefinedFlags.HOST.validate_input_flag_value("192.168.1.1"))  # True
print(PredefinedFlags.HOST.validate_input_flag_value("invalid"))      # False

print(PredefinedFlags.PORT.validate_input_flag_value("8080"))         # True
print(PredefinedFlags.PORT.validate_input_flag_value("99999"))        # True
print(PredefinedFlags.PORT.validate_input_flag_value("abc"))          # False

# Флаги без значений
print(PredefinedFlags.HELP.validate_input_flag_value(None))           # True
print(PredefinedFlags.HELP.validate_input_flag_value("something"))    # False

# Проверка строковых представлений
print(PredefinedFlags.HELP.string_entity)       # --help
print(PredefinedFlags.SHORT_HELP.string_entity) # -H
print(PredefinedFlags.HOST.string_entity)       # --host
print(PredefinedFlags.SHORT_PORT.string_entity) # -P
