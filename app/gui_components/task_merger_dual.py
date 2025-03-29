"""
DualMergerUI - GUI Component for Merging Two COCO Annotation Files (Strawberries + Flowers)

Author: Yael Vicente  
Date: March 28, 2025  
Version: 1.0  

Description:
    This component provides a graphical interface to merge two COCO annotation files:
    - One file with strawberry annotations.
    - One file with flower annotations.

    The user can:
    - Select both input JSON files.
    - Select the destination path for the merged file.
    - Execute the merge using a modular, object-oriented script.
    - View post-merge statistics including total images, annotations, and breakdown by category.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Label, Entry
from scripts.strawberry_flower_annotation import COCOAnnotationMerger as DualMerger


class DualMergerUI(tk.Frame):
    """
    A UI Frame for merging two COCO annotation files (one for strawberries, one for flowers).

    Attributes:
        straw_file (tk.StringVar): Path to the strawberry annotation file.
        flower_file (tk.StringVar): Path to the flower annotation file.
        output_file (tk.StringVar): Destination path for the merged annotation file.
        stats_label (tk.Label): Optional label to show annotation statistics after merging.
    """

    def __init__(self, master):
        super().__init__(master, bg="#e6f0fa")
        self.straw_file = tk.StringVar()
        self.flower_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.stats_label = None
        self._build_ui()

    def _build_ui(self):
        """Constructs the interface with labeled file selectors and action button."""
        Label(self, text="Merge Two COCO Files (Strawberries + Flowers)", font=("Helvetica", 14, "bold"),
              background="#e6f0fa", foreground="#003366").pack(pady=10)

        self._create_path_selector("Strawberry Annotation File:", self.straw_file, self.browse_straw)
        self._create_path_selector("Flower Annotation File:", self.flower_file, self.browse_flower)
        self._create_path_selector("Output File (.json):", self.output_file, self.save_output)

        # Action Button
        tk.Button(self, text="Run Merge", command=self.run_merge, font=("Helvetica", 11, "bold"),
                  bg="#007acc", fg="white", activebackground="#005f99", relief="flat", padx=10, pady=5).pack(pady=10)

    def _create_path_selector(self, label_text, variable, browse_command):
        """
        Creates a row with label, entry field and browse button.

        Args:
            label_text (str): Description for the input.
            variable (tk.StringVar): Linked variable to store the file path.
            browse_command (function): Function to invoke on 'Browse' button click.
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

    def browse_straw(self):
        """Opens a file dialog to select the strawberry annotation JSON file."""
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            self.straw_file.set(path)

    def browse_flower(self):
        """Opens a file dialog to select the flower annotation JSON file."""
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            self.flower_file.set(path)

    def save_output(self):
        """Opens a save dialog to define the output file location."""
        path = filedialog.asksaveasfilename(defaultextension=".json")
        if path:
            self.output_file.set(path)

    def run_merge(self):
        """Validates inputs, runs the merge, and displays results or errors."""
        if not self.straw_file.get() or not self.flower_file.get() or not self.output_file.get():
            messagebox.showerror("Error", "Please select all paths.")
            return
        try:
            merger = DualMerger(self.straw_file.get(), self.flower_file.get(), self.output_file.get())
            merger.merge()
            messagebox.showinfo("Done", f"Merged file saved at:\n{self.output_file.get()}")
            self.display_stats(merger)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_stats(self, merger):
        """
        Displays merge statistics after merging.

        Args:
            merger (COCOAnnotationMerger): The merger object used to perform the merge.
        """
        merged_data = merger.load_json(merger.output_file)

        if self.stats_label:
            self.stats_label.destroy()

        total_images = len(merged_data.get("images", []))
        total_anns = len(merged_data.get("annotations", []))
        categories = {cat["id"]: cat["name"] for cat in merged_data.get("categories", [])}
        counter = {}
        for ann in merged_data["annotations"]:
            cat_id = ann["category_id"]
            counter[cat_id] = counter.get(cat_id, 0) + 1

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
