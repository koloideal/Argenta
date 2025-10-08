from typing import Literal
from argenta.command.flag.flags.models import InputFlags
from argenta.response.status import ResponseStatus


EMPTY_INPUT_FLAGS: InputFlags = InputFlags()


class Response:
    __slots__: tuple[Literal['status', 'input_flags'], ...] = ("status", "input_flags")

    def __init__(
        self,
        status: ResponseStatus,
        input_flags: InputFlags = EMPTY_INPUT_FLAGS,
    ):
        """
        Public. The entity of the user input sent to the handler
        :param status: the status of the response
        :param input_flags: all input flags
        """
        self.status: ResponseStatus = status
        self.input_flags: InputFlags = input_flags
