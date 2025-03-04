# Argenta

---

## Описание
**Argenta** — Python library for creating custom shells

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

Пример простейшей оболочки с командой без флагов
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
from routers import router

app: App = App()

def main() -> None:
    app.include_router(router)
    app.start_polling()

    
if __name__ == '__main__':
    main()
```
Пример оболочки с командой, у которой зарегистрированы флаги

```python
# routers.py
import re
from argenta.router import Router
from argenta.command import Command
from argenta.command.params.flag import FlagsGroup, Flag

router = Router()

list_of_flags = [
    Flag(flag_name='host',
         flag_prefix='--',
         possible_flag_values=re.compile(r'^192.168.\d{1,3}.\d{1,3}$')),
    Flag(flag_name='port',
         flag_prefix='---',
         possible_flag_values=re.compile(r'^[0-9]{1,4}$'))
]


@router.command(Command("hello"))
def handler():
    print("Hello, world!")


@router.command(Command(trigger="ssh",
                        description='connect via ssh',
                        flags=FlagsGroup(list_of_flags)))
def handler_with_flags(flags: dict):
    for flag in flags:
        print(f'Flag name: {flag['name']}\n
              f'Flag value: {flag['value']}')
```

---

# *classes* :

---

##  *class* :: `App` 
Класс, определяющий поведение и состояние оболочки

### Конструктор
```python
App(prompt: str = 'Enter a command',
    initial_greeting: str = '\nHello, I am Argenta\n',
    farewell_message: str = '\nGoodBye\n',
    exit_command: str = 'Q',
    exit_command_description: str = 'Exit command',
    system_points_title: str = 'System points:',
    ignore_exit_command_register: bool = True,
    ignore_command_register: bool = False,
    line_separate: str = '',
    command_group_description_separate: str = '',
    repeat_command_groups: bool = True,
    print_func: Callable[[str], None] = print)
