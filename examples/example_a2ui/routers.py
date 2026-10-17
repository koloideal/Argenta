import re

from rich.console import Console

from argenta import Command, Response, Router
from argenta.command import Flag, Flags
from argenta.command.flag import PossibleValues, ValidationStatus

release_router: Router = Router(title="\nRelease commands:\n")
console = Console(highlight=False)


def _flag_value(response: Response, name: str) -> str:
    flag = response.input_flags.get_flag_by_name(name, with_status=ValidationStatus.VALID)
    return flag.input_value if flag else ""


@release_router.command(
    Command(
        "deploy",
        flags=Flags(
            [
                Flag("env", possible_values=["dev", "staging", "prod"]),
                Flag("force", possible_values=PossibleValues.NEITHER),
                Flag("tag", possible_values=re.compile(r"^v\d+\.\d+\.\d+$")),
            ]
        ),
        description="Deploy a release to an environment",
    )
)
def deploy_handler(response: Response) -> None:
    force_flag = response.input_flags.get_flag_by_name("force", with_status=ValidationStatus.VALID)
    env_value = _flag_value(response, "env")
    tag_value = _flag_value(response, "tag")
    force_text = "yes" if force_flag else "no"
    console.print(f"Deploying env={env_value} force={force_text} tag={tag_value}")


@release_router.command(
    Command(
        "rollback",
        flags=Flag("to", possible_values=["prev", "lts"]),
        description="Roll back a deployment",
    )
)
def rollback_handler(response: Response) -> None:
    to_value = _flag_value(response, "to")
    console.print(f"Rolling back to={to_value}")
