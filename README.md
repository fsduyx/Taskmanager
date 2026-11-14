# Task Manager v0.2.0

Менеджер задач на Python + tkinter: создание, изменение, удаление задач и отметка «выполнено».
Данные хранятся в `tasks.json` и сохраняются между запусками.

## Запуск

    python main.py

Тесты (окно не нужно):

    python -m unittest

## Архитектура

    main.py -> TaskManager (фасад)
                 |-- Interface (прослойка к tkinter)
                 |      '-- Components: AppLabel, AppEntry, AppButton, AppListbox, AppFrame
                 '-- StorageManager (JSON)
                        '-- Task

| Класс | Файл | Ответственность |
|---|---|---|
| `Task` | `Task.py` | шаблон задачи: `id`, `title`, `description`, `status`, `author`, `created_at`; `to_dict()` / `from_dict()` |
| `StorageManager` | `StorageManager.py` | сохранение в JSON: `load`, `save`, `add`, `update`, `delete` |
| `AppLabel`, `AppEntry`, `AppButton`, `AppListbox`, `AppFrame`, `AppScrollFrame` | `Components.py` | наследники tk-виджетов с единым стилем |
| `Interface` | `Interface.py` | прослойка к tkinter: `build`, `get_input`, `clear_input`, `show_tasks`, `show_message`, `show_warning`, `ask_confirm`, `get_selected_index` |
| `TaskManager` | `TaskManager.py` | фасад: `create_task`, `edit_task`, `delete_task`, `toggle_status`, `refresh`, `run` |

## Как это работает

1. `main.py` создаёт окно `root` и передаёт его в `TaskManager`.
2. `TaskManager.__init__` создаёт `StorageManager` и `Interface`, передаёт `Interface` свои методы как обработчики кнопок (`set_callbacks`), вызывает `build()` и `refresh()`.
3. Нажатие кнопки вызывает метод `TaskManager`. Он читает ввод через `get_input()`, меняет данные через `StorageManager` и вызывает `refresh()`.
4. `refresh()` перечитывает файл и передаёт список задач в `Interface.show_tasks()`.
5. Кнопка ✎ (или клик по названию) заполняет поля ввода, после чего задачу можно править и сохранять. Квадрат слева переключает статус, ✕ удаляет.

`Interface` ничего не знает про файл и логику, `StorageManager` ничего не знает про окно. Поэтому JSON можно заменить на базу данных, а tkinter на другую библиотеку, не трогая остальные классы.

## Проверка

1. Добавьте задачу кнопкой «+ Новая».
2. Нажмите ✎ у задачи, измените текст в полях, нажмите «Сохранить».
3. Нажмите на квадрат слева от задачи: он станет зелёным, а название зачеркнётся.
4. Нажмите ✕ справа от задачи и подтвердите удаление.
5. Закройте окно и запустите снова: задачи остались.