```
**Аргументы:**
- **name : mean**
- `prompt` (`str`): Сообщение перед вводом команды.
- `initial_greeting` (`str`): Приветственное сообщение при запуске.
- `farewell_message` (`str`): Сообщение при выходе.
- `exit_command` (`str`): Команда выхода (по умолчанию `'Q'`).
- `exit_command_description` (`str`): Описание команды выхода.
- `system_points_title` (`str`): Заголовок перед списком системных команд.
- `ignore_exit_command_register` (`bool`): Игнорировать регистр команды выхода.
- `ignore_command_register` (`bool`): Игнорировать регистр всех команд.
- `line_separate` (`str`): Разделительная строка между командами.
- `command_group_description_separate` (`str`): Разделитель между группами команд.
- `repeat_command_groups` (`bool`): Повторять описание команд перед вводом.
- `print_func` (`Callable[[str], None]`): Функция вывода текста в терминал (по умолчанию `print`).

---

### ***methods***     

---

**App().**`start_polling() -> None`  

*method mean* **::** запускает жизненный цикл приложения

---

**App().**`include_router(router: Router) -> None`  

*param* `router: Router` **::** регистрируемый роутер

*method mean* **::** регистрирует роутер в приложении

---

**App().**`set_initial_message(message: str) -> None`  

*param* `message: str` **::** устанавливаемое приветственное сообщение  
*example* **::** `"Hello, I'm a example app"`

*method mean* **::** устанавливает сообщение, которое будет отображено при запуске программы

---

**App().**`set_farewell_message(message: str) -> None`  

*param* `message: str` **::** устанавливаемое сообщение при выходе  
*example* **::** `"GoodBye !"`

*method mean* **::** устанавливает сообщение, которое будет отображено при выходе

---

**App().**`set_description_message_pattern(pattern: str) -> None`  

*param* `pattern: str` **::** паттерн описания команды при её выводе в консоль  
*example* **::** `"[{command}] *=*=* {description}"`

*method mean* **::** устанавливает паттерн описания команд, который будет использован
при выводе в консоль

---

**App().**`set_repeated_input_flags_handler(handler: Callable[[str], None]) -> None`  

*param* `handler: Callable[[str], None]` **::** функция или лямбда функция, которой будет передано управление при
вводе юзером повторяющихся флагов
*example* **::** `lambda raw_command: print_func(f'Repeated input flags: "{raw_command}"')`

*method mean* **::** устанавливает функцию, которой будет передано управление при
вводе юзером повторяющихся флагов

---

**App().**`set_invalid_input_flags_handler(self, handler: Callable[[str], None]) -> None`  

*param* `handler: Callable[[str], None]` **::** функция или лямбда функция, которой будет передано управление при
вводе юзером команды с некорректным синтаксисом флагов
*example* **::** `lambda raw_command: print_func(f'Incorrect flag syntax: "{raw_command}"')`

*method mean* **::** устанавливает функцию, которой будет передано управление при
вводе юзером команды с некорректным синтаксисом флагов

---

**App().**`set_unknown_command_handler(self, handler: Callable[[str], None]) -> None`  

*param* `handler: Callable[[str], None]` **::** функция или лямбда функция, которой будет передано управление при
вводе юзером неизвестной команды
*example* **::** `lambda command: print_func(f"Unknown command: {command.get_string_entity()}")`

*method mean* **::** устанавливает функцию, которой будет передано управление при
вводе юзером неизвестной команды

---

**App().**`set_empty_command_handler(self, handler: Callable[[str], None]) -> None`  

*param* `handler: Callable[[str], None]` **::** функция или лямбда функция, которой будет передано управление при
вводе юзером пустой команды
*example* **::** `lambda: print_func(f'Empty input command')`

*method mean* **::** устанавливает функцию, которой будет передано управление при
вводе юзером пустой команды

---

### Примечания  

- В устанавливаемом паттерне сообщения описания команды необходимы быть два ключевых слова: 
`command` и `description`, каждое из которых должно быть заключено в фигурные скобки, после обработки
паттерна на места этих ключевых слов будут подставлены соответствующие значения команды, при отсутствии
этих двух ключевых слов будет вызвано исключение `InvalidDescriptionMessagePatternException`

- Команды приложения не должны повторяться, при значении атрибута `ignore_command_register` равным `True`
допускается создание обработчиков для разных регистров одинаковых символов в команде, для примера `u` и `U`,
при значении атрибута `ignore_command_register` класса `App` равным `False` тот же пример вызывает исключение 
`RepeatedCommandInDifferentRoutersException`. Исключение вызывается только при наличии пересекающихся команд 
у __<u>разных</u>__ роутеров




### Исключения

- `InvalidRouterInstanceException` — Переданный объект в метод `App().include_router()` не является экземпляром класса `Router`.
- `InvalidDescriptionMessagePatternException` — Неправильный формат паттерна описания команд.
- `IncorrectNumberOfHandlerArgsException` — У обработчика нестандартного поведения зарегистрировано неверное количество аргументов(в большинстве случаев у него должен быть один аргумент).
- `NoRegisteredRoutersException` — Отсутствуют зарегистрированные роутеры.
- `NoRegisteredHandlersException` — У роутера нет ни одного обработчика команд.
- `RepeatedCommandInDifferentRoutersException` — Одна и та же команда зарегистрирована в разных роутерах.

---

##  *class* :: `Router` 
Класс, который определяет и конфигурирует обработчики команд

### Конструктор
```python
Router(title: str = 'Commands group title:',
       name: str = 'subordinate')
