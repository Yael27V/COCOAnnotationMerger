"""
TaskSelector - GUI Menu for Selecting COCO Annotation Merge or Conversion Task

Author: Yael Vicente  
Date: March 28, 2025  
Version: 1.0  
Last Updated: April 4, 2025

Description:
    This class implements the main task selection menu for the COCO Annotation Merger GUI.
    It provides an intuitive interface to choose between different types of annotation
    processing modes:

    - Merge multiple annotation files with shared categories.
    - Merge two annotation files with different categories (e.g., strawberries and flowers).
    - Merge all annotations from two directories.
    - Convert segmentation annotations into bounding boxes only.

    The selection triggers the corresponding UI module through a callback system.
"""

import tkinter as tk
from tkinter import ttk


class TaskSelector(tk.Frame):
    """
    Main menu interface to select one of the available annotation processing tasks.

    Attributes:
        switch_callback (function): A callback function to handle UI switching based on selected task.
    """

    def __init__(self, master, switch_callback, *args, **kwargs):
        """
        Initializes the task selection interface.

        Args:
            master (tk.Tk or tk.Frame): Parent Tkinter container.
            switch_callback (function): Function to call with task identifier ('single', 'dual', etc.).
            *args, **kwargs: Additional arguments for the Frame.
        """
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

        # Shared button style configuration
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

        # Option 1: Merge multiple JSONs with same categories
        tk.Button(
            self,
            text="1. Merge Multiple COCO Files with Same Categories",
            command=lambda: self.switch_callback("single"),
            **btn_style
        ).pack(pady=10)

        # Option 2: Merge two JSONs with different categories (Strawberries + Flowers)
        tk.Button(
            self,
            text="2. Merge Two COCO Files with Different Categories",
            command=lambda: self.switch_callback("dual"),
            **btn_style
        ).pack(pady=10)

        # Option 3: Merge two folders of annotations (Strawberries + Flowers)
        tk.Button(
            self,
            text="3. Merge All Annotations from Two Folders (Strawberries + Flowers)",
            command=lambda: self.switch_callback("multi"),
            **btn_style
        ).pack(pady=10)

        # Option 4: Convert all segmentations to bounding boxes only
        tk.Button(
            self,
            text="4. Convert to BBoxes only (no masks)",
            command=lambda: self.switch_callback("Bbox"),
            **btn_style
        ).pack(pady=10)
