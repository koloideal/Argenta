from argenta.command import Flag, Flags
from argenta.command.flag.defaults import PredefinedFlags

# Начальная коллекция
flags = Flags([
    PredefinedFlags.HOST
])

# Дополнительные флаги
additional_flags = [
    PredefinedFlags.PORT,
    Flag("database"),
    Flag("ssl"),
    Flag("verbose")
]

# Добавление списка флагов
flags.add_flags(additional_flags)

print(len(flags.flags))  # 5