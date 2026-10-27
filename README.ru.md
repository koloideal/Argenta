![preview](https://raw.githubusercontent.com/koloideal/Argenta/main/.github/assets/logo.jpg)

**Argenta** — это фреймворк для Python-приложений, построенных вокруг команд.

Опишите команды один раз и запускайте их там, где они нужны: в терминале, в веб-интерфейсе и не только.

Argenta — это **"Самый простой"**, **"Самый модульный"** и **"Самый элегантный"** способ создавать на Python приложения, построенные вокруг команд. 

[![PyPI version](https://img.shields.io/pypi/v/argenta)](https://pypi.org/project/argenta/)
[![Python versions](https://img.shields.io/pypi/pyversions/argenta)](https://pypi.org/project/argenta/)
[![Tests](https://github.com/koloideal/Argenta/actions/workflows/ci-tests.yml/badge.svg)](https://github.com/koloideal/Argenta/actions/workflows/ci-tests.yml)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/koloideal/Argenta/actions/workflows/ci-tests.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/koloideal/Argenta/badge)](https://scorecard.dev/viewer/?uri=github.com/koloideal/Argenta)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/15453/badge)](https://www.bestpractices.dev/projects/15453)
[![License](https://img.shields.io/pypi/l/argenta)](https://github.com/koloideal/Argenta/blob/main/LICENSE)

📖 **Читайте полную документацию:** [argenta.wiki](https://argenta.wiki/)<br>
🌍 **Другие языки:** [EN](https://github.com/koloideal/Argenta/blob/main/README.md)

---

![preview](https://raw.githubusercontent.com/koloideal/Argenta/main/.github/assets/demo.gif)

**Argenta** позволяет создавать такие приложения невероятно легко. Не нужно вручную парсить сложные структуры команд или управлять переходами состояний — просто используйте роутеры и команды.

## ✨ Установка Argenta 

Argenta доступна на ``PyPI``:

```console
$ pip install argenta
```

или с использованием ``uv``:

```console
$ uv add argenta
```

Argenta официально поддерживает Python 3.12+.

## 🚀 Поддерживаемые возможности и лучшие практики

Argenta готова к требованиям создания масштабируемых, надежных и поддерживаемых приложений.

-   **Встроенные рантаймы**: Рантайм — это способ, которым люди или программы работают с вашим приложением. Argenta поставляет их из коробки: сейчас это интерактивная терминальная сессия и веб-интерфейс, дальше будет больше, так что писать самому ничего не нужно. Команды не зависят от рантайма, поэтому переход на другой не требует их переписывать.
-   **Декларативный синтаксис**: Команды и их обработчики объявляются с помощью простых декораторов, что делает код интуитивно понятным и позволяет сосредоточиться на том, "что" вы хотите сделать, а не "как".
-   **Нативный DI**: Благодаря интеграции с [dishka](https://dishka.readthedocs.io/en/stable/), вы можете легко внедрять зависимости прямо в обработчики команд, что упрощает их тестирование, позволяет избежать мутабельных глобалов и многое другое.
-   **Автоматическая валидация и парсинг**: Фреймворк берёт на себя обработку флагов и аргументов, включая их парсинг, валидацию и преобразование типов.
-   **Гибкая настройка**: Вы можете легко кастомизировать системные сообщения, форматирование вывода, создавать кастомные обработчики нестандартного поведения и т.д.

Нужно что-то еще? Создайте **issue**, мы открыты к предложениям.

## 📌 Стабильность и версионирование

Argenta следует [Semantic Versioning](https://semver.org/lang/ru/). Публичный API стабилен: обратно несовместимые изменения вводятся только в мажорных релизах, поэтому минорные и патч-обновления всегда безопасны.

## 📄 Зачем мы это создали?

Когда приложение растёт, становится сложно две вещи: держать в порядке десятки команд и не привязывать их к интерфейсу, через который с ними работают. Большинство инструментов первое оставляют на вас, а второе зашивают намертво.

Argenta создана, чтобы решить обе проблемы. Роутеры разбивают команды на изолированные, самодостаточные модули, а рантаймы отделяют интерфейс от логики. Создавать приложения должно быть так же приятно, как работать с современным веб-фреймворком.

## 🚀 Быстрый старт

Вот простой пример для начала работы:

```python
# routers.py
from argenta import Router, Response
from argenta.command import Flag, Command

router = Router()

@router.command(Command("hello"))
def handler(response: Response):
    """Простая команда hello world"""
    print("Привет, мир!")

@router.command(Command("greet", flags=Flag('name')))
def greet_handler(response: Response):
    """Поприветствовать пользователя по имени"""
    name_flag = response.input_flags.get_flag_by_name('name')
    if name_flag:
        print(f"Привет, {name_flag.input_value}!")
    else:
        print("Привет, Незнакомец!")
```

```python
# main.py
from argenta import App, Orchestrator
from routers import router

app = App()
orchestrator = Orchestrator()

def main() -> None:
    # Подключите ваши роутеры
    app.include_router(router)
    
    # Запустите интерактивный REPL
    orchestrator.run_repl(app)

if __name__ == '__main__':
    main()
```

Вот и всё! Теперь у вас есть полностью функциональное интерактивное приложение. Чтобы отдать те же команды через другой интерфейс, меняется только способ запуска. Сами команды остаются нетронутыми.

## 📚 Документация

Полная документация доступна на [argenta.wiki](https://argenta.wiki/)

---

MIT 2025-2026 kolo | made by [kolo](https://t.me/kolo_id)
