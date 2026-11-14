""" =========================================================
    StorageManager — сохранение и загрузка задач.
    Сейчас JSON, в будущем — замена на БД без смены API.
    =========================================================
"""
import json
import os

from Task import Task


class StorageManager:
    """Управляет персистентностью коллекции задач."""

    def __init__(self, path: str = "tasks.json") -> None:
        """Запомнить путь к файлу, при необходимости — создать."""
        if not os.path.isabs(path):
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
        self.path = path
        if not os.path.exists(self.path):
            self.save([])

    def load(self) -> list[Task]:
        """Прочитать все задачи из хранилища."""
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []

        tasks = [Task.from_dict(item) for item in data if isinstance(item, dict)]
        next_id = max((t.id for t in tasks if t.id is not None), default=0) + 1
        for task in tasks:
            if task.id is None:
                task.id = next_id
                next_id += 1
        return tasks

    def save(self, tasks: list[Task]) -> None:
        """Записать весь список задач в хранилище."""
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump([t.to_dict() for t in tasks], file, ensure_ascii=False, indent=2)

    def add(self, task: Task) -> None:
        """Добавить одну задачу."""
        tasks = self.load()
        task.id = max((t.id for t in tasks), default=0) + 1
        tasks.append(task)
        self.save(tasks)

    def update(self, task_id: int, task: Task) -> None:
        """Обновить задачу по id."""
        tasks = self.load()
        for number, old in enumerate(tasks):
            if old.id == task_id:
                task.id = task_id
                tasks[number] = task
                break
        self.save(tasks)

    def delete(self, task_id: int) -> None:
        """Удалить задачу по id."""
        self.save([t for t in self.load() if t.id != task_id])
