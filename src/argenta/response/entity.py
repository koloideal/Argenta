from __future__ import annotations

__all__ = ["Response"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dishka import Container

from argenta.command import InputFlags
from argenta.response.status import ResponseStatus

EMPTY_INPUT_FLAGS: InputFlags = InputFlags()


class Response:
    __dishka_container__: Container

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

    @classmethod
    def patch_by_container(cls, container: Container) -> None:
        cls.__dishka_container__ = container
