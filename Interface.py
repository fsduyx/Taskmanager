""" =========================================================
    Interface — прослойка между логикой и tkinter.
    Не знает про задачи. Только создаёт и обновляет виджеты.
    =========================================================
"""
import tkinter as tk
from tkinter import messagebox

from Components import (AppLabel, AppEntry, AppButton, AppListbox, AppFrame,
                        COLOR_BG, COLOR_OK, COLOR_WARN, COLOR_DANGER, COLOR_GRAY)


class Interface:
    """Фасад над tkinter: единый API для TaskManager."""

    def __init__(self, title: str = "Task Manager", width: int = 520, height: int = 520,
                 root: tk.Tk | None = None) -> None:
        """Создать корневое окно, настроить размеры и стиль."""
        self.root = root if root is not None else tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(480, 460)
        self.root.configure(bg=COLOR_BG)
        self._callbacks = {}
        self._rows = []

    def set_callbacks(self, on_create=None, on_edit=None, on_delete=None, on_toggle=None) -> None:
        """Привязать функции к кнопкам."""
        self._callbacks = {
            "create": on_create, "edit": on_edit,
            "delete": on_delete, "toggle": on_toggle,
        }

    def _handler(self, name):
        def call():
            callback = self._callbacks.get(name)
            if callback:
                callback()
        return call

    # ---------- жизненный цикл ----------
    def run(self) -> None:
        """Запустить главный цикл."""
        self.root.mainloop()

    def quit(self) -> None:
        """Закрыть окно."""
        self.root.destroy()

    def clear(self) -> None:
        """Удалить все дочерние виджеты."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------- построение ----------
    def build(self) -> None:
        """Собрать базовый каркас: заголовок, список, поле ввода, кнопки."""
        self.clear()

        AppLabel(self.root, text="Менеджер задач",
                 font=("Segoe UI", 16, "bold")).pack(fill="x", padx=14, pady=(12, 4))

        form = AppFrame(self.root)
        form.pack(fill="x", padx=14, pady=4)
        self.entry_title = self._add_field(form, "Название")
        self.entry_description = self._add_field(form, "Описание")
        self.entry_author = self._add_field(form, "Автор")

        buttons = AppFrame(self.root)
        buttons.pack(fill="x", padx=14, pady=6)
        AppButton(buttons, "+ Новая", self._handler("create")).pack(side="left", padx=(0, 6))
        AppButton(buttons, "Сохранить", self._handler("edit"), color=COLOR_WARN).pack(side="left", padx=(0, 6))
        AppButton(buttons, "Выполнено", self._handler("toggle")).pack(side="left", padx=(0, 6))
        AppButton(buttons, "Удалить", self._handler("delete"), color=COLOR_DANGER).pack(side="left")

        self.listbox = AppListbox(self.root)
        self.listbox.pack(fill="both", expand=True, padx=14, pady=4)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        bottom = AppFrame(self.root)
        bottom.pack(fill="x", padx=14, pady=(4, 12))
        self.label_status = AppLabel(bottom, text="")
        self.label_status.pack(side="left", fill="x", expand=True)
        AppButton(bottom, "Выход", self.quit, color=COLOR_GRAY).pack(side="right")

    def _add_field(self, parent, caption: str) -> AppEntry:
        row = AppFrame(parent)
        row.pack(fill="x", pady=3)
        AppLabel(row, text=caption, width=10).pack(side="left")
        entry = AppEntry(row)
        entry.pack(side="left", fill="x", expand=True, ipady=4)
        return entry

    def _on_select(self, event=None) -> None:
        """Показать данные выбранной строки в полях ввода."""
        index = self.get_selected_index()
        if index is None or index >= len(self._rows):
            return
        row = self._rows[index]
        self.clear_input()
        self.entry_title.insert(0, row["title"])
        self.entry_description.insert(0, row["description"])
        self.entry_author.insert(0, row["author"])

    # ---------- ввод ----------
    def get_input(self) -> dict:
        """Вернуть {title, description, author} из полей ввода."""
        return {
            "title": self.entry_title.get().strip(),
            "description": self.entry_description.get().strip(),
            "author": self.entry_author.get().strip(),
        }

    def clear_input(self) -> None:
        """Очистить поля ввода."""
        for entry in (self.entry_title, self.entry_description, self.entry_author):
            entry.delete(0, tk.END)

    # ---------- отображение ----------
    def show_tasks(self, tasks: list, select: int | None = None) -> None:
        """Заполнить список задач (list[Task] или list[dict])."""
        self._rows = [t if isinstance(t, dict) else t.to_dict() for t in tasks]
        self.listbox.delete(0, tk.END)
        for row in self._rows:
            mark = "[x]" if row.get("status") else "[   ]"
            self.listbox.insert(tk.END, f"{mark}  {row['title']}   ({row.get('author', '—')})")
        if select is not None and 0 <= select < len(self._rows):
            self.listbox.selection_set(select)

    def show_message(self, title: str, text: str) -> None:
        """Показать информационное сообщение."""
        self.label_status.config(text=f"{title}: {text}", fg=COLOR_OK)

    def show_warning(self, title: str, text: str) -> None:
        """Показать предупреждение."""
        messagebox.showwarning(title, text)

    def ask_confirm(self, title: str, text: str) -> bool:
        """Спросить подтверждение. True — да, False — нет."""
        return messagebox.askyesno(title, text)

    def get_selected_index(self) -> int | None:
        """Индекс выбранной строки в списке или None."""
        selection = self.listbox.curselection()
        return selection[0] if selection else None
