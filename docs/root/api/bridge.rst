.. _root_api_bridge:

DataBridge
==========

``DataBridge`` — это сущность, предоставляющая временное хранилище данных, которое существует в рамках одной сессии приложения (от запуска до выхода). Она предназначена для обмена данными между обработчиками.

Основной способ получения доступа к ``DataBridge`` — через ``di``.

.. code-block:: python
   :linenos:

   from argenta.di import FromDishka
   from argenta import DataBridge, Response
   
   # ... setting up router and other

   def my_handler(response: Response, data_bridge: FromDishka[DataBridge]):
       # ... your code

**Практический пример: Аутентификация**

Рассмотрим пример, где команда `login` сохраняет токен аутентификации, а команда `get-profile` использует его.

.. literalinclude:: ../../code_snippets/response/data_sharing.py
   :language: python
   :linenos:

**Как это работает:**

1.  При вызове обработчика ``dishka`` автоматически внедряет экземпляр ``DataBridge``.
2.  Команда ``login --username <имя>`` вызывает ``login_handler``, который через внедрённый ``data_bridge`` сохраняет токен.
3.  Команда ``get-profile`` вызывает ``get_profile_handler``, который так же получает ``data_bridge`` и извлекает из него токен.

-----------

.. py:class:: DataBridge

   .. py:method:: __init__(self, initial_data: dict | None = None)
      :no-index:

      Инициализирует хранилище. При использовании через ``di`` вызывается автоматически.

   .. py:method:: update(self, data: dict) -> None

      Обновляет хранилище данными из словаря.

   .. py:method:: get_all(self) -> dict

      Возвращает все данные из хранилища.

   .. py:method:: get_by_key(self, key: str) -> Any

      Возвращает значение по ключу или ``None``, если ключ не найден.

   .. py:method:: delete_by_key(self, key: str) -> None

      Удаляет значение по ключу. Вызывает ``KeyError``, если ключ не найден.

   .. py:method:: clear_all(self) -> None

      Полностью очищает хранилище.
