"""Terminal gRPC client for the A2UI example agent.

Start the agent with ``argenta a2ui -t grpc examples/a2ui/agent.py:main``,
then run this client via
``uv run --extra a2ui python examples/a2ui/grpc_client.py [host:port]``.
Type ``<command> flag=value ...`` lines to dispatch actions.
"""

import json
import queue
import sys
import threading
from dataclasses import dataclass, replace

import grpc
from rich.console import Console
from rich.panel import Panel

from argenta.a2ui.models import Message
from argenta.a2ui.transport.grpc import agent_pb2, agent_pb2_grpc


@dataclass(frozen=True)
class ClientConfig:
    """Connection and rendering settings for the terminal client"""

    address: str = "127.0.0.1:8765"
    protocol_version: str = "v0.9"
    log_path: str = "/log"
    log_fence: str = "````"


class _LogView:
    """Private. Mirrors the agent log and renders only the appended tail"""

    def __init__(self, console: Console, config: ClientConfig) -> None:
        self._console = console
        self._config = config
        self._lines: list[str] = []

    def render(self, message: Message) -> None:
        """Private. Prints log lines added since the previous update;
        non-log frames are skipped"""
        update = message.get("updateDataModel")
        if isinstance(update, dict) and update.get("path") == self._config.log_path:
            self._show(update.get("value", ""))

    def _show(self, raw_log: object) -> None:
        """Private. Diffs the log model and prints the appended tail"""
        text = str(raw_log).replace(self._config.log_fence, "")
        current = text.strip().splitlines()
        size = len(self._lines)
        fresh = current
        if current[:size] == self._lines:
            fresh = current[size:]
        for line in fresh:
            self._console.print(line)
        self._lines = current


def _context_flags(tail: str) -> dict[str, str]:
    """Private. `flag=value` pairs into an action context"""
    context = {}
    for pair in tail.split():
        key, _, flag_value = pair.partition("=")
        if key:
            context[key] = flag_value
    return context


def _action_frame(line: str, config: ClientConfig) -> agent_pb2.Frame:
    """Private. A `<command> [flag=value ...]` line into an action frame"""
    name, _, tail = line.partition(" ")
    action: Message = {"name": name, "context": _context_flags(tail)}
    message: Message = {"version": config.protocol_version, "action": action}
    return agent_pb2.Frame(json=json.dumps(message))


def _read_actions(outgoing: queue.Queue[agent_pb2.Frame | None], config: ClientConfig) -> None:
    """Private. Feeds stdin lines into the request stream; EOF ends it"""
    for line in sys.stdin:
        if line.strip():
            outgoing.put(_action_frame(line.strip(), config))
    outgoing.put(None)


def _pump(
    console: Console,
    channel: grpc.Channel,
    outgoing: queue.Queue[agent_pb2.Frame | None],
    config: ClientConfig,
) -> None:
    """Private. Renders incoming agent frames until the stream ends"""
    stub = agent_pb2_grpc.AgentChannelStub(channel)  # type: ignore[no-untyped-call]
    view = _LogView(console, config)
    try:
        for frame in stub.Channel(iter(outgoing.get, None)):
            view.render(json.loads(frame.json))
    except grpc.RpcError as error:
        status = error.code() if isinstance(error, grpc.Call) else error
        console.print(f"[yellow]agent stream ended: {status}[/]")


def main(address: str | None = None) -> None:
    """Connects to the agent's gRPC transport, prints agent output and
    forwards `<command> flag=value` lines as actions"""
    config = ClientConfig()
    if address is not None:
        config = replace(config, address=address)
    channel = grpc.insecure_channel(config.address)
    outgoing: queue.Queue[agent_pb2.Frame | None] = queue.Queue()
    console = Console(highlight=False)
    console.print(
        Panel.fit(
            "type [bold]<command> flag=value[/] lines · Ctrl+D to quit",
            title=f"[bold cyan]a2ui[/] [dim]{config.address}[/]",
            border_style="cyan",
        )
    )
    reader = threading.Thread(target=_read_actions, args=(outgoing, config), daemon=True)
    reader.start()
    _pump(console, channel, outgoing, config)
    channel.close()


if __name__ == "__main__":
    cli_address = sys.argv[1] if len(sys.argv) > 1 else None
    main(cli_address)
