import sqlite3
from sqlite3 import Connection
from typing import Iterable

from dishka import Provider, Scope, provide

from argenta import App, Orchestrator


class ConnectionProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def new_connection(self) -> Iterable[Connection]:
        conn = sqlite3.connect(":memory:")
        yield conn
        conn.close()


# 2. Create and configure App
app = App()
# ... you can add routers here ...

# 3. Create Orchestrator, passing our provider
orchestrator = Orchestrator(custom_providers=[ConnectionProvider()])

# 4. Start the application
if __name__ == "__main__":
    orchestrator.start_polling(app)
