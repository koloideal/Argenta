from argenta.command import Flag, Flags

# Создание коллекции
flags: Flags = Flags()

# Динамическое добавление флагов
flags.add_flag(Flag("config"))
flags.add_flag(Flag("debug"))
flags.add_flag(Flag("log-level", possible_values=["INFO", "DEBUG", "ERROR"]))

print(len(flags.flags))  # 3
