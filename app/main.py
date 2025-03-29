"""
COCO Annotation Merger GUI

Author: Yael Vicente
Last Updated: March 2025
Version: 1.0

Description:
    This script defines the main application class and entry point for a graphical
    user interface (GUI) that allows users to merge COCO annotation files.

    It supports three modes of merging:
        1. Merging multiple JSON files with the same categories.
        2. Merging two JSON files with different categories.
        3. Merging all JSON files from two folders (e.g., strawberries and flowers).

    The GUI is built using Tkinter and follows a modular structure with components
    for task selection and dedicated UI panels per merge strategy.
"""

import os
import sys
import platform
import tkinter as tk
from tkinter import Label, Frame, PhotoImage

# Import UI components
from gui_components.task_selector import TaskSelector
from gui_components.task_merger_single import SingleMergerUI
from gui_components.task_merger_dual import DualMergerUI
from gui_components.task_merger_multi import MultiMergerUI


class COCOAnnotationApp:
    """
    Main GUI application class for COCO Annotation Merger.
    Initializes the window, layout, and handles task selection.
    """
    def __init__(self, root):
        """
        Initialize the main window and layout.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("COCO Annotation Merger")
        self.root.geometry("800x800")
        self.root.configure(bg="#e6f0fa")  # Light blue background

        # Cross-platform icon support
        self.set_window_icon()

        # Header label
        self.header = Label(
            root,
            text="COCO Annotation Merger",
            font=("Helvetica", 20, "bold"),
            background="#e6f0fa",
            foreground="#0a3d62"
        )
        self.header.pack(pady=20)

        # Container where task-specific UI components will be displayed
        self.main_frame = Frame(root, background="#e6f0fa")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Task selector menu at the bottom of the window
        self.task_selector = TaskSelector(self.root, self.select_task)
        self.task_selector.pack(pady=10)

        # Active task frame (e.g., SingleMergerUI, DualMergerUI, etc.)
        self.active_task_frame = None

    def set_window_icon(self):
        """
        Set the window icon depending on the platform.
        Uses .ico for Windows, .png for others.
        """
        # Icon handling (cross-platform and PyInstaller safe)
        try:
            if hasattr(sys, "_MEIPASS"):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.abspath(".")
            logo_path = os.path.join(base_path, "assets", "logo.png")
            icon_img = PhotoImage(file=logo_path)
            self.root.iconphoto(True, icon_img)
        except Exception as e:
            print(f"⚠️ Could not set icon: {e}")

    def select_task(self, task_type):
        """
        Callback for switching between annotation merge tasks.

        Args:
            task_type (str): Type of the merge task. Can be "single", "dual", or "multi".
        """
        # Remove previous task frame if any
        if self.active_task_frame:
            self.active_task_frame.destroy()

        # Load new task UI based on selection
        if task_type == "single":
            self.active_task_frame = SingleMergerUI(self.main_frame)
        elif task_type == "dual":
            self.active_task_frame = DualMergerUI(self.main_frame)
        elif task_type == "multi":
            self.active_task_frame = MultiMergerUI(self.main_frame)

        # Show new UI frame
        if self.active_task_frame:
            self.active_task_frame.pack(fill="both", expand=True)


# Entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = COCOAnnotationApp(root)
    root.mainloop()
