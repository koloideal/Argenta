"""Shared scenario builders and configs for benchmark modules."""

from collections.abc import Iterable
from dataclasses import dataclass

from argenta.command import Flag, Flags
from argenta.command.models import Command
from argenta.response import Response
from argenta.router import Router


@dataclass(frozen=True, slots=True)
class InputCommandParseConfig:
    benchmark_type: str = "input_command_parse"
    extreme_flags_count: int = 50


def command_handler(_res: Response) -> None: ...


def alias_sets(command_count: int, aliases_count: int) -> tuple[set[str], ...]:
    return tuple(
        {f"alias{command_index}_{alias_index}" for alias_index in range(aliases_count)}
        for command_index in range(command_count)
    )


def router_with_commands(
    trigger_prefix: str, command_count: int, flags_per_command: int = 0
) -> Router:
    router = Router()
    for command_index in range(command_count):
        flags = (
            Flags(
                [
                    Flag(f"{trigger_prefix}{command_index}_f{flag_index}")
                    for flag_index in range(flags_per_command)
                ]
            )
            if flags_per_command
            else None
        )
        router.command(Command(f"{trigger_prefix}{command_index}", flags=flags))(command_handler)
    return router


def flags_router(flag_names: Iterable[str]) -> Router:
    flags = Flags([Flag(name) for name in flag_names])
    router = Router()
    router.command(Command("test", flags=flags))(command_handler)
    return router
