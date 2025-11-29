from argenta.command import Flags, PredefinedFlags

# Using predefined flags when creating a command
command_flags = Flags(
    [
        PredefinedFlags.HELP,
        PredefinedFlags.SHORT_HELP,
        PredefinedFlags.INFO,
    ]
)

# Using Network Flags
network_flags = Flags(
    [
        PredefinedFlags.HOST,
        PredefinedFlags.PORT,
    ]
)

# Validating the values of predefined flags
print(PredefinedFlags.HOST.validate_input_flag_value("192.168.1.1"))  # True
print(PredefinedFlags.HOST.validate_input_flag_value("invalid"))  # False

print(PredefinedFlags.PORT.validate_input_flag_value("8080"))  # True
print(PredefinedFlags.PORT.validate_input_flag_value("99999"))  # True
print(PredefinedFlags.PORT.validate_input_flag_value("abc"))  # False

# Flags without values
print(PredefinedFlags.HELP.validate_input_flag_value(None))  # True
print(PredefinedFlags.HELP.validate_input_flag_value("something"))  # False

# Checking string representations
print(PredefinedFlags.HELP.string_entity)  # --help
print(PredefinedFlags.SHORT_HELP.string_entity)  # -H
print(PredefinedFlags.HOST.string_entity)  # --host
print(PredefinedFlags.SHORT_PORT.string_entity)  # -P
