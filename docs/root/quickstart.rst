.. _root_quickstart:

Быстрый старт
********************

1. **Установка** ``Argenta``

.. code-block:: shell

    pip install argenta

2. **Определение роутера и хэндлеров**. За регистрацию функции как обработчика отвечает декоратор ``@router.command``, хэндлер всегда должен принимать аргумент с типом ``Response``, подробнее в :ref:`разделе <Response>`.

.. literalinclude:: ../code_snippets/quickstart_example_routers.py
   :language: python

3. **Определение приложения и оркестратора**. Для запуска приложения необходимо вызвать ``.include_router()`` у созданного приложения и передать ему раннее созданный роутер, после этого необходимо вызвать ``.start_polling()`` у созданного оркестратора и передать ему созданное приложение.

.. literalinclude:: ../code_snippets/quickstart_example_main.py
   :language: python

4. **Запуск приложения**. Запускаем приложение как обычный скрипт.


.. image:: https://github.com/koloideal/Argenta/blob/docs/create_docs/imgs/mock_app_preview6.png?raw=true
   :alt: Quickstart Example
