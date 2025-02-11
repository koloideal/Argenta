# Argenta

---

## Описание
**Argenta** — это библиотека для создания CLI-приложений на Python. Она предоставляет удобные инструменты для маршрутизации команд и обработки пользовательского ввода.

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
Пример базового CLI-приложения с Argenta:
```python
#routers.py
from argenta.router import Router

router = Router()

@router.command("hello")
def hello():
    print("Hello, world!")

@router.unknown_command
def unlnown_command(command):
    print(f'Command "{command}" undefined')
```
```python
#main.py
from argenta.app import App
from routers import router

app: App = App()

def main() -> None:
    app.include_router(router)
    app.start_polling()

    
if __name__ == '__main__':
    main()
```

---

# Техническая документация

---

## declared *classes* :

---

###  *class* :: `App` 
Класс, определяющий поведение и состояние приложения

#### Конструктор
```python
App(prompt: str = 'Enter a command',
    initial_greeting: str = '\nHello, I am Argenta\n',
    farewell_message: str = '\nGoodBye\n',
    exit_command: str = 'Q',
    exit_command_description: str = 'Exit command',
    exit_command_title: str = 'System points:',
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
- `exit_command_title` (`str`): Заголовок перед списком команд выхода.
- `ignore_exit_command_register` (`bool`): Игнорировать регистр команды выхода.
- `ignore_command_register` (`bool`): Игнорировать регистр всех команд.
- `line_separate` (`str`): Разделительная строка между командами.
- `command_group_description_separate` (`str`): Разделитель между группами команд.
- `repeat_command_groups` (`bool`): Повторять описание команд перед вводом.
- `print_func` (`Callable[[str], None]`): Функция вывода текста в терминал (по умолчанию `print`).

---

#### **declared *methods***     

---

**App().**`start_polling() -> None`  

*method mean* **::** запускает жизненный цикл приложения

---

**App().**`include_router(router: Router, is_main: bool = False) -> None`  

*param* `router: Router` **::** регистрируемый роутер  

*param* `is_main: bool` **::** будет ли являться регистрируемый роутер главным  
*example* **::** `True` или `False` 

*method mean* **::** регистрирует роутер в приложении

---

**App().**`set_initial_message(message: str) -> None`  

*param* `message: str` **::** устанавливаемое приветственное сообщение  
*example* **::** `"Hello, I'm a cli example app"`

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

*method mean* **::** устанавливает приветственное сообщение

---

**App().**`get_main_router() -> Router`  

*method mean* **::** возвращает `Router()`, который является главным в приложении

---

**App().**`get_all_app_commands() -> list[str]`  

*method mean* **::** возвращает список команд всех зарегистрированных роутеров, сохраняя их регистр

---

#### Примечания  

-  Среди зарегистрированных в приложении роутеров должен быть один главный, является ли роутер главным
определяется значением аргумента `is_main` равным `True`, в методе `App().include_router()`, который по умолчанию равен
`False`, если в приложении зарегистрирован лишь один роутер, то он неявно устанавливается главным, если
зарегистрировано больше одного роутера, то требуется явное указание главного. При регистрации более одного
главного роутера вызывается исключение `OnlyOneMainRouterIsAllowedException`. При регистрации более одного
роутера и отсутствии указания главного вызывается исключение `MissingMainRouterException`  

- В устанавливаемом паттерне сообщения описания команды необходимы быть два ключевых слова: 
`command` и `description`, каждое из которых должно быть заключено в фигурные скобки, после обработки
паттерна на места этих ключевых слов будут подставлены соответствующие значения команды, при отсутствии
этих двух ключевых слов будет вызвано исключение `InvalidDescriptionMessagePatternException`

- Команды приложения не должны повторяться, при значении атрибута `ignore_command_register` равным `True`
допускается создание обработчиков для разных регистров одинаковых символов в команде, для примера `u` и `U`,
при значении атрибута `ignore_command_register` класса `App` равным `False` тот же пример вызывает исключение 
`RepeatedCommandInDifferentRoutersException`. Исключение вызывается только при наличии пересекающихся команд 
у __<u>разных</u>__ роутеров

- У главного обработчика должен быть зарегистрирован обработчик неизвестных команд:  
```python
router = Router()

@router.unknown_command
def unknown_command(command):
    print(f'Command "{command}" undefined')
```
При отсутствии обработчика неизвестных команд у главного роутера будет вызвано исключение
`MissingHandlerForUnknownCommandsException`. При регистрации обработчика неизвестных команд у
__<u>не</u>__ главного роутера будет вызвано исключение `HandlerForUnknownCommandsOnNonMainRouterException`




#### Исключения

- `InvalidRouterInstanceException` — Переданный объект в метод `App().include_router()` не является экземпляром класса `Router`.
- `InvalidDescriptionMessagePatternException` — Неправильный формат паттерна описания команд.
- `OnlyOneMainRouterIsAllowedException` — Регистрация более одного главного роутера.
- `MissingMainRouterException` — Отсутствует главный роутер.
- `MissingHandlerForUnknownCommandsException` — В основном роутере отсутствует обработчик неизвестных команд.
- `HandlerForUnknownCommandsOnNonMainRouterException` — Обработчик неизвестных команд определён не у основного роутера.
- `NoRegisteredRoutersException` — Отсутствуют зарегистрированные роутеры.
- `NoRegisteredHandlersException` — У роутера нет ни одного обработчика команд.
- `RepeatedCommandInDifferentRoutersException` — Одна и та же команда зарегистрирована в разных роутерах.

---

###  *class* :: `Router` 
Класс, который определяет и конфигурирует обработчики команд

#### Конструктор
```python
Router(title: str = 'Commands group title:',
       name: str = 'subordinate')
```

**Аргументы:**
- **name : mean**
- `title` (`str`): Заголовок группы команд.
- `name` (`str`): Персональное название роутера



#### **declared *methods***     

---

**`@`Router().**`command(command: str, description: str = None)`  

*param* `command: str` **::** строковый триггер, который будет выполнять указанные действия  
*example* **::** `U` / `update` / `ExaMPLE` 

*param* `description: str` **::** описание команды, которое будет выведено в консоль 
*example* **::** `description for update command` или `example description` 

*method mean* **::** декоратор регистрирует функцию как обработчик команды

---

**`@`Router().**`unknown_command`   

*method mean* **::** декоратор регистрирует функцию как обработчик неизвестных команд

---

**`@`Router().**`command(command: str, description: str = None)`  

*param* `command: str` **::** строковый триггер, который будет выполнять указанные действия  
*example* **::** `U` / `update` / `ExaMPLE` 

*param* `description: str` **::** описание команды, которое будет выведено в консоль 
*example* **::** `description for update command` или `example description` 

*method mean* **::** декоратор регистрирует функцию как обработчик команды

---

**Router().**`get_name() -> str`  

*method mean* **::** возвращает установленное название роутера

---

**Router().**`get_title() -> str`  

*method mean* **::** возвращает установленный заголовок группы команд данного роутера

---

**Router().**`get_router_info() -> dict`  

*method mean* **::** возвращает информацию о роутере

---

**Router().**`get_all_commands() -> list[str]`  

*method mean* **::** возвращает все зарегистрированные команды для данного роутера

---

#### Исключения 
- `InvalidCommandInstanceException` - Переданный объект для регистрации команды не является строкой
- `InvalidDescriptionInstanceException` - Переданный объект для регистрации описания команды не является строкой
- `UnknownCommandHandlerHasAlreadyBeenCreatedException` - Обработчик неизвестных команд уже создан
- `RepeatedCommandException` - Одна и та же команда зарегистрирована в одном роутере
