"""Runs the A2UI Lit demo: the agent over WebSocket plus the static client"""

import subprocess
import sys
from pathlib import Path

from rich.console import Console


def main() -> None:
    """
    Spawns the agent (`argenta a2ui --verbose`) and a static
    file server for the Lit client, then waits; Ctrl+C stops both
    :return: None
    """
    example_dir = Path(__file__).resolve().parent
    client_port = "8080"
    agent = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "argenta._cli",
            "a2ui",
            "--verbose",
            "examples.example_a2ui.main:main",
        ],
        cwd=example_dir.parent.parent,
    )
    client = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "http.server",
            client_port,
            "--directory",
            str(example_dir / "client"),
        ],
        cwd=example_dir.parent.parent,
    )
    Console().print(f"Client: http://127.0.0.1:{client_port}  |  Agent: ws://127.0.0.1:8765")
    try:
        agent.wait()
    except KeyboardInterrupt:
        agent.terminate()
    client.terminate()
    client.wait()


if __name__ == "__main__":
    main()
