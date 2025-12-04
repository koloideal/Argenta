from argenta.command import Flag, Flags
from argenta.command.flag.defaults import PredefinedFlags


flags = Flags([PredefinedFlags.HOST, PredefinedFlags.PORT, Flag("verbose")])

host_flag = flags.get_flag_by_name("host")
if host_flag:
    print(f"Found flag: {host_flag.name}")

unknown_flag = flags.get_flag_by_name("nonexistent")
if unknown_flag is None:
    print("Flag not found")
