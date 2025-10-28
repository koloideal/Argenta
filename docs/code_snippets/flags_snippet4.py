from argenta.command import Flags, Flag
from argenta.command.flag.defaults import PredefinedFlags

flags = Flags([
    PredefinedFlags.HOST,
    PredefinedFlags.PORT,
    Flag("verbose")
])

# Получение флага по имени
host_flag = flags.get_flag_by_name("host")
if host_flag:
    print(f"Found flag: {host_flag.name}")

# Поиск несуществующего флага
unknown_flag = flags.get_flag_by_name("nonexistent")
if unknown_flag is None:
    print("Flag not found")