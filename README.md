# Argenta

---

## Описание
**Argenta** — Python library for creating custom shells

![prewiev](https://github.com/koloideal/Argenta/blob/kolo/imgs/mock_app_preview_last.png?raw=True)  
Пример внешнего вида TUI, написанного с помощью Argenta  

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

Пример простейшей оболочки с командой без зарегистрированных флагов
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
from argenta.command.flag import Flags, Flag, InputFlags

router = Router()

registered_flags = Flags(
    Flag(name='host',
         prefix='--',
         possible_values=re.compile(r'^192.168.\d{1,3}.\d{1,3}$')),
    Flag('port', '--', re.compile(r'^[0-9]{1,4}$')))


@router.command(Command("hello"))
def handler():
    print("Hello, world!")


@router.command(Command(trigger="ssh",
                        description='connect via ssh',
                        flags=registered_flags))
def handler_with_flags(flags: InputFlags):
    for flag in flags:
        print(f'Flag name: {flag.get_name()}\n'
              f'Flag value: {flag.get_value()}')
```

---

# *classes* :

---

##  *class* : : `App` 
Класс, определяющий поведение и состояние оболочки

### Конструктор
```python
App(prompt: str = 'What do you want to do?\n',
    initial_message: str = 'Argenta',
    farewell_message: str = 'See you',
    exit_command: str = 'Q',
    exit_command_description: str = 'Exit command',
    system_points_title: str = 'System points:',
    ignore_command_register: bool = True,
    dividing_line: StaticDividingLine | DynamicDividingLine = StaticDividingLine(),
    repeat_command_groups: bool = True,
    print_func: Callable[[str], None] = Console().print)
```
**Аргументы:**
- **name : mean**
- `prompt` (`str`): Сообщение перед вводом команды.
- `initial_message` (`str`): Приветственное сообщение при запуске.
- `farewell_message` (`str`): Сообщение при выходе.
- `exit_command` (`str`): Команда выхода (по умолчанию `'Q'`).
- `exit_command_description` (`str`): Описание команды выхода.
- `system_points_title` (`str`): Заголовок перед списком системных команд.
- `ignore_command_register` (`bool`): Игнорировать регистр всех команд.
- `dividing_line` (`StaticDividingLine | DynamicDividingLine`): Разделительная строка.
- `repeat_command_groups` (`bool`): Повторять описание команд перед вводом.
- `print_func` (`Callable[[str], None]`): Функция вывода текста в терминал.

---

### ***methods***     

---

#### **.start_polling() -> `None`**  

*method mean* **::** Запускает цикл обработки ввода

---

#### **.include_router(router: Router) -> `None`**  

*param* `router: Router` **::** Регистрируемый роутер  
*required* **::** True

*method mean* **::** Регистрирует роутер в оболочке

---

#### **.include_routers(\*routers: Router) -> `None`**  

*param* `routers: Router` **::** Неограниченное количество регистрируемых роутеров    
*required* **::** True

*method mean* **::** Регистрирует роутер в оболочке

---

#### **.set_description_message_pattern(pattern: str) -> `None`**  

*param* `pattern: str` **::** Паттерн описания команды при её выводе в консоль  
*required* **::** True  
*example* **::** `"[{command}] *=*=* {description}"`

*method mean* **::** Устанавливает паттерн описания команд, который будет использован
при выводе в консоль

---

#### **.add_message_on_startup(message: str) -> `None`**  

*param* `message: str` **::** Сообщение, которое будет выведено при запуске приложения 
*required* **::** True  
*example* **::** `Message on startup`

*method mean* **::** Устанавливает паттерн описания команд, который будет использован
при выводе в консоль

---

<a name="custom_handler"></a>
#### **.repeated_input_flags_handler: `Callable[[str], None])`**

*example* **::** `lambda raw_command: print_func(f'Repeated input flags: "{raw_command}"')`

*attr mean* **::** Устанавливает функцию, которой будет передано управление при
вводе юзером повторяющихся флагов

---

#### **.invalid_input_flags_handler: `Callable[[str], None])`**  

*example* **::** `lambda raw_command: print_func(f'Incorrect flag syntax: "{raw_command}"')`

*attr mean* **::** Устанавливает функцию, которой будет передано управление при
вводе юзером команды с некорректным синтаксисом флагов

---

#### **.unknown_command_handler: `Callable[[str], None]`**  

*example* **::** `lambda command: print_func(f"Unknown command: {command.get_string_entity()}")`

*attr mean* **::** Устанавливает функцию, которой будет передано управление при
вводе юзером неизвестной команды

---

#### **.empty_command_handler: `Callable[[str], None])`**  

*example* **::** `lambda: print_func(f'Empty input command')`

*attr mean* **::** Устанавливает функцию, которой будет передано управление при
вводе юзером пустой команды

---

### Примечания  

- В устанавливаемом паттерне сообщения описания команды необходимы быть два ключевых слова: 
`command` и `description`, каждое из которых должно быть заключено в фигурные скобки, после обработки
паттерна на места этих ключевых слов будут подставлены соответствующие атрибуты команды, при отсутствии
этих двух ключевых слов будет вызвано исключение `InvalidDescriptionMessagePatternException`

- Команды оболочки не должны повторяться, при значении атрибута `ignore_command_register` равным `True`
допускается создание обработчиков для разных регистров одинаковых символов в команде, для примера `u` и `U`,
при значении атрибута `ignore_command_register` класса `App` равным `False` тот же пример вызывает исключение 
`RepeatedCommandInDifferentRoutersException`. Исключение вызывается только при наличии пересекающихся команд 
у __<u>разных</u>__ роутеров

- Наиболее частые сообщение при запуске предопределены и доступны для быстрого
использования: `argenta.app.defaults.PredeterminedMessages`




### Исключения

- `InvalidRouterInstanceException` — Переданный объект в метод `App().include_router()` не является экземпляром класса `Router`.
- `InvalidDescriptionMessagePatternException` — Неправильный формат паттерна описания команд.
- `IncorrectNumberOfHandlerArgsException` — У обработчика нестандартного поведения зарегистрировано неверное количество аргументов(в большинстве случаев у него должен быть один аргумент).
- `NoRegisteredHandlersException` — У роутера нет ни одного обработчика команд.

---

##  *class* :: `StaticDivideLine` 
Класс, экземпляр которого представляет собой строковый разделитель фиксированной длины

### Конструктор
```python
StaticDivideLine(unit_part: str = '-', 
                 length: int = 25)
