import io
from contextlib import redirect_stdout
from time import time

from argenta import App


def get_time_of_pre_cycle_setup(app: App) -> float:
    """
    Public. Return time of pre cycle setup
    :param app: app instance for testing time of pre cycle setup
    :return: time of pre cycle setup as float
    """
    start = time()
    with redirect_stdout(io.StringIO()):
        app._pre_cycle_setup() # pyright: ignore[reportPrivateUsage]
    end = time()
    return end - start
