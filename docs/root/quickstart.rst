.. _root_quickstart:

Быстрый старт
=============

В этом руководстве мы рассмотрим два примера создания CLI-приложения с помощью Argenta:

*   **Простой пример**: минимальное приложение для быстрого знакомства с основными компонентами.
*   **Более сложный пример**: полнофункциональное приложение «Менеджер задач» с внедрением зависимостей и бизнес-логикой.

Простой пример
---------------

**Установка**

.. code-block:: shell

    pip install argenta

Этот пример демонстрирует абсолютный минимум, необходимый для создания и запуска приложения. Вы можете скопировать этот код, запустить его и сразу увидеть результат.

.. literalinclude:: ../code_snippets/quickstart/simple_app.py
   :language: python
   :linenos:

**Результат**

.. image:: https://i.ibb.co/35q24Bh8/image.png
   :alt: Simple App Example
   
-----

Более сложный пример: Менеджер задач
--------------------------------------

В этом руководстве мы создадим простое, но полнофункциональное CLI-приложение «Менеджер задач», которое продемонстрирует ключевые возможности Argenta.

1. **Установка**

.. code-block:: shell

    pip install argenta

2. **Определение моделей данных и репозитория**

Сначала определим модели данных для задачи и репозиторий для их хранения.

.. literalinclude:: ../code_snippets/quickstart/task_manager/repository.py
   :language: python
   :linenos:

3. **Создание провайдера для DI**

Чтобы Argenta могла внедрять ``TaskRepository`` в наши обработчики, мы создадим провайдер для ``dishka``.

.. literalinclude:: ../code_snippets/quickstart/task_manager/provider.py
   :language: python
   :linenos:

4. **Создание обработчиков команд**

Теперь создадим обработчики для команд ``add-task`` и ``list-tasks``. Обратите внимание, как мы используем флаги и внедряем ``TaskRepository``.

.. literalinclude:: ../code_snippets/quickstart/task_manager/handlers.py
   :language: python
   :linenos:

5. **Сборка и запуск приложения**

Наконец, соберем все вместе: создадим экземпляр ``App``, подключим роутер и провайдер, а затем запустим приложение.

.. literalinclude:: ../code_snippets/quickstart/task_manager/main.py
   :language: python
   :linenos:

6. **Результат**

Теперь вы можете запустить ``main.py`` и взаимодействовать с вашим новым CLI-приложением.

.. image:: https://i.ibb.co/bgsCLZhP/image.png
   :alt: Task Manager Example
