import sqlite3
from sqlite3 import Connection
from typing import Iterable

from dishka import Provider, Scope, provide


class ConnectionProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def new_connection(self) -> Iterable[Connection]:
        conn = sqlite3.connect(":memory:")
        yield conn
        conn.close()
