__all__ = ["Response"]
from typing import Any

from dishka import Container

from argenta.command.flag.flags.models import InputFlags
from argenta.response.status import ResponseStatus

EMPTY_INPUT_FLAGS: InputFlags = InputFlags()


class DataBridge:
	_data: dict[str, Any] = {}

	@classmethod
	def update_data(cls, data: dict[str, Any]) -> None:
		cls._data.update(data)

	@classmethod
	def get_data(cls) -> dict[str, Any]:
		return cls._data

	@classmethod
	def clear_data(cls) -> None:
		cls._data.clear()

	@classmethod
	def delete_from_data(cls, key: str) -> None:
		cls._data.pop(key)


class Response(DataBridge):
    _dishka_container: Container

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
        cls._dishka_container = container
