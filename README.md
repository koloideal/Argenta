![preview](https://raw.githubusercontent.com/koloideal/Argenta/main/.github/assets/logo.jpg)

**Argenta** is the command-driven framework for Python.

Build your commands once — run them wherever they're needed: from an interactive terminal to a web UI and beyond.

Argenta is the **"Simplest"**, **"Most Modular"**, and **"Most Elegant"** way to build command-driven applications in Python.

[![PyPI version](https://img.shields.io/pypi/v/argenta)](https://pypi.org/project/argenta/)
[![Python versions](https://img.shields.io/pypi/pyversions/argenta)](https://pypi.org/project/argenta/)
[![Tests](https://github.com/koloideal/Argenta/actions/workflows/ci-tests.yml/badge.svg)](https://github.com/koloideal/Argenta/actions/workflows/ci-tests.yml)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/koloideal/Argenta/actions/workflows/ci-tests.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/koloideal/Argenta/badge)](https://scorecard.dev/viewer/?uri=github.com/koloideal/Argenta)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/15453/badge)](https://www.bestpractices.dev/projects/15453)
[![License](https://img.shields.io/pypi/l/argenta)](https://github.com/koloideal/Argenta/blob/main/LICENSE)

📖 **Read the full documentation:** [argenta.wiki](https://argenta.wiki/)<br>
🌍 **Other languages:** [RU](https://github.com/koloideal/Argenta/blob/main/README.ru.md)

---

![preview](https://raw.githubusercontent.com/koloideal/Argenta/main/.github/assets/demo.gif)

**Argenta** lets you build command-driven applications incredibly easily. There's no need to manually parse complex command structures or manage state transitions — just use routers and commands.

## ✨ Installing Argenta

Argenta is available on ``PyPI``:

```console
$ pip install argenta
```

or using ``uv``:

```console
$ uv add argenta
```

Argenta officially supports Python 3.12+.

## 🚀 Supported Features & Best Practices

Argenta is ready for the demands of building scalable, robust and maintainable applications.

-   **Built-in Runtimes**: A runtime is the way people or programs interact with your application. Argenta ships them out of the box — an interactive terminal session and a web UI today, with more to come — so there's nothing to write yourself. Commands never depend on the runtime, so switching to another one doesn't require rewriting them.
-   **Declarative Syntax**: Commands and their handlers are declared using simple decorators, making the code intuitive and allowing you to focus on "what" you want to do, not "how".
-   **Native DI**: Thanks to integration with [dishka](https://dishka.readthedocs.io/en/stable/), you can easily inject dependencies directly into command handlers, simplifying testing, avoiding mutable globals, and much more.
-   **Automatic Validation and Parsing**: The framework handles flags and arguments processing, including parsing, validation, and type conversion.
-   **Flexible Configuration**: You can easily customize system messages, output formatting, create custom handlers for non-standard behavior, and more.

Need something more? Create an **issue**, we're open to suggestions.

## 📌 Stability & Versioning

Argenta follows [Semantic Versioning](https://semver.org/). The public API is stable: breaking changes are only introduced in major releases, so minor and patch upgrades are always safe.

## 📄 Why did we create this?

As a command-driven application grows, two things get hard: keeping dozens of commands organized, and keeping them independent of the interface they are used through. Most tools leave the first to you and hard-wire the second.

Argenta was built to fix both. Routers split commands into isolated, self-contained modules, and runtimes keep the interface separate from the logic. Building an application should feel as pleasant as working with a modern web framework.

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
from routers import router

app = App()
orchestrator = Orchestrator()

def main() -> None:
    # Include your routers
    app.include_router(router)
    
    # Start the interactive REPL
    orchestrator.run_repl(app)

if __name__ == '__main__':
    main()
```

That's it! You now have a fully functional interactive application. To serve the same commands through another interface, you only change how the app is started — the commands stay untouched.

## 📚 Documentation

Full documentation is available at [argenta.wiki](https://argenta.wiki/)

---

MIT 2025-2026 kolo | made by [kolo](https://t.me/kolo_id)
