.. _root_api_orchestrator_argparser:

Argparser
==========

Объект ``ArgParser`` в ``Argenta`` предназначен для разбора и обработки **аргументов командной строки**, которые передаются вашему приложению при его запуске. Важно не путать их с командами, которые пользователь вводит в интерактивном режиме работы приложения. `ArgParser` позволяет вашему приложению получать внешнюю конфигурацию в момент старта, например, путь к файлу настроек, флаги для отладки или режим запуска.

-----

Инициализация
-------------

.. code-block:: python

   def __init__(self, processed_args: list[argenta.orchestrator.InputArgument] = []) -> None

Создает экземпляр парсера аргументов командной строки.

* ``processed_args``: Список аргументов, которые будут обрабатываться и парситься при запуске приложения.

Основные методы
---------------

.. py:method:: parse(self) -> dict[str, str | list[str]]

   Основной метод, который выполняет разбор списка `processed_args`. Он анализирует аргументы и преобразует их в структурированный словарь.

   *   Аргументы, имеющие вид флага (например, `--verbose`), получают значение `True`.
   *   Аргументы, за которыми следует значение (например, `--config settings.yaml`), сохраняются как пара "ключ-значение".
   *   Если один и тот же аргумент встречается несколько раз, его значения могут быть собраны в список.

   :returns: Словарь, где ключи — это имена аргументов, а значения — их соответствующие значения.

.. py:method:: get(self, key: str, default: str | None = None) -> str | None

   Удобный метод для получения значения конкретного аргумента по его имени (ключу). Если аргумент не был найден, возвращается значение `default`.

   :param key: Имя аргумента (например, `"--config"`).
   :param default: Значение, которое будет возвращено, если аргумент `key` отсутствует. По умолчанию `None`.
   :returns: Значение аргумента или значение по умолчанию.

.. py:method:: all_args(self) -> list[str]

   Возвращает список всех имен (ключей) аргументов, которые были распознаны парсером после вызова метода `parse()`.

Назначение и интеграция
------------------------

`ArgParser` является неотъемлемой частью `Orchestrator`. При создании `Orchestrator` ему передается экземпляр `ArgParser`, который обычно инициализируется с `sys.argv[1:]`.

После этого `Orchestrator` помещает `ArgParser` в DI-контейнер. Это означает, что любой ваш сервис или обработчик команды может запросить `ArgParser` через внедрение зависимостей и получить доступ к стартовым аргументам приложения. Это предпочтительный способ для конфигурации компонентов на основе параметров запуска.

Пример использования
--------------------

.. code-block:: python

    import sys
    from argenta.orchestrator import Orchestrator
    from argenta.orchestrator.argparser import ArgParser
    from argenta.app import App
    from dishka import Provider, Scope, provide

    # 1. Создаем парсер на основе реальных аргументов командной строки
    # Например, если запустить: python main.py --config prod.json --debug
    arg_parser = ArgParser(processed_args=sys.argv[1:])

    # 2. Определяем сервис, который будет использовать эти аргументы
    class Settings:
        def __init__(self, config_path: str, is_debug: bool):
            self.config_path = config_path
            self.is_debug = is_debug

    class SettingsProvider(Provider):
        @provide(scope=Scope.APP)
        def get_settings(self, parser: ArgParser) -> Settings:
            # Запрашиваем ArgParser из DI и используем его для конфигурации
            path = parser.get('--config', default='default.json')
            debug_mode = bool(parser.get('--debug'))
            return Settings(config_path=path, is_debug=debug_mode)

    # 3. Создаем Orchestrator, передавая ему парсер и провайдер
    app = App()
    orchestrator = Orchestrator(
        arg_parser=arg_parser,
        custom_providers=[SettingsProvider()]
    )

    # 4. Запускаем приложение
    if __name__ == "__main__":
        orchestrator.start_polling(app)


