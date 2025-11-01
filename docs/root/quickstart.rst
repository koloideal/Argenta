.. _root_quickstart:

Быстрый старт
********************

1. **Установка** ``Argenta``

.. code-block:: shell

    pip install argenta

2. **Создание обработчиков**. Чтобы зарегистрировать функцию как обработчик команды, используйте декоратор ``@router.command``. Обработчик всегда должен принимать первым аргументом объект ``Response`` (подробнее в :ref:`документации <root_api_response>`).

.. literalinclude:: ../code_snippets/quickstart/routers.py
   :language: python
   :linenos:

3. **Настройка и запуск**. Чтобы подключить обработчики, вызовите метод ``.include_router()`` у экземпляра приложения и передайте в него ваш роутер. Затем создайте оркестратор и вызовите его метод ``.start_polling()``, передав ему приложение.

.. literalinclude:: ../code_snippets/quickstart/main.py
   :language: python
   :linenos:

4. **Запуск**. Теперь приложение можно запустить как обычный Python-скрипт.


.. image:: https://github.com/koloideal/Argenta/blob/docs/create_docs/imgs/mock_app_preview6.png?raw=true
   :alt: Quickstart Example