```

**Аргументы:**
- **name : mean**
- `unit_part` (`str`): Единичная часть строкового разделителя
- `length` (`int`): Длина строкового разделителя

---

##  *class* :: `DinamicDivideLine` 
Строковый разделитель динамической длины, которая определяется длиной обрамляемого вывода команды

### Конструктор
```python
DinamicDivideLine(unit_part: str = '-')
```

**Аргументы:**
- **name : mean**
- `unit_part` (`str`): Единичная часть строкового разделителя

---

##  *class* :: `Router` 
Класс, который определяет и конфигурирует обработчики команд

### Конструктор
```python
Router(title: str = 'Commands group title:',
       name: str = 'Default')
```



**Аргументы:**
- **name : mean**
- `title` (`str`): Заголовок группы команд.
- `name` (`str`): Персональное название роутера

---

### ***methods***     

---

#### **command(command: Command)**  

*param* `command: Command` **::** Экземпляр класса `Command`, который определяет строковый триггер команды,
допустимые флаги команды и другое  
*required* **::** True  
*example* **::** `Command(command='ssh', description='connect via ssh')`

*method mean* **::** Декоратор, который регистрирует функцию как обработчик команды

---

#### **.get_name() -> `str`**  

*method mean* **::** Возвращает установленное название роутера

---

#### **.get_title() -> `str`**  

*method mean* **::** Возвращает установленный заголовок группы команд данного роутера

---


### Исключения
- `RepeatedFlagNameException` - Повторяющиеся зарегистрированные флаги в команде
- `TooManyTransferredArgsException` - Слишком много зарегистрированных аргументов у обработчика команды
- `RequiredArgumentNotPassedException` - Не зарегистрирован обязательный аргумент у обработчика команды(аргумент, через который будут переданы флаги введённой команды)
- `IncorrectNumberOfHandlerArgsException` - У обработчика нестандартного поведения зарегистрировано неверное количество аргументов(в большинстве случаев у него должен быть один аргумент)
- `TriggerCannotContainSpacesException` - У регистрируемой команды в триггере содержатся пробелы

---

##  *class* :: `Command` 
Класс, экземпляр которого определяет строковый триггер хэндлера и конфигурирует его атрибуты

### Конструктор
```python
Command(trigger: str,
        description: str = None,
        flags: Flag | Flags = None)
