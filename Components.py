""" =========================================================
    Компоненты UI. Наследники tk-виджетов с единым стилем.
    Interface использует ТОЛЬКО эти классы.
    =========================================================
"""
import tkinter as tk

COLOR_BG = "#0b0e1a"
COLOR_PANEL = "#121631"
COLOR_ROW = "#171c38"
COLOR_BORDER = "#262d52"
COLOR_TEXT = "#e8eaf6"
COLOR_MUTED = "#7f87ad"
COLOR_ACCENT = "#3b5bdb"
COLOR_ACCENT_BG = "#1b2a5e"
COLOR_ACCENT_TEXT = "#8fb0ff"
COLOR_OK = "#2ecc71"
COLOR_DANGER = "#ff6b6b"
COLOR_DANGER_BG = "#3a1f2e"
COLOR_DANGER_BORDER = "#5a2a3c"

FONT = ("Segoe UI", 10)


class AppLabel(tk.Label):
    def __init__(self, master, text: str = "", **kwargs) -> None:
        options = {"bg": COLOR_BG, "fg": COLOR_TEXT, "font": FONT, "anchor": "w"}
        options.update(kwargs)
        super().__init__(master, text=text, **options)


class AppEntry(tk.Entry):
    def __init__(self, master, **kwargs) -> None:
        options = {
            "bg": COLOR_ROW, "fg": COLOR_TEXT, "insertbackground": COLOR_TEXT,
            "relief": "flat", "highlightthickness": 1,
            "highlightbackground": COLOR_BORDER, "highlightcolor": COLOR_ACCENT,
            "font": ("Segoe UI", 11),
        }
        options.update(kwargs)
        super().__init__(master, **options)


class AppButton(tk.Button):
    STYLES = {
        "default": (COLOR_ROW, COLOR_TEXT, COLOR_BORDER),
        "primary": (COLOR_ACCENT_BG, COLOR_ACCENT_TEXT, COLOR_ACCENT),
        "danger": (COLOR_DANGER_BG, COLOR_DANGER, COLOR_DANGER_BORDER),
    }

    def __init__(self, master, text: str, command, **kwargs) -> None:
        bg, fg, border = self.STYLES[kwargs.pop("kind", "default")]
        options = {
            "bg": bg, "fg": fg, "activebackground": border, "activeforeground": fg,
            "relief": "flat", "bd": 0, "highlightthickness": 1,
            "highlightbackground": border, "padx": 10, "pady": 6,
            "cursor": "hand2", "font": ("Segoe UI", 10, "bold"),
        }
        options.update(kwargs)
        super().__init__(master, text=text, command=command, **options)


class AppListbox(tk.Listbox):
    def __init__(self, master, **kwargs) -> None:
        options = {
            "bg": COLOR_ROW, "fg": COLOR_TEXT, "selectbackground": COLOR_ACCENT,
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


class AppScrollFrame(AppFrame):
    """Прокручиваемая область. Виджеты кладутся в self.body."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        bg = kwargs.get("bg", COLOR_BG)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.body = AppFrame(self.canvas, bg=bg)
        self._window = self.canvas.create_window((0, 0), window=self.body, anchor="nw")
        self.body.bind("<Configure>", self._on_body_resize)
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        for sequence in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.bind_all(sequence, self._on_wheel)

    def _on_body_resize(self, event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_resize(self, event) -> None:
        self.canvas.itemconfig(self._window, width=event.width)

    def _on_wheel(self, event) -> None:
        if self.body.winfo_height() <= self.canvas.winfo_height():
            return
        if event.num == 4:
            step = -1
        elif event.num == 5:
            step = 1
        else:
            step = -1 if event.delta > 0 else 1
        self.canvas.yview_scroll(step, "units")
