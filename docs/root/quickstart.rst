.. _root_quickstart:

Быстрый старт
********************

В этом руководстве мы создадим простое, но полнофункциональное CLI-приложение «Менеджер задач», которое продемонстрирует ключевые возможности Argenta.

1. **Установка**

.. code-block:: shell

    pip install argenta

2. **Определение моделей данных и репозитория**

Сначала определим модели данных для задачи и репозиторий для их хранения. Это будет наша "бизнес-логика".

.. literalinclude:: ../code_snippets/quickstart/task_manager/repository.py
   :language: python
   :linenos:

3. **Создание провайдера для DI**

Чтобы Argenta могла внедрять `TaskRepository` в наши обработчики, мы создадим провайдер для `dishka`.

.. literalinclude:: ../code_snippets/quickstart/task_manager/provider.py
   :language: python
   :linenos:

4. **Создание обработчиков команд**

Теперь создадим обработчики для команд `add-task` и `list-tasks`. Обратите внимание, как мы используем флаги и внедряем `TaskRepository`.

.. literalinclude:: ../code_snippets/quickstart/task_manager/handlers.py
   :language: python
   :linenos:

5. **Сборка и запуск приложения**

Наконец, соберем все вместе: создадим экземпляр `App`, подключим роутер и провайдер, а затем запустим приложение.

.. literalinclude:: ../code_snippets/quickstart/task_manager/main.py
   :language: python
   :linenos:

6. **Результат**

Теперь вы можете запустить `main.py` и взаимодействовать с вашим новым CLI-приложением.

.. image:: https://github.com/koloideal/Argenta/blob/main/imgs/mock_app_preview4.png?raw=True
   :alt: Task Manager Example