```



**Аргументы:**
- **name : mean**
- `title` (`str`): Заголовок группы команд.
- `name` (`str`): Персональное название роутера

---

### ***methods***     

---

**`@`Router().**`command(command: Command)`  

*param* `command: Command` **::** экземпляр класса `Command`, который определяет строковый триггер команды,
допустимые флаги команды и другое
*example* **::** `Command(command='ssh', description='connect via ssh')`

*method mean* **::** декоратор, который регистрирует функцию как обработчик команды

---

**Router().**`get_name() -> str`  

*method mean* **::** возвращает установленное название роутера

---

**Router().**`get_title() -> str`  

*method mean* **::** возвращает установленный заголовок группы команд данного роутера

---

**Router().**`get_all_commands() -> list[str]`  

*method mean* **::** возвращает все зарегистрированные команды для данного роутера

---

### Исключения
- `RepeatedCommandException` - Одна и та же команда зарегистрирована в одном роутере
- `RepeatedFlagNameException` - Повторяющиеся зарегистрированные флаги в команде
- `TooManyTransferredArgsException` - Слишком много зарегистрированных аргументов у обработчика команды
- `RequiredArgumentNotPassedException` - Не зарегистрирован обязательный аргумент у обработчика команды(аргумент, через который будут переданы флаги введённой команды)
- `IncorrectNumberOfHandlerArgsException` - У обработчика нестандартного поведения зарегистрировано неверное количество аргументов(в большинстве случаев у него должен быть один аргумент)

---

##  *class* :: `Command` 
Класс, экземпляр которого определяет строковый триггер хэндлера и конфигурирует его атрибуты

### Конструктор
```python
Command(trigger: str,
        description: str = None,
        flags: Flag | FlagsGroup = None)
```

**Аргументы:**
- **name : mean**
- `trigger` (`str`): Строковый триггер
- `description` (`str`): Описание команды, которое будет выведено в консоль при запуске оболочки
- `flags` (`Flag | FlagsGroup`): Флаги, которые будут обработаны при их наличии во вводе юзера

---

**Command().**`get_trigger() -> str`  

*method mean* **::** возвращает строковый триггер экземпляра

---

**Command().**`get_description() -> str`  

*method mean* **::** возвращает описание команды

---

**Command().**`get_registered_flags() -> FlagsGroup | None`  

*method mean* **::** возвращает зарегистрированные флаги экземпляра

---

### Исключения 
- `UnprocessedInputFlagException` - Некорректный синтаксис ввода команды
- `RepeatedInputFlagsException` - Повторяющиеся флаги во введённой команде
- `EmptyInputCommandException` - Введённая команда является пустой(не содержит символов)  

**Примечание**
Все вышеуказанные исключения класса `Command` вызываются в рантайме запущенным экземпляром класса
`App`, а также по дефолту обрабатываются, при желании можно задать пользовательские
обработчики для этих исключений ([подробнее см.](#methods-))

---

##  *class* :: `Flag` 
Класс, экземпляры которого в большинстве случаев должны передаваться при создании
экземпляра класса `Command` для регистрации допустимого флага при вводе юзером команды

### Конструктор
```python
Flag(flag_name: str,
     flag_prefix: Literal['-', '--', '---'] = '-',
     ignore_flag_value_register: bool = False,
     possible_flag_values: list[str] | Pattern[str] = False)
```

---

**Аргументы:**
- **name : mean**
- `flag_name` (`str`): Имя флага
- `flag_prefix` (`Literal['-', '--', '---']`): Префикс команды, допустимым значением является от одного до трёх минусов
- `ignore_flag_value_register` (`bool`): Будет ли игнорироваться регистр значения введённого флага 
- `possible_flag_values` (`list[str] | Pattern[str]`): Множество допустимых значений флага, может быть задано 
списком с допустимыми значениями или регулярным выражением (рекомендуется `re.compile(r'example exspression')`)

---

### ***methods***     

---

**Flag().**`get_sring_entity() -> str`  

*method mean* **::** возвращает строковое представление флага(префикс + имя)

---

**Flag().**`get_flag_name() -> str`  

*method mean* **::** возвращает имя флага

---

**Flag().**`get_flag_prefix() -> str`  

*method mean* **::** возвращает префикс флага

---

##  *class* :: `FlagsGroup` 
Класс, объединяющий список флагов в один объект, используется в качестве 
передаваемого аргумента `flags` экземпляру класса `Command`, при регистрации
хэндлера

### Конструктор
```python
FlagsGroup(flags: list[Flag] = None)
```

---

**Аргументы:**
- **name : mean**
- `flags` (`list[Flag]`): Список флагов, которые будут объединены в одну группу

---

### ***methods***     

---

**FlagsGroup().**`get_flags() -> list[Flag]`  

*method mean* **::** возвращает зарегистрированные флаги

---

# Тесты

Запуск тестов:

```bash
python -m unittest discover
```
or
```bash
python -m unittest discover -v
```
