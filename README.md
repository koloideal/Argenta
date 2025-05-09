# Argenta

### Библиотека для создания модульных CLI приложeний

![preview](https://github.com/koloideal/Argenta/blob/kolo/imgs/mock_app_preview4.png?raw=True)  

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


router = Router()

@router.command(Command("hello"))
def handler():
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
## Полная [документация](https://argenta-docs.vercel.app) | MIT 2025 kolo | made by [kolo](https://t.me/kolo_id)



