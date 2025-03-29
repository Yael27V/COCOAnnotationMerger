import tkinter as tk
from tkinter import ttk

class TaskSelector(tk.Frame):
    def __init__(self, master, switch_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.switch_callback = switch_callback
        self.configure(bg='#e6f0fa')  # Light blue background

        # Title label
        tk.Label(
            self,
            text="Select Annotation Merge Mode",
            font=("Helvetica", 16, "bold"),
            bg='#e6f0fa',
            fg='#003366'
        ).pack(pady=20)

        # Option buttons
        btn_style = {
            "font": ("Helvetica", 12),
            "width": 60,
            "bg": "#007acc",
            "fg": "white",
            "activebackground": "#005f99",
            "bd": 0,
            "relief": "flat",
            "pady": 10
        }

        tk.Button(
            self,
            text="1. Merge Multiple COCO Files with Same Categories",
            command=lambda: self.switch_callback("single"),
            **btn_style
        ).pack(pady=10)

        tk.Button(
            self,
            text="2. Merge Two COCO Files with Different Categories",
            command=lambda: self.switch_callback("dual"),
            **btn_style
        ).pack(pady=10)

        tk.Button(
            self,
            text="3. Merge All Annotations from Two Folders (Strawberries + Flowers)",
            command=lambda: self.switch_callback("multi"),
            **btn_style
        ).pack(pady=10)
