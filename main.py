"""Точка входа в приложение для визуализации случайного пути."""

import tkinter as tk

from src.app import App


def main() -> None:
    """Создает главное окно Tkinter и запускает цикл приложения."""
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
