"""
SingleMergerUI - GUI Component for Merging Multiple COCO Files with the Same Categories

Author: Yael Vicente
Date: March 28, 2025
Version: 1.0

Description:
    This class defines the GUI component for merging multiple COCO annotation files 
    that share the same categories. It allows the user to:
        - Select an input directory with JSON files.
        - Choose an output destination for the merged JSON.
        - Start the merge operation.
        - View summary statistics after the merge.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Label, Entry
from pathlib import Path
from scripts.coco_annotation_merger import COCOAnnotationMerger


class SingleMergerUI(tk.Frame):
    """
    UI frame for merging multiple COCO annotation files with shared categories.

    Attributes:
        input_dir (tk.StringVar): Directory containing input JSON files.
        output_file (tk.StringVar): Destination path for the merged output JSON.
        stats_label (tk.Label): Optional label displaying summary statistics after merge.
    """

    def __init__(self, master):
        super().__init__(master, bg="#e6f0fa")
        self.input_dir = tk.StringVar()
        self.output_file = tk.StringVar()
        self.stats_label = None
        self._build_ui()

    def _build_ui(self):
        """Builds the full UI layout including labels, entry fields and buttons."""
        Label(
            self,
            text="Merge Multiple COCO Files (Same Categories)",
            font=("Helvetica", 14, "bold"),
            background="#e6f0fa",
            foreground="#003366"
        ).pack(pady=10)

        self._create_path_selector("Input annotations directory:", self.input_dir, self.browse_input_dir)
        self._create_path_selector("Output File (.json):", self.output_file, self.browse_output_file)

        # Main button to run the merge operation
        tk.Button(
            self,
            text="Start Merge",
            command=self.start_merge,
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
        Creates a labeled input field with a browse button.

        Args:
            label_text (str): Text displayed above the input field.
            variable (tk.StringVar): Tkinter variable to bind input value.
            browse_command (callable): Function triggered on 'Browse' click.
        """
        # Outer container
        container = tk.Frame(self, bg="#e6f0fa")
        container.pack(fill="x", padx=40, pady=8)

        # Label
        label = tk.Label(
            container,
            text=label_text,
            font=("Helvetica", 11),
            bg="#e6f0fa",
            fg="#003366"
        )
        label.pack(anchor="w", pady=(0, 4))

        # Entry + Browse button frame
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

    def browse_input_dir(self):
        """Opens a file dialog to select the input directory containing JSON files."""
        selected = filedialog.askdirectory()
        if selected:
            self.input_dir.set(selected)

    def browse_output_file(self):
        """Opens a save file dialog to select output file path."""
        selected = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[["JSON Files", "*.json"]])
        if selected:
            self.output_file.set(selected)

    def start_merge(self):
        """Starts the merge process and handles errors or success messaging."""
        input_path = self.input_dir.get()
        output_path = self.output_file.get()

        if not input_path or not output_path:
            messagebox.showwarning("Missing Input", "Please select both input directory and output file.")
            return

        try:
            merger = COCOAnnotationMerger(input_path, output_path)
            merger.run()
            messagebox.showinfo("Success", f"Merged annotation saved to:\n{output_path}")
            self.display_stats(merger.merged_data)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def display_stats(self, data):
        """
        Displays summary statistics of the merged annotation result.

        Args:
            data (dict): Merged COCO-format annotation dictionary.
        """
        if self.stats_label:
            self.stats_label.destroy()

        total_images = len(data.get("images", []))
        total_anns = len(data.get("annotations", []))
        category_counts = {}
        for ann in data.get("annotations", []):
            cat_id = ann["category_id"]
            category_counts[cat_id] = category_counts.get(cat_id, 0) + 1

        categories = {cat["id"]: cat["name"] for cat in data.get("categories", [])}

        stat_text = f"📊 Merged Statistics:\n- Total Images: {total_images}\n- Total Annotations: {total_anns}\n"
        for cat_id, count in category_counts.items():
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
