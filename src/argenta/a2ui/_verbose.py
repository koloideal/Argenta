from rich.console import Console


class VerboseLog:
    """
    Private. Stderr reporter for the A2UI agent lifecycle; stderr keeps
    the stdio transport wire free of log noise. ``always=True`` events
    are reported even when verbose logging is disabled
    """

    def __init__(self, enabled: bool, channel: str) -> None:
        self._enabled = enabled
        self._channel = channel
        self._console = Console(stderr=True, markup=False, log_path=False)

    def report(self, event: str, *, always: bool = False, style: str | None = None) -> None:
        if self._enabled or always:
            self._console.log(f"a2ui [{self._channel}]: {event}", style=style)
