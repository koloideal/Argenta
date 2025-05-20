# Argenta

### Library for creating modular CLI applications

#### RU - [README.ru.md](https://github.com/koloideal/Argenta/blob/kolo/README.ru.md) • DE - [README.de.md](https://github.com/koloideal/Argenta/blob/kolo/README.de.md)

![preview](https://github.com/koloideal/Argenta/blob/kolo/imgs/mock_app_preview4.png?raw=True)  

---

# Installing
```bash
pip install argenta
```
or
```bash
poetry add argenta
```

---

# Quick start

An example of a simple application
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

# Features in development

- Full support for autocompleter on Linux

## Full [docs](https://argenta-docs.vercel.app) | MIT 2025 kolo | made by [kolo](https://t.me/kolo_id)



