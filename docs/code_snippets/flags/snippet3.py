from argenta.command import Flag, Flags
from argenta.command.flag.defaults import PredefinedFlags

flags = Flags([PredefinedFlags.HOST])

additional_flags = [
    PredefinedFlags.PORT,
    Flag("database"),
    Flag("ssl"),
    Flag("verbose"),
]

flags.add_flags(additional_flags)

print(len(flags))  # 5
