import subprocess
import threading
from importlib.util import find_spec
from pathlib import Path

from rich.console import Console


def resolve_watch_root(file_path: str) -> Path | None:
    """Private. The directory watched for changes in --reload mode:
    the parent of the entrypoint file or of the resolved module"""
    path = Path(file_path)
    if path.suffix == ".py":
        return path.resolve().parent
    try:
        spec = find_spec(file_path)
    except (ImportError, ValueError):
        return None
    if spec is not None and spec.origin is not None:
        return Path(spec.origin).resolve().parent
    return None


def _monitor_child(child: subprocess.Popen[bytes], stop: threading.Event) -> None:
    child.wait()
    stop.set()


def _terminate(child: subprocess.Popen[bytes] | None) -> None:
    if child and child.poll() is None:
        child.terminate()
        child.wait()


def _spawn_and_monitor(child_args: list[str], stop: threading.Event) -> subprocess.Popen[bytes]:
    """Private. Spawns the child and sets ``stop`` once it exits on its own"""
    child = subprocess.Popen(child_args, stdin=subprocess.DEVNULL)
    threading.Thread(target=_monitor_child, args=(child, stop), daemon=True).start()
    return child


def _watch_until_change(
    child: subprocess.Popen[bytes], watch_root: Path, stop: threading.Event, console: Console
) -> bool:
    """Private. Blocks on file changes; True means the child must be
    respawned, False means it exited on its own"""
    from watchfiles import watch  # optional dependency of the a2ui extra

    for changes in watch(
        watch_root,
        watch_filter=lambda _change, path: path.endswith(".py"),
        stop_event=stop,
    ):
        if child.poll() is not None:
            return False
        changed = sorted(path for _change, path in changes)
        console.print(f"[dim]a2ui: {Path(changed[0]).name} changed, restarting[/dim]")
        return True
    return False


def supervise_cli(child_args: list[str], watch_root: Path, console: Console) -> int:
    """Private. Runs the `argenta a2ui` child process and respawns it whenever
    python files under ``watch_root`` change; exits with the last child's code"""
    child: subprocess.Popen[bytes] | None = None
    try:
        while True:
            stop = threading.Event()
            child = _spawn_and_monitor(child_args, stop)
            if _watch_until_change(child, watch_root, stop, console):
                _terminate(child)
            else:
                break
    except KeyboardInterrupt:
        console.print("[dim]a2ui: interrupted, shutting down[/dim]")
    finally:
        _terminate(child)
    if child is None:
        return 0
    return child.returncode or 0
