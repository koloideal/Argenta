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


# 2. Создаем и настраиваем App
app = App()
# ... здесь можно добавить роутеры ...

# 3. Создаем Orchestrator, передавая наш провайдер
orchestrator = Orchestrator(custom_providers=[ConnectionProvider()])

# 4. Запускаем приложение
if __name__ == "__main__":
    orchestrator.start_polling(app)
