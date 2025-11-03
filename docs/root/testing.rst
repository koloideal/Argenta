Тестирование
============

В этом разделе описаны рекомендации и лучшие практики по тестированию приложений, построенных с использованием Argenta.

Модульное тестирование
----------------------

Для модульного тестирования команд рекомендуется использовать стандартный модуль ``unittest`` или любой другой предпочитаемый фреймворк (например, ``pytest``).

Пример теста для простой команды:

.. code-block:: python

    import unittest
    from unittest.mock import MagicMock
    from your_app import app, your_command_handler

    class TestYourCommand(unittest.TestCase):
        def test_your_command_handler(self):
            # Подготовка тестовых данных
            mock_scope = MagicMock()
            test_args = {"arg1": "test_value"}
            
            # Вызов обработчика
            result = your_command_handler(scope=mock_scope, **test_args)
            
            # Проверка результата
            self.assertEqual(result, "expected_result")
            mock_scope.some_dependency.assert_called_once_with("test_value")


Тестирование с зависимостями
----------------------------

При использовании внедрения зависимостей через Dishka, вы можете использовать моки для тестирования:

.. code-block:: python

    from dishka import make_async_container
    from dishka.integrations.base import wrap_injection
    from unittest.mock import AsyncMock

    class TestWithDependencies(unittest.IsolatedAsyncioTestCase):
        async def test_handler_with_dependencies(self):
            # Создаем мок-контейнер
            mock_dependency = AsyncMock()
            mock_dependency.some_method.return_value = "mocked_result"
            
            # Настраиваем контейнер
            container = MagicMock()
            container.get.return_value = mock_dependency
            
            # Оборачиваем обработчик для тестирования
            handler = wrap_injection(
                your_handler,
                container=container,
            )
            
            # Вызываем обработчик
            result = await handler(arg1="test")
            
            # Проверяем результаты
            self.assertEqual(result, "expected_result")
            mock_dependency.some_method.assert_called_once()


Интеграционное тестирование
---------------------------

Для тестирования всего приложения целиком можно использовать клиент тестирования:

.. code-block:: python

    from argenta import Application
    from io import StringIO
    import unittest

    class TestAppIntegration(unittest.TestCase):
        def setUp(self):
            self.app = Application()
            self.app.setup()  # Инициализация приложения
            self.output = StringIO()
            self.app.stdout = self.output

        def test_help_command(self):
            self.app.process_input("help")
            output = self.output.getvalue()
            self.assertIn("Доступные команды:", output)


Советы по тестированию
----------------------

1. **Изолируйте тесты**: Каждый тест должен быть независимым от других.
2. **Используйте моки**: Заменяйте внешние зависимости моками для изоляции тестируемого кода.
3. **Проверяйте граничные случаи**: Уделяйте внимание краевым случаям и ошибочным сценариям.
4. **Тестируйте обработку ошибок**: Убедитесь, что ваше приложение корректно обрабатывает ошибки.
5. **Измеряйте покрытие**: Используйте инструменты вроде ``coverage.py`` для анализа покрытия кода тестами.

Пример настройки ``pytest`` с покрытием кода:

.. code-block:: ini

    # setup.cfg
    [tool:pytest]
    testpaths = tests
    python_files = test_*.py
    addopts = -v --cov=your_package --cov-report=term-missing

Для запуска тестов с покрытием:

.. code-block:: bash

    pip install pytest-cov
    pytest
