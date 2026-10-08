"""Точка входа в программу."""
import tkinter as tk
from src.app import App

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()