""" =========================================================
    TaskManager — главный фасад.
    Связывает Task, StorageManager и Interface.
    =========================================================
"""
from typing import TYPE_CHECKING

from Task import Task
from StorageManager import StorageManager

if TYPE_CHECKING:
    import tkinter as tk


class TaskManager:
    """Оркестратор приложения. Единственная точка входа для UI."""

    def __init__(self, root: "tk.Tk", storage=None, interface=None) -> None:
        """Создать StorageManager и Interface, привязать колбэки."""
        self.root = root
        self.storage = storage or StorageManager()
        if interface is None:
            from Interface import Interface
            interface = Interface(root=root)
        self.interface = interface
        self.tasks: list[Task] = []

        self.interface.set_callbacks(
            on_create=self.create_task,
            on_edit=self.edit_task,
            on_delete=self.delete_task,
            on_toggle=self.toggle_status,
        )
        self.interface.build()
        self.refresh()

    def _selected(self) -> tuple[int | None, Task | None]:
        """Индекс и задача, выбранные в списке."""
        index = self.interface.get_selected_index()
        if index is None or index >= len(self.tasks):
            self.interface.show_warning("Нет выбора", "Выберите задачу в списке!")
            return None, None
        return index, self.tasks[index]

    # ---------- CRUD ----------
    def create_task(self) -> None:
        """Прочитать ввод → создать Task → сохранить → обновить список."""
        data = self.interface.get_input()
        if not data["title"]:
            self.interface.show_warning("Ошибка ввода", "Название задачи не может быть пустым!")
            return
        task = Task(title=data["title"], description=data["description"],
                    author=data["author"] or "—")
        self.storage.add(task)
        self.interface.clear_input()
        self.refresh()
        self.interface.show_message("Готово", f"задача «{task.title}» добавлена")

    def edit_task(self) -> None:
        """Взять выбранную задачу → изменить → сохранить → обновить."""
        index, task = self._selected()
        if task is None:
            return
        data = self.interface.get_input()
        if not data["title"]:
            self.interface.show_warning("Ошибка ввода", "Название задачи не может быть пустым!")
            return
        task.title = data["title"]
        task.description = data["description"]
        task.author = data["author"] or "—"
        self.storage.update(task.id, task)
        self.refresh(select=index)
        self.interface.show_message("Готово", f"задача «{task.title}» сохранена")

    def delete_task(self) -> None:
        """Удалить выбранную задачу (с подтверждением)."""
        index, task = self._selected()
        if task is None:
            return
        if not self.interface.ask_confirm("Удаление", f"Удалить задачу «{task.title}»?"):
            return
        self.storage.delete(task.id)
        self.interface.clear_input()
        self.refresh()
        self.interface.show_message("Готово", f"задача «{task.title}» удалена")

    def toggle_status(self) -> None:
        """Переключить статус выбранной задачи."""
        index, task = self._selected()
        if task is None:
            return
        task.status = not task.status
        self.storage.update(task.id, task)
        self.refresh(select=index)
        self.interface.show_message("Готово", "статус изменён")

    toggle_done = toggle_status

    # ---------- служебное ----------
    def refresh(self, select: int | None = None) -> None:
        """Перечитать задачи из StorageManager и отрисовать."""
        self.tasks = self.storage.load()
        self.interface.show_tasks(self.tasks, select)

    def run(self) -> None:
        """Передать управление Interface."""
        self.interface.run()
