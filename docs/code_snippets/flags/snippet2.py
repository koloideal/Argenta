from argenta.command import Flag, Flags

flags: Flags = Flags()

flags.add_flag(Flag("config"))
flags.add_flag(Flag("debug"))
flags.add_flag(Flag("log-level", possible_values=["INFO", "DEBUG", "ERROR"]))

print(len(flags))  # 3
