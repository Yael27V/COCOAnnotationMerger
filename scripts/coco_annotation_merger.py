"""
COCO Annotation Merger (OOP Version)

Author: Yael Vicente
Date: March 27, 2025
Version: 2.0 (OOP Refactored)

Description:
    Object-oriented version of a script that merges multiple COCO annotation JSON files
    into a single dataset. It ensures:

    - Unique image, annotation, and category IDs.
    - Deduplication of license information.
    - Preservation of fields like confidence and orientation.
    - Correct remapping of category and image IDs.

Usage:
    merger = COCOAnnotationMerger(input_dir, output_file)
    merger.run()
"""

import os
import json
import glob
from pathlib import Path
from collections import defaultdict


class COCOAnnotationMerger:
    def __init__(self, input_dir: str, output_file: str):
        self.input_dir = input_dir
        self.output_file = Path(output_file).resolve()

        self.merged_data = {
            "info": {},
            "licenses": [],
            "images": [],
            "annotations": [],
            "categories": []
        }

        self.license_map = {}
        self.category_map = {}
        self.image_id_map = {}

        self.next_license_id = 1
        self.next_category_id = 1
        self.next_image_id = 1
        self.next_annotation_id = 1

    def run(self):
        self.process_all_files()
        self.clean_empty_fields()
        self.save_output()
        self.print_summary()

    def process_all_files(self):
        for json_file in glob.glob(os.path.join(self.input_dir, "*.json")):
            print(f"Processing file: {json_file}")
            with open(json_file, 'r', encoding='utf-8') as f:
                coco_data = json.load(f)
            self.process_info(coco_data)
            self.process_licenses(coco_data)
            self.process_categories(coco_data)
            self.process_images(coco_data)
            self.process_annotations(coco_data)

    def process_info(self, coco_data):
        if "info" in coco_data and (not self.merged_data["info"] or 
            coco_data["info"].get("date_created", "") > self.merged_data["info"].get("date_created", "")):
            self.merged_data["info"] = coco_data["info"]

    def process_licenses(self, coco_data):
        for license in coco_data.get("licenses", []):
            key = (license.get("name", ""), license.get("url", ""))
            if key not in self.license_map:
                self.license_map[key] = self.next_license_id
                new_license = license.copy()
                new_license["id"] = self.next_license_id
                self.merged_data["licenses"].append(new_license)
                self.next_license_id += 1

    def process_categories(self, coco_data):
        for category in coco_data.get("categories", []):
            key = (category["name"], category.get("supercategory", ""))
            if key not in self.category_map:
                self.category_map[key] = self.next_category_id
                new_category = category.copy()
                new_category["id"] = self.next_category_id
                self.merged_data["categories"].append(new_category)
                self.next_category_id += 1

    def process_images(self, coco_data):
        for image in coco_data.get("images", []):
            old_image_id = image["id"]
            self.image_id_map[old_image_id] = self.next_image_id
            new_image = image.copy()
            new_image["id"] = self.next_image_id

            if "license" in image:
                for license in coco_data.get("licenses", []):
                    if license["id"] == image["license"]:
                        key = (license.get("name", ""), license.get("url", ""))
                        if key in self.license_map:
                            new_image["license"] = self.license_map[key]
                        break

            self.merged_data["images"].append(new_image)
            self.next_image_id += 1

    def process_annotations(self, coco_data):
        for ann in coco_data.get("annotations", []):
            if ann["image_id"] not in self.image_id_map:
                continue
            new_ann = ann.copy()
            new_ann["id"] = self.next_annotation_id
            new_ann["image_id"] = self.image_id_map[ann["image_id"]]

            if "confidence" in ann:
                new_ann["confidence"] = ann["confidence"]
            if "orientation" in ann:
                new_ann["orientation"] = ann["orientation"]

            for category in coco_data.get("categories", []):
                if category["id"] == ann["category_id"]:
                    key = (category["name"], category.get("supercategory", ""))
                    if key in self.category_map:
                        new_ann["category_id"] = self.category_map[key]
                    break

            self.merged_data["annotations"].append(new_ann)
            self.next_annotation_id += 1

    def clean_empty_fields(self):
        for key in list(self.merged_data.keys()):
            if not self.merged_data[key]:
                del self.merged_data[key]

    def save_output(self):
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.merged_data, f, indent=2, ensure_ascii=False)

    def print_summary(self):
        print(f"\n✅ Combined file saved at: {self.output_file}")
        print(f"📊 Total Images: {len(self.merged_data.get('images', []))}")
        print(f"📊 Total Annotations: {len(self.merged_data.get('annotations', []))}")
        print(f"📊 Total Categories: {len(self.merged_data.get('categories', []))}")
        print(f"📊 Total Licenses: {len(self.merged_data.get('licenses', []))}")