```

**Аргументы:**
- **name : mean**
- `trigger` (`str`): Строковый триггер
- `description` (`str`): Описание команды, которое будет выведено в консоль при запуске оболочки
- `flags` (`Flag | Flags`): Флаги, которые будут обработаны при их наличии во вводе юзера

---

#### **.get_trigger() -> `str`**  

*method mean* **::** Возвращает строковый триггер экземпляра

---

#### **.get_description() -> `str`**  

*method mean* **::** Возвращает описание команды

---

#### **.get_registered_flags() -> `Flags | None`**  

*method mean* **::** Возвращает зарегистрированные флаги экземпляра

---

### Исключения 
- `UnprocessedInputFlagException` - Некорректный синтаксис ввода команды
- `RepeatedInputFlagsException` - Повторяющиеся флаги во введённой команде
- `EmptyInputCommandException` - Введённая команда является пустой(не содержит символов)  

**Примечание**
Все вышеуказанные исключения класса `Command` вызываются в рантайме запущенным экземпляром класса
`App`, а также по дефолту обрабатываются, при желании можно задать пользовательские
обработчики для этих исключений ([подробнее см.](#custom_handler))

---

##  *class* :: `Flag` 
Класс, экземпляры которого в большинстве случаев передаются при создании
экземпляра класса `Command` для регистрации допустимого флага при вводе юзером команды

### Конструктор
```python
Flag(name: str,
     prefix: typing.Literal['-', '--', '---'] = '-',
     possible_values: list[str] | typing.Pattern[str] | False = True)
```

---

**Аргументы:**
- **name : mean**
- `name` (`str`): Имя флага
- `prefix` (`Literal['-', '--', '---']`): Префикс команды, допустимым значением является от одного до трёх минусов
- `possible_values` (`list[str] | Pattern[str] | bool`): Множество допустимых значений флага, может быть задано
списком с допустимыми значениями или регулярным выражением (рекомендуется `re.compile(r'example exspression')`), при значении
аргумента `False` у введённого флага не может быть значения, иначе будет вызвано исключение и обработано соответствующим 
еррор-хэндлером

---

### ***methods***     

---

#### **.get_string_entity() -> `str`**  

*method mean* **::** Возвращает строковое представление флага(префикс + имя)

---

#### **.get_name() -> `str`**  

*method mean* **::** Возвращает имя флага

---

#### **.get_prefix() -> `str`**  

*method mean* **::** Возвращает префикс флага

---

##  *class* :: `InputFlag` 
Класс, экземпляры которого являются введёнными флагами команды, передаётся в хэндлер команды
через `InputFlags`

---

### Примечания  

- Наиболее часто используемые флаги предопределены и доступны для быстрого использования:
`argenta.command.flag.defaults.PredeterminedFlags` 

---


### Конструктор
```python
InputFlag(name: str,
         prefix: typing.Literal['-', '--', '---'] = '-',
         value: str = None)
```

---

**Аргументы:**
- **name : mean**
- `name` (`str`): Имя флага
- `prefix` (`Literal['-', '--', '---']`): Префикс команды, допустимым значением является от одного до трёх минусов
- `value` (`str`): Значение введённого флага, если оно есть

---

### ***methods***     

---

#### **.get_value() -> `str | None`**  

*method mean* **::** Возвращает значение введённого флага

---

##  *class* :: `Flags` 
Класс, объединяющий список флагов в один объект, используется в качестве 
передаваемого аргумента `flags` экземпляру класса `Command`, при регистрации
хэндлера

### Конструктор
```python
Flags(*flags: Flag)
```

---

**Аргументы:**
- **name : mean**
- `*flags` (`Flag`): Неограниченное количество передаваемых флагов

---

### ***methods***     

---

#### **.get_flags() -> `list[Flag]`**  

*method mean* **::** Возвращает зарегистрированные флаги

---

#### **.add_flag(flag: Flag) -> `None`**  

*method mean* **::** Добавляет флаг в группу

---

#### **.add_flags(flags: list[Flag]) -> `None`**  

*method mean* **::** Добавляет флаги в группу

---

#### **.get_flag(name: str) -> `Flag | None`**  

*param* `name: str` **::** Строковый триггер флага без префикса
*required* **::** True  
*example* **::** `'host'`

*method mean* **::** Возвращает флаг по его триггеру или `None`, если флаг не найден

---

##  *class* :: `InputFlags` 
Класс, объединяющий список введённых флагов в один объект, передаётся соответствующему хэндлеру
в качестве аргумента

### Конструктор
```python
InputFlags(*flags: Flag)
```

---

**Аргументы:**
- **name : mean**
- `*flags` (`InputFlag`): Неограниченное количество передаваемых флагов

---

### ***methods***     

---

#### **.get_flags() -> `list[Flag]`**  

*method mean* **::** Возвращает введённые флаги

---

#### **.get_flag(name: str) -> `InputFlag | None`**  

*param* `name: str` **::** Строковый триггер флага без префикса
*required* **::** True  
*example* **::** `'host'`

*method mean* **::** Возвращает введённый флаг по его триггеру или `None`, если флаг не найден

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
