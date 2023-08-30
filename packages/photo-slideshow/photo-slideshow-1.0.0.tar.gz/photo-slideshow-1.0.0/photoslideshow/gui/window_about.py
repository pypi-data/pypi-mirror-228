import tkinter as tk


class About(tk.Toplevel):
    """
    Window to show photos in fullscreen mode
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grab_set()

        tk.Label(master=self, text="Version: 1.0.0").pack()
        tk.Label(master=self, text="Author: Mateusz Poślednik").pack()
        tk.Label(master=self, text="Project url: www...").pack()
        tk.Label(master=self, text="License: MIT").pack()
        tk.Label(master=self, text="Copyright by: Mateusz Poślednik@2023").pack(padx=4)

        tk.Button(master=self, text="Close", command=lambda: self.destroy()).pack(pady=4)

