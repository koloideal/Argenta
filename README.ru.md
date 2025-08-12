# Argenta

### Библиотека для создания модульных CLI приложeний

Argenta позволяет инкапсулировать CLI фукциональность в изолированные, абстрагированные **среды**. К примеру: вы создаете утилиту, подобную Metasploit Framework, где пользователь сначала входит в определенный скоуп (например, выбирает модуль для сканирования), а затем получает доступ к набору команд, специфичных только для этого контекста. Argenta предоставляет простой и лаконичный способ для построения такой архитектуры.

---

![preview](https://github.com/koloideal/Argenta/blob/main/imgs/mock_app_preview4.png?raw=True)  

---

# Установка
```bash
pip install argenta
```
or
```bash
poetry add argenta
```

---

# Быстрый старт

Пример простейшего приложения
```python
# routers.py
from argenta.router import Router
from argenta.command import Command
from argenta.response import Response


router = Router()

@router.command(Command("hello"))
def handler(response: Response):
    print("Hello, world!")
```

```python
# main.py
from argenta.app import App
from argenta.orchestrator import Orchestrator
from routers import router

app: App = App()
orchestrator: Orchestrator = Orchestrator()


def main() -> None:
    app.include_router(router)
    orchestrator.start_polling(app)


if __name__ == '__main__':
    main()
```

---

# Фичи в разработке

- Полноценная поддержка автокомплитера на Linux

## Полная [документация](https://argenta-docs.vercel.app) | MIT 2025 kolo | made by [kolo](https://t.me/kolo_id)



