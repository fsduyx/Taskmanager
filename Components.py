""" =========================================================
    Компоненты UI. Наследники tk-виджетов с единым стилем.
    Interface использует ТОЛЬКО эти классы.
    =========================================================
"""
import tkinter as tk

COLOR_BG = "#1e1f26"
COLOR_PANEL = "#2a2c36"
COLOR_TEXT = "#e8e8ee"
COLOR_ACCENT = "#2d6cdf"
COLOR_WARN = "#8a6d1f"
COLOR_DANGER = "#d9534f"
COLOR_GRAY = "#555a6b"
COLOR_OK = "#4caf72"

FONT = ("Segoe UI", 10)


class AppLabel(tk.Label):
    def __init__(self, master, text: str = "", **kwargs) -> None:
        options = {"bg": COLOR_BG, "fg": COLOR_TEXT, "font": FONT, "anchor": "w"}
        options.update(kwargs)
        super().__init__(master, text=text, **options)


class AppEntry(tk.Entry):
    def __init__(self, master, **kwargs) -> None:
        options = {
            "bg": COLOR_PANEL, "fg": COLOR_TEXT, "insertbackground": "white",
            "relief": "flat", "highlightthickness": 1,
            "highlightbackground": COLOR_PANEL, "highlightcolor": COLOR_ACCENT,
            "font": ("Segoe UI", 11),
        }
        options.update(kwargs)
        super().__init__(master, **options)


class AppButton(tk.Button):
    def __init__(self, master, text: str, command, **kwargs) -> None:
        color = kwargs.pop("color", COLOR_ACCENT)
        options = {
            "bg": color, "fg": "white", "activebackground": color,
            "activeforeground": "white", "relief": "flat", "padx": 10, "pady": 6,
            "cursor": "hand2", "font": ("Segoe UI", 10, "bold"),
        }
        options.update(kwargs)
        super().__init__(master, text=text, command=command, **options)


class AppListbox(tk.Listbox):
    def __init__(self, master, **kwargs) -> None:
        options = {
            "bg": COLOR_PANEL, "fg": COLOR_TEXT, "selectbackground": COLOR_ACCENT,
            "selectforeground": "white", "activestyle": "none",
            "highlightthickness": 0, "relief": "flat", "exportselection": False,
            "font": ("Segoe UI", 11),
        }
        options.update(kwargs)
        super().__init__(master, **options)


class AppFrame(tk.Frame):
    def __init__(self, master, **kwargs) -> None:
        options = {"bg": COLOR_BG}
        options.update(kwargs)
        super().__init__(master, **options)
