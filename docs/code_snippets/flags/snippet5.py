from argenta.command import Flag, Flags
from argenta.command.flag.defaults import PredefinedFlags

flags = Flags([PredefinedFlags.HOST, PredefinedFlags.PORT, Flag("verbose")])

# Итерация по всем флагам
for flag in flags:
    print(f"Flag: {flag.name} (type: {type(flag).__name__})")

# Использование в list comprehension
flag_names = [flag.name for flag in flags]
print(f"All flags: {flag_names}")
