"""
COCO Annotation Merger GUI

Author: Yael Vicente
Last Updated: March 2025
Version: 1.1

Description:
    This script defines the main application class and entry point for a graphical
    user interface (GUI) that allows users to merge COCO annotation files.

    It supports three merge strategies:
        1. Merging multiple JSON files with the same categories.
        2. Merging two JSON files with different categories.
        3. Merging all JSON files from two folders (e.g., strawberries and flowers).

    This version sets a custom application icon using a .ico file.
"""

import tkinter as tk
from tkinter import Label, Frame
import os

# UI Components
from gui_components.task_selector import TaskSelector
from gui_components.task_merger_single import SingleMergerUI
from gui_components.task_merger_dual import DualMergerUI
from gui_components.task_merger_multi import MultiMergerUI


class COCOAnnotationApp:
    """
    Main application class for the COCO Annotation Merger GUI.
    Handles UI setup, layout, and task switching logic.
    """
    def __init__(self, root):
        """
        Initialize the main GUI window.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("COCO Annotation Merger")
        self.root.geometry("800x800")
        self.root.configure(bg="#e6f0fa")  # Light blue background

        # === Set custom application icon ===
        try:
            icon_path = os.path.join("assets", "logo.ico")  # Make sure logo.ico exists
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"⚠️ Could not set window icon: {e}")

        # === Main header ===
        self.header = Label(
            self.root,
            text="COCO Annotation Merger",
            font=("Helvetica", 20, "bold"),
            background="#e6f0fa",
            foreground="#0a3d62"
        )
        self.header.pack(pady=20)

        # === Main container for UI components ===
        self.main_frame = Frame(self.root, background="#e6f0fa")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # === Task selector panel ===
        self.task_selector = TaskSelector(self.root, self.select_task)
        self.task_selector.pack(pady=10)

        # === Currently selected task panel ===
        self.active_task_frame = None

    def select_task(self, task_type):
        """
        Switch between task UIs depending on the selected merge strategy.

        Args:
            task_type (str): One of "single", "dual", or "multi".
        """
        # Remove previous task frame if present
        if self.active_task_frame:
            self.active_task_frame.destroy()

        # Load new task frame
        if task_type == "single":
            self.active_task_frame = SingleMergerUI(self.main_frame)
        elif task_type == "dual":
            self.active_task_frame = DualMergerUI(self.main_frame)
        elif task_type == "multi":
            self.active_task_frame = MultiMergerUI(self.main_frame)

        # Display new task frame
        if self.active_task_frame:
            self.active_task_frame.pack(fill="both", expand=True)


# === Entry point ===
if __name__ == "__main__":
    root = tk.Tk()
    app = COCOAnnotationApp(root)
    root.mainloop()
