# Argenta

### Bibliothek zum Erstellen modularer CLI-Anwendungen

Mit Argenta können Sie die CLI-Funktionalität in isolierte, abstrahierte Umgebungen einkapseln. Zum Beispiel: Sie erstellen ein Dienstprogramm ähnlich dem Metasploit Framework, bei dem der Benutzer zuerst in einen bestimmten Scoop eintritt (z. B. ein Modul zum Scannen auswählt) und dann auf eine Reihe von Befehlen zugreift, die nur für diesen Kontext spezifisch sind. Argenta bietet eine einfache und prägnante Möglichkeit, eine solche Architektur zu konstruieren.

---

![preview](https://github.com/koloideal/Argenta/blob/main/imgs/mock_app_preview4.png?raw=True)  

---

# Installation
```bash
pip install argenta
```
or
```bash
poetry add argenta
```

---

# Schnellstart

Ein Beispiel für eine einfache Anwendung
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

# Funktionen in der Entwicklung

- Vollständige Unterstützung für Autocompleter unter Linux

## Vollständige [Dokumentation](https://argenta-docs.vercel.app) | MIT 2025 kolo | made by [kolo](https://t.me/kolo_id)



