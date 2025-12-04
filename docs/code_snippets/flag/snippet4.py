from argenta.command import Flag

help_flag = Flag(name="help")
version_flag = Flag(name="V", prefix="-")

print(help_flag)  # --help

message = f"Use {help_flag} to see help"
print(message)  # Use --help to see help
