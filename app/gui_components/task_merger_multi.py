"""
MultiMergerUI - GUI Component for Merging Annotations from Two Folders (Strawberries + Flowers)

Author: Yael Vicente
Date: March 28, 2025
Version: 1.0

Description:
    This component provides a graphical interface to merge all COCO annotations from two separate
    folders (one containing strawberry annotations and one containing flower annotations). The UI allows:

        - Folder selection for strawberry and flower annotations.
        - Output file path definition.
        - Execution of merging using a POO-based backend.
        - Display of merge statistics: total images, annotations, and per-category breakdown.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Label, Entry
from scripts.strawberry_flower_annotations_combiner import COCOAnnotationCombiner
import json


class MultiMergerUI(tk.Frame):
    """
    UI Frame to merge multiple COCO annotation files from two folders:
    one for strawberries and one for flowers.

    Attributes:
        dir_straw (tk.StringVar): Path to strawberry annotation folder.
        dir_flower (tk.StringVar): Path to flower annotation folder.
        output_file (tk.StringVar): Destination path for the merged annotation JSON.
        stats_label (tk.Label): Optional stats label displayed after merging.
    """

    def __init__(self, master):
        super().__init__(master, bg="#e6f0fa")
        self.dir_straw = tk.StringVar()
        self.dir_flower = tk.StringVar()
        self.output_file = tk.StringVar()
        self.stats_label = None
        self._build_ui()

    def _build_ui(self):
        """Builds the layout of the UI including path selectors and action button."""
        Label(
            self,
            text="Merge All Annotations from Two Folders (Strawberries + Flowers)",
            font=("Helvetica", 14, "bold"),
            background="#e6f0fa",
            foreground="#003366"
        ).pack(pady=10)

        self._create_path_selector("Strawberry annotations directory:", self.dir_straw, self.browse_straw_dir)
        self._create_path_selector("Flower annotations directory:", self.dir_flower, self.browse_flower_dir)
        self._create_path_selector("Output file path (.json):", self.output_file, self.save_output)

        # Main action button
        tk.Button(
            self,
            text="Merge Annotations",
            command=self.run_merge,
            font=("Helvetica", 11, "bold"),
            bg="#007acc",
            fg="white",
            activebackground="#005f99",
            relief="flat",
            padx=10,
            pady=5
        ).pack(pady=10)

    def _create_path_selector(self, label_text, variable, browse_command):
        """
        Creates a labeled entry with a 'Browse' button.

        Args:
            label_text (str): Descriptive label text.
            variable (tk.StringVar): Variable to bind the input.
            browse_command (callable): Callback for the Browse button.
        """
        container = tk.Frame(self, bg="#e6f0fa")
        container.pack(fill="x", padx=40, pady=8)

        label = tk.Label(
            container,
            text=label_text,
            font=("Helvetica", 11),
            bg="#e6f0fa",
            fg="#003366"
        )
        label.pack(anchor="w", pady=(0, 4))

        entry_frame = tk.Frame(container, bg="#e0e0e0")
        entry_frame.pack(fill="x")

        entry = tk.Entry(
            entry_frame,
            textvariable=variable,
            font=("Helvetica", 11),
            bg="#f8f8f8",
            fg="black",
            relief="flat",
            bd=0,
            insertbackground="#000000"
        )
        entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(6, 4), pady=4)

        browse_btn = tk.Button(
            entry_frame,
            text="Browse",
            command=browse_command,
            font=("Helvetica", 10, "bold"),
            bg="#4a90e2",
            fg="white",
            activebackground="#2d6ca2",
            relief="flat",
            padx=10,
            pady=6
        )
        browse_btn.pack(side="right", padx=(4, 6), pady=4)

    def browse_straw_dir(self):
        """Opens a folder dialog to select the strawberry annotation folder."""
        path = filedialog.askdirectory()
        if path:
            self.dir_straw.set(path)

    def browse_flower_dir(self):
        """Opens a folder dialog to select the flower annotation folder."""
        path = filedialog.askdirectory()
        if path:
            self.dir_flower.set(path)

    def save_output(self):
        """Opens a save dialog to select where to store the merged output file."""
        path = filedialog.asksaveasfilename(defaultextension=".json")
        if path:
            self.output_file.set(path)

    def run_merge(self):
        """Runs the merge process and displays results or errors."""
        if not self.dir_straw.get() or not self.dir_flower.get() or not self.output_file.get():
            messagebox.showerror("Error", "Please select all paths.")
            return

        try:
            combiner = COCOAnnotationCombiner(
                self.dir_straw.get(),
                self.dir_flower.get(),
                self.output_file.get()
            )
            combiner.run()
            self.display_stats(self.output_file.get())
            messagebox.showinfo("Success", f"Merged annotation saved to:\n{self.output_file.get()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_stats(self, file_path):
        """
        Loads the merged JSON and displays image/annotation/category statistics.

        Args:
            file_path (str): Path to the merged annotation file.
        """
        with open(file_path, "r") as f:
            data = json.load(f)

        if self.stats_label:
            self.stats_label.destroy()

        total_images = len(data.get("images", []))
        total_anns = len(data.get("annotations", []))
        counter = {}
        for ann in data.get("annotations", []):
            cat_id = ann["category_id"]
            counter[cat_id] = counter.get(cat_id, 0) + 1

        categories = {cat["id"]: cat["name"] for cat in data["categories"]}
        stat_text = f"📊 Merged Statistics:\n- Total Images: {total_images}\n- Total Annotations: {total_anns}\n"
        for cat_id, count in counter.items():
            stat_text += f"- {categories.get(cat_id, 'Unknown')} (ID {cat_id}): {count}\n"

        self.stats_label = tk.Label(
            self,
            text=stat_text,
            font=("Courier", 10),
            bg="#e6f0fa",
            justify="left",
            fg="#003366"
        )
        self.stats_label.pack(pady=10)