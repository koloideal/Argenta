"""Note-keeping commands for the compact REPL example."""

from rich.console import Console

from argenta import Command, Response, Router
from argenta.command import Flag
from argenta.command.flag import ValidationStatus

notes_router: Router = Router(title="Notes:")
console = Console(highlight=False)

_notes: list[str] = []


@notes_router.command(Command("add", flags=Flag("text"), description="Add a note"))
def add_handler(response: Response) -> None:
    text_flag = response.input_flags.get_flag_by_name("text", with_status=ValidationStatus.VALID)
    if not text_flag:
        console.print("usage: add --text <note>")
        return
    _notes.append(text_flag.input_value)
    console.print(f"note #{len(_notes)} saved")


@notes_router.command(Command("list", description="List all notes"))
def list_handler(response: Response) -> None:
    if not _notes:
        console.print("no notes yet")
        return
    for position, note in enumerate(_notes, start=1):
        console.print(f"{position}. {note}")


@notes_router.command(Command("clear", description="Remove all notes"))
def clear_handler(response: Response) -> None:
    removed = len(_notes)
    _notes.clear()
    console.print(f"removed {removed} note(s)")
