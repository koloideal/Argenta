![preview](https://i.ibb.co/fTQXbXV/a-minimalist-logo-design-featuring-the-t-OL3-WIOEp-Q5izi-Oyd6-FHq-XQ-CCd1xei4-Q2-Sky-Z0-GPf-SWMA.jpg)

**Argenta** is a simple, yet elegant, CLI framework for building modular command-line applications. It provides a clean and intuitive way to create context-aware CLI tools with isolated command scopes.

Argenta is the **"Simplest"**, **"Most Modular"**, and **"Most Elegant"** way to build interactive CLI applications in Python. 

📖 **Read the full documentation:** [argenta-docs.vercel.app](https://argenta-docs.vercel.app)<br>
🌍 **Other languages:** [RU](https://github.com/koloideal/Argenta/blob/main/README.ru.md)

---

![preview](https://i.ibb.co/fzWcfgFq/2025-12-04-173045.png)

```python
>>> from argenta import Router, Command, Response
>>>
>>> router = Router()
>>>
>>> @router.command(Command("hello"))
... def handler(response: Response):
...     print("Hello, world!")
>>>
>>> from argenta import App, Orchestrator
>>>
>>> app = App()
>>> app.include_router(router)
>>> orchestrator = Orchestrator()
>>> orchestrator.start_polling(app)
```

Argenta allows you to build interactive CLI applications extremely easily. There's no need to manually parse complex command structures or manage state transitions — just use routers and commands!

## ✨ Installing Argenta and Supported Versions

Argenta is available on PyPI:

```console
$ python -m pip install argenta
```

or using Poetry:

```console
$ poetry add argenta
```

Argenta officially supports Python 3.7+.

## 🚀 Supported Features & Best Practices

Argenta is ready for the demands of building scalable, robust and maintainable CLI applications.

- Context-Aware Command Routing
- Isolated Command Scopes
- Modular Router Architecture
- Clean Decorator-Based API
- Response Object Pattern
- Command Orchestration
- Interactive Polling Mode
- Fully Type-Annotated
- Easy to Test
- Extensible

Need something more? Create an issue, we listen.

## 📝 Why did we create this?

Building complex CLI applications often requires managing different contexts and command scopes. For example, when creating a utility similar to the Metasploit Framework, users need to enter specific scopes (like selecting a scanning module) and then access commands specific only to that context.

Traditional CLI frameworks don't provide an elegant way to handle this kind of modular, context-aware architecture. Argenta was built to solve this problem by providing a simple and concise way to encapsulate CLI functionality in isolated, abstracted environments.

We believe that building CLI applications should be as pleasant as building web applications with modern frameworks. Argenta brings the router pattern and clean separation of concerns to the CLI world.

## 🚀 Quick Start

Here's a simple example to get you started:

```python
# routers.py
from argenta.router import Router
from argenta.command import Command
from argenta.response import Response

router = Router()

@router.command(Command("hello"))
def handler(response: Response):
    """A simple hello world command"""
    print("Hello, world!")

@router.command(Command("greet"))
def greet_handler(response: Response):
    """Greet a user by name"""
    name = response.args.get("name", "stranger")
    print(f"Hello, {name}!")
```

```python
# main.py
from argenta.app import App
from argenta.orchestrator import Orchestrator
from routers import router

app = App()
orchestrator = Orchestrator()

def main() -> None:
    # Include your routers
    app.include_router(router)
    
    # Start the interactive CLI
    orchestrator.start_polling(app)

if __name__ == '__main__':
    main()
```

That's it! You now have a fully functional interactive CLI application with modular command routing.

## 🔮 Features in Development

- Full autocomplete support on Linux
- Enhanced context switching
- Built-in command history
- Plugin system for extensions

## 📚 Documentation

Full documentation is available at [argenta-docs.vercel.app](https://argenta-docs.vercel.app)

---

MIT 2025 kolo | made by [kolo](https://t.me/kolo_id)



