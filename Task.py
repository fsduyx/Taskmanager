""" =========================================================
    Task — шаблон задачи.
    =========================================================
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class Task:
    """Модель одной задачи."""
    title: str
    description: str = ""
    status: bool = False
    author: str = "—"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    id: int | None = None

    def to_dict(self) -> dict:
        """Сериализовать задачу в dict для StorageManager."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Восстановить Task из dict."""
        known = {"title", "description", "status", "author", "created_at", "id"}
        kwargs = {key: value for key, value in data.items() if key in known}
        kwargs.setdefault("title", "")
        kwargs["status"] = bool(kwargs.get("status", False))
        return cls(**kwargs)
