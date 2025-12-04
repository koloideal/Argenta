![preview](https://i.ibb.co/fTQXbXV/a-minimalist-logo-design-featuring-the-t-OL3-WIOEp-Q5izi-Oyd6-FHq-XQ-CCd1xei4-Q2-Sky-Z0-GPf-SWMA.jpg)

**Argenta** is a simple and elegant framework for building modular CLI applications. It provides a clean and intuitive way to create context-aware command-line tools with isolated command scopes.

Argenta is the **"Simplest"**, **"Most Modular"**, and **"Most Elegant"** way to build interactive CLI applications in Python.

📖 **Read the full documentation:** [argenta.readthedocs.io](https://argenta.readthedocs.io/)<br>
🌍 **Other languages:** [RU](https://github.com/koloideal/Argenta/blob/main/README.ru.md)

---

![preview](https://i.ibb.co/fzWcfgFq/2025-12-04-173045.png)

**Argenta** allows you to build interactive CLI applications incredibly easily. There's no need to manually parse complex command structures or manage state transitions — just use routers and commands!

## ✨ Installing Argenta

Argenta is available on ``PyPI``:

```console
$ python -m pip install argenta
```

or using ``uv``:

```console
$ uv add argenta
```

Argenta officially supports Python 3.12+.

## 🚀 Supported Features & Best Practices

Argenta is ready for the demands of building scalable, robust and maintainable CLI applications.

-   **Interactive Sessions**: Unlike traditional CLI tools, ``Argenta`` creates cyclic sessions, allowing users to execute commands sequentially without restarting the application.
-   **Declarative Syntax**: Commands and their handlers are declared using simple decorators, making the code intuitive and allowing you to focus on "what" you want to do, not "how".
-   **Native DI**: Thanks to integration with `dishka <https://dishka.readthedocs.io/en/stable/>`_, you can easily inject dependencies directly into command handlers, simplifying testing, avoiding mutable globals, and much more.
-   **Automatic Validation and Parsing**: The library handles command-line flags and arguments processing, including parsing, validation, and type conversion.
-   **Flexible Configuration**: You can easily customize system messages, output formatting, create custom handlers for non-standard behavior, and more.

Need something more? Create an **issue**, we're open to suggestions.

## 📝 Why did we create this?

Building complex CLI applications often requires managing different contexts and command scopes. For example, when creating a utility similar to the Metasploit Framework, users need to enter specific scopes (like selecting a scanning module) and then access commands specific only to that context.

Traditional CLI frameworks don't provide an elegant way to handle this kind of modular, context-aware architecture. Argenta was built to solve this problem by providing a simple and concise way to encapsulate CLI functionality in isolated, abstracted environments.

We believe that building CLI applications should be as pleasant as building web applications with modern frameworks. Argenta brings the router pattern and clean separation of concerns to the CLI world.

## 🚀 Quick Start

Here's a simple example to get you started:

```python
# routers.py
from argenta import Router, Response
from argenta.command import Flag, Command

router = Router()

@router.command(Command("hello"))
def handler(response: Response):
    """A simple hello world command"""
    print("Hello, world!")

@router.command(Command("greet", flags=Flag('name')))
def greet_handler(response: Response):
    """Greet a user by name"""
    name_flag = response.input_flags.get_flag_by_name('name')
    if name_flag:
        print(f"Hello, {name_flag.input_value}!")
    else:
        print("Hello, Stranger!")
```

```python
# main.py
from argenta import App, Orchestrator
from .routers import router

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

That's it! You now have a fully functional interactive CLI application.

## 📚 Documentation

Full documentation is available at [argenta.readthedocs.io](https://argenta.readthedocs.io/)

---

MIT 2025 kolo | made by [kolo](https://t.me/kolo_id)
