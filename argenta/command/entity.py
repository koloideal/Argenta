from .params.flag.entity import Flag
from .params.flag.flags_group.entity import FlagsGroup
from .exceptions import (InvalidCommandInstanceException,
                         InvalidDescriptionInstanceException,
                         InvalidFlagsInstanceException)
from .params.flag.input_flag.entity import InputFlag


class Command:
    def __init__(self, command: str,
                 description: str | None = None,
                 flags: Flag | FlagsGroup | None = None):
        self._command = command
        self._description = description
        self._flags = flags

        self._input_flags: FlagsGroup | None = None

    def get_string_entity(self):
        return self._command

    def get_description(self):
        if not self._description:
            description = f'description for "{self._command}" command'
            return description
        else:
            return self._description

    def get_flags(self):
        return self._flags

    def set_command(self, command: str):
        self._command = command

    def validate_commands_params(self):
        if not isinstance(self._command, str):
            raise InvalidCommandInstanceException(self._command)
        if not isinstance(self._description, str):
            raise InvalidDescriptionInstanceException()
        if not (isinstance(self._flags, Flag) or not isinstance(self._flags, FlagsGroup)) or not self._flags is None:
            raise InvalidFlagsInstanceException

    def validate_input_flag(self, flag: InputFlag):
        registered_flags: FlagsGroup = self._flags
        if registered_flags:
            for registered_flag in registered_flags:
                if registered_flag.get_string_entity() == flag.get_string_entity():
                    is_valid = registered_flag.validate_input_flag_value(flag)
                    if is_valid:
                        return True
        return False



