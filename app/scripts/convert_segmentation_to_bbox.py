"""
COCOSegmentationToBBoxConverter - Converts COCO Segmentations to Bounding Box Format for CVAT Compatibility

Author: Yael Vicente  
Date: April 3, 2025  
Version: 1.0

Description:
    This class provides functionality to process and clean COCO annotation files by removing 
    polygon segmentations and leaving only bounding boxes (bbox). This transformation is required 
    for compatibility with CVAT when importing annotations as pure bounding boxes.

    Features:
        - Validates essential COCO structure.
        - Sets "segmentation": [] for all annotations.
        - Filters invalid bbox entries.
        - Saves the cleaned file in standard COCO format (JSON).
"""

import json
from typing import Dict, Any


class COCOSegmentationToBBoxConverter:
    """
    Cleans COCO annotation files by removing segmentation data and keeping only bounding boxes.

    This class is used to convert segmentation-based COCO annotations to a format accepted by CVAT,
    where 'segmentation' is set as an empty list. It also ensures the required structure of the
    COCO JSON and filters out invalid bounding boxes.
    """

    def __init__(self, input_path: str, output_path: str):
        """
        Initializes the converter with input and output paths.

        Args:
            input_path (str): Path to the original COCO annotation file.
            output_path (str): Path where the cleaned JSON will be saved.
        """
        self.input_path = input_path
        self.output_path = output_path
        self.coco_data: Dict[str, Any] = {}
        self.required_keys = ["info", "licenses", "images", "annotations", "categories"]

    def load(self):
        """
        Loads the COCO annotation JSON from disk.

        Raises:
            FileNotFoundError: If the input file does not exist.
            json.JSONDecodeError: If the file is not a valid JSON.
        """
        with open(self.input_path, 'r') as f:
            self.coco_data = json.load(f)

    def validate(self):
        """
        Validates the structure of the COCO JSON file.

        Ensures that all the required top-level keys are present.

        Raises:
            ValueError: If any required key is missing.
        """
        for key in self.required_keys:
            if key not in self.coco_data:
                raise ValueError(f"Missing required key in COCO JSON: '{key}'")

    def clean_annotations(self):
        """
        Cleans the annotation entries:
            - Sets 'segmentation' to an empty list.
            - Removes annotations with invalid or incomplete bbox fields.
        """
        cleaned = []
        for ann in self.coco_data.get("annotations", []):
            ann["segmentation"] = []
            if (
                "bbox" in ann and
                isinstance(ann["bbox"], list) and
                len(ann["bbox"]) == 4 and
                all(isinstance(v, (int, float)) and v >= 0 for v in ann["bbox"])
            ):
                cleaned.append(ann)
        self.coco_data["annotations"] = cleaned

    def save(self):
        """
        Saves the cleaned COCO annotation data to the output file.

        Raises:
            IOError: If the file cannot be written.
        """
        with open(self.output_path, 'w') as f:
            json.dump(self.coco_data, f, indent=2)

    def convert(self):
        """
        Executes the full conversion process:
            1. Loads the input file.
            2. Validates its structure.
            3. Cleans the annotations.
            4. Saves the result to disk.
        """
        self.load()
        self.validate()
        self.clean_annotations()
        self.save()
        print(f"[✔] COCO annotations converted successfully: {self.output_path}")