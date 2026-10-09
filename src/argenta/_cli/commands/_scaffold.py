from pathlib import Path

from rich.console import Console


def sanitize_package_name(name: str) -> str:
    return name.lower().replace(" ", "_").replace("-", "_")


def create_file(path: Path, file_content: str, console: Console) -> None:
    if path.exists():
        console.print(f"[yellow]Skipped:[/yellow] {path} (already exists)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    stripped = file_content.strip()
    path.write_text(f"{stripped}\n" if stripped else "", encoding="utf-8")
