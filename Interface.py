""" =========================================================
    Interface — прослойка между логикой и tkinter.
    Не знает про задачи. Только создаёт и обновляет виджеты.
    =========================================================
"""
import tkinter as tk
from tkinter import messagebox

from Components import (AppLabel, AppEntry, AppButton, AppFrame, AppScrollFrame,
                        COLOR_BG, COLOR_PANEL, COLOR_ROW, COLOR_BORDER, COLOR_TEXT,
                        COLOR_MUTED, COLOR_ACCENT, COLOR_OK)


class Interface:
    """Фасад над tkinter: единый API для TaskManager."""

    def __init__(self, title: str = "Task Manager", width: int = 560, height: int = 640,
                 root: tk.Tk | None = None) -> None:
        """Создать корневое окно, настроить размеры и стиль."""
        self.root = root if root is not None else tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(480, 520)
        self.root.configure(bg=COLOR_BG)
        self._callbacks = {}
        self._rows = []
        self._row_frames = []
        self._selected = None

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

        AppLabel(self.root, text="Task Manager v0.2.0",
                 font=("Segoe UI", 15, "bold")).pack(fill="x", padx=18, pady=(16, 2))
        AppLabel(self.root, text="Превращаем приложение в чистый модульный проект",
                 fg=COLOR_MUTED).pack(fill="x", padx=18, pady=(0, 10))

        form = AppFrame(self.root, bg=COLOR_PANEL, highlightthickness=1,
                        highlightbackground=COLOR_BORDER)
        form.pack(fill="x", padx=18, pady=(0, 10))
        self.entry_title = self._add_field(form, "Название")
        self.entry_description = self._add_field(form, "Описание")
        self.entry_author = self._add_field(form, "Автор")

        self.scroll = AppScrollFrame(self.root, bg=COLOR_PANEL, highlightthickness=1,
                                     highlightbackground=COLOR_BORDER)
        self.scroll.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        AppFrame(self.root, bg=COLOR_BORDER, height=1).pack(fill="x", padx=18)
        self.label_status = AppLabel(self.root, text="", height=2)
        self.label_status.pack(fill="x", padx=18)

        buttons = AppFrame(self.root)
        buttons.pack(fill="x", padx=18, pady=(0, 16))
        for column in range(3):
            buttons.columnconfigure(column, weight=1, uniform="buttons")
        AppButton(buttons, "+ Новая", self._handler("create"), kind="primary").grid(
            row=0, column=0, sticky="ew", padx=(0, 6))
        AppButton(buttons, "Сохранить", self._handler("edit")).grid(
            row=0, column=1, sticky="ew", padx=3)
        AppButton(buttons, "Выход", self.quit).grid(
            row=0, column=2, sticky="ew", padx=(6, 0))

    def _add_field(self, parent, caption: str) -> AppEntry:
        row = AppFrame(parent, bg=COLOR_PANEL)
        row.pack(fill="x", padx=12, pady=4)
        AppLabel(row, text=caption, width=9, bg=COLOR_PANEL, fg=COLOR_MUTED).pack(side="left")
        entry = AppEntry(row)
        entry.pack(side="left", fill="x", expand=True, ipady=4)
        return entry

    def _add_row(self, index: int, row: dict) -> None:
        done = bool(row.get("status"))
        frame = AppFrame(self.scroll.body, bg=COLOR_ROW, highlightthickness=1,
                         highlightbackground=COLOR_BORDER)
        frame.pack(fill="x", padx=10, pady=4)

        if done:
            check = AppLabel(frame, text="✓", width=2, anchor="center", bg=COLOR_OK,
                             fg=COLOR_BG, font=("Segoe UI", 10, "bold"))
        else:
            check = AppLabel(frame, text="", width=2, bg=COLOR_ROW, highlightthickness=1,
                             highlightbackground=COLOR_MUTED)
        check.pack(side="left", padx=(10, 8), pady=10)
        check.config(cursor="hand2")
        check.bind("<Button-1>", lambda event, i=index: self._on_check(i))

        font = ("Segoe UI", 11, "overstrike") if done else ("Segoe UI", 11)
        title = AppLabel(frame, text=row["title"], bg=COLOR_ROW, font=font,
                         fg=COLOR_MUTED if done else COLOR_TEXT, cursor="hand2")
        title.pack(side="left", fill="x", expand=True)
        title.bind("<Button-1>", lambda event, i=index: self._select(i, fill=True))

        AppButton(frame, "✕", lambda i=index: self._on_delete(i), kind="danger",
                  width=2, padx=4, pady=2).pack(side="right", padx=(4, 10), pady=8)
        AppButton(frame, "✎", lambda i=index: self._select(i, fill=True),
                  width=2, padx=4, pady=2).pack(side="right", pady=8)

        self._row_frames.append(frame)

    def _select(self, index: int, fill: bool = False) -> None:
        """Выделить строку и (если нужно) показать её данные в полях ввода."""
        self._selected = index
        self._highlight()
        if fill:
            row = self._rows[index]
            self.clear_input()
            self.entry_title.insert(0, row["title"])
            self.entry_description.insert(0, row.get("description", ""))
            self.entry_author.insert(0, row.get("author", ""))

    def _highlight(self) -> None:
        for number, frame in enumerate(self._row_frames):
            color = COLOR_ACCENT if number == self._selected else COLOR_BORDER
            frame.config(highlightbackground=color)

    def _on_check(self, index: int) -> None:
        self._select(index)
        self._handler("toggle")()

    def _on_delete(self, index: int) -> None:
        self._select(index)
        self._handler("delete")()

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
        for widget in self.scroll.body.winfo_children():
            widget.destroy()
        self._row_frames = []
        self._selected = select if select is not None and 0 <= select < len(self._rows) else None

        if not self._rows:
            AppLabel(self.scroll.body, text="Список задач пуст", bg=COLOR_PANEL,
                     fg=COLOR_MUTED, anchor="center").pack(fill="x", pady=30)
        for index, row in enumerate(self._rows):
            self._add_row(index, row)
        self._highlight()

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
        return self._selected
