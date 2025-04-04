"""
SegmentationToBBoxUI - GUI Component for Converting COCO Segmentations to Bounding Boxes

Author: Yael Vicente
Date: April 3, 2025
Version: 1.1

Description:
    This class defines a GUI component that allows the user to convert a COCO annotation file
    from polygon segmentations to pure bounding box format for CVAT compatibility.

    Features:
        - Select a COCO JSON file with segmentations.
        - Choose an output path for the cleaned file.
        - Perform the conversion with one click.
        - Display summary statistics after conversion.
        - Display success or error messages to the user.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Label, Entry
from pathlib import Path
from scripts.convert_segmentation_to_bbox import COCOSegmentationToBBoxConverter


class SegmentationToBBoxUI(tk.Frame):
    """
    UI frame for converting COCO segmentations into bounding boxes only format.

    Attributes:
        input_file (tk.StringVar): Path to the input COCO annotation JSON.
        output_file (tk.StringVar): Path to save the converted JSON.
    """

    def __init__(self, master):
        super().__init__(master, bg="#e6f0fa")
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.stats_label = None
        self._build_ui()

    def _build_ui(self):
        """Builds the UI layout including fields and buttons."""
        Label(
            self,
            text="Convert COCO (Segmentation → Bounding Boxes)",
            font=("Helvetica", 14, "bold"),
            background="#e6f0fa",
            foreground="#003366"
        ).pack(pady=10)

        self._create_path_selector("Input COCO File (.json):", self.input_file, self.browse_input_file)
        self._create_path_selector("Output File (.json):", self.output_file, self.browse_output_file)

        tk.Button(
            self,
            text="Run Convert",
            command=self.start_conversion,
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

    def browse_input_file(self):
        """Opens a file dialog to select the input COCO annotation file."""
        selected = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if selected:
            self.input_file.set(selected)

    def browse_output_file(self):
        """Opens a save file dialog to select the output JSON path."""
        selected = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if selected:
            self.output_file.set(selected)

    def start_conversion(self):
        """Runs the conversion process and handles success or errors."""
        input_path = self.input_file.get()
        output_path = self.output_file.get()

        if not input_path or not output_path:
            messagebox.showwarning("Missing Input", "Please select both input and output files.")
            return

        try:
            converter = COCOSegmentationToBBoxConverter(input_path, output_path)
            converter.convert()
            self.display_stats(converter.coco_data, output_path)
            messagebox.showinfo("Success", f"File converted successfully:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def display_stats(self, data, output_path):
        """
        Displays summary statistics of the converted annotation file.

        Args:
            data (dict): Converted COCO-format annotation dictionary.
            output_path (str): Path to the saved output file.
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

        stat_text = f"\U0001F4BE File saved at: {output_path}\n"
        stat_text += f"\n📊 Conversion Statistics:\n"
        stat_text += f"- Total Images: {total_images}\n"
        stat_text += f"- Total Annotations: {total_anns}\n"
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
