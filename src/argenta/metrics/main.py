import io
from contextlib import redirect_stdout
from time import time

from argenta.router import Router
from argenta.command import Command
from argenta.response import Response
from argenta.response.status import Status
from argenta.command.flag import Flag, Flags
from argenta.app import App


def get_time_of_pre_cycle_setup(app: App) -> float:
    start = time()
    with redirect_stdout(io.StringIO()):
        app.pre_cycle_setup()
    end = time()
    return end - start








