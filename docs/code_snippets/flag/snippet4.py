from argenta.command import Flag

help_flag = Flag(name="help")
version_flag = Flag(name="V", prefix="-")

# Использование str() или print()
print(str(help_flag))     # --help
print(version_flag)       # -V

# Форматирование строк
message = f"Use {help_flag} to see help"
print(message)  # Use --help to see help
