from argenta.command.flags.models import ValidInputFlags, UndefinedInputFlags, InvalidValueInputFlags
from argenta.response.status import Status


class Response:
    def __init__(self, status: Status,
                 valid_flags: ValidInputFlags = None,
                 undefined_flags: UndefinedInputFlags = None,
                 invalid_value_flags: InvalidValueInputFlags = None):
        self.status = status
        self.valid_flags = valid_flags
        self.undefined_flags = undefined_flags
        self.invalid_value_flags = invalid_value_flags
