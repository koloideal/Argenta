from typing import Optional
from argenta.command.flag.flags.models import InputFlags
from argenta.response.status import ResponseStatus


class Response:
    __slots__ = ("status", "input_flags")

    def __init__(
        self,
        status: ResponseStatus,
        input_flags: Optional[InputFlags] = None
    ):
        """
        Public. The entity of the user input sent to the handler
        :param status: the status of the response
        :param input_flags: all input flags
        """
        self.status = status
        self.input_flags = input_flags
