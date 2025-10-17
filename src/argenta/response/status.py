__all__ = ["ResponseStatus"]

from enum import Enum


class ResponseStatus(Enum):
    ALL_FLAGS_VALID = "ALL_FLAGS_VALID"
    UNDEFINED_FLAGS = "UNDEFINED_FLAGS"
    INVALID_VALUE_FLAGS = "INVALID_VALUE_FLAGS"
    UNDEFINED_AND_INVALID_FLAGS = "UNDEFINED_AND_INVALID_FLAGS"

    @classmethod
    def from_flags(cls, *, has_invalid_value_flags: bool, has_undefined_flags: bool) -> 'ResponseStatus':
        key = (has_invalid_value_flags, has_undefined_flags)
        status_map: dict[tuple[bool, bool], ResponseStatus] = {
            (True,  True):  cls.UNDEFINED_AND_INVALID_FLAGS,
            (True,  False): cls.INVALID_VALUE_FLAGS,
            (False, True):  cls.UNDEFINED_FLAGS,
            (False, False): cls.ALL_FLAGS_VALID,
        }
        return status_map[key]
