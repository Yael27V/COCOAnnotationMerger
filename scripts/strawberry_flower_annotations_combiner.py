"""
Strawberry & Flower COCO Annotation Combiner (POO)

Author: Yael Vicente
Date: March 27, 2025
Version: 2.0 (OOP Refactored)

Description:
    This script merges COCO annotations from two directories:
    - One with strawberry annotations (categories: fruit_ripe, fruit_unripe).
    - One with flower annotations (category: flower).
    
    Each annotation file corresponds to a single image (COCO format).
    The script:
    - Matches annotations to their corresponding image via filename.
    - Reassigns unique IDs to images and annotations.
    - Reassigns the flower category ID to avoid conflicts.
    - Outputs a single merged COCO-format JSON file.

Usage:
    1. Update the config variables in the `if __name__ == "__main__"` section.
    2. Run the script: `python StrawberryFlowerAnnotationCombiner.py`
"""

import os
import json
from collections import defaultdict, Counter
from pathlib import Path


class COCOAnnotationCombiner:
    def __init__(self, dir_strawberries: str, dir_flowers: str, output_file: str):
        self.dir_strawberries = dir_strawberries
        self.dir_flowers = dir_flowers
        self.output_file = output_file

        self.strawberry_annotations = []
        self.flower_annotations = []

    def load_annotations_from_directory(self, directory: str) -> list:
        """Load all COCO annotation JSON files from a directory."""
        annotations = []
        for file in os.listdir(directory):
            if file.endswith(".json"):
                path = os.path.join(directory, file)
                with open(path, "r") as f:
                    data = json.load(f)
                    annotations.append(data)
        return annotations

    def process_annotations(self, annotation_files: list, valid_categories: dict, new_flower_id=None) -> dict:
        """
        Organize annotations by image filename.

        Returns:
            Dictionary mapping image filename -> (image_dict, [annotations])
        """
        result = {}
        for data in annotation_files:
            if not data["annotations"] or not data["images"]:
                continue

            image = data["images"][0]
            file_name = image["file_name"]

            image_dict = image.copy()
            valid_anns = []

            for ann in data["annotations"]:
                if ann["category_id"] in valid_categories.values():
                    ann_copy = ann.copy()
                    if new_flower_id and ann["category_id"] == valid_categories.get("flower"):
                        ann_copy["category_id"] = new_flower_id
                    ann_copy["image_id"] = file_name  # temporary placeholder
                    valid_anns.append(ann_copy)

            result[file_name] = (image_dict, valid_anns)
        return result

    def combine_datasets(self, straw_dict: dict, flower_dict: dict):
        """Combine two annotation dictionaries and assign new unique IDs."""
        final_images, final_annotations = [], []
        stats = Counter()

        image_id_counter = 1
        annotation_id_counter = 1
        all_filenames = set(straw_dict.keys()) | set(flower_dict.keys())

        for name in all_filenames:
            image = straw_dict.get(name, flower_dict.get(name))[0]
            image["id"] = image_id_counter
            final_images.append(image)

            anns_straw = straw_dict.get(name, (None, []))[1]
            anns_flower = flower_dict.get(name, (None, []))[1]
            all_anns = anns_straw + anns_flower

            for ann in all_anns:
                ann["id"] = annotation_id_counter
                ann["image_id"] = image_id_counter
                stats[ann["category_id"]] += 1
                final_annotations.append(ann)
                annotation_id_counter += 1

            image_id_counter += 1

        return final_images, final_annotations, stats

    def run(self):
        print("🔄 Loading strawberry annotations...")
        self.strawberry_annotations = self.load_annotations_from_directory(self.dir_strawberries)
        print("🔄 Loading flower annotations...")
        self.flower_annotations = self.load_annotations_from_directory(self.dir_flowers)

        # Extract category info
        strawberry_cats = {cat["name"]: cat["id"] for cat in self.strawberry_annotations[0]["categories"]}
        flower_cats = {cat["name"]: cat["id"] for cat in self.flower_annotations[0]["categories"]}

        id_fruit_ripe = strawberry_cats["fruit_ripe"]
        id_fruit_unripe = strawberry_cats["fruit_unripe"]
        id_flower_original = flower_cats["flower"]
        id_flower_new = max(id_fruit_ripe, id_fruit_unripe) + 1

        # Process all individual annotations
        straw_dict = self.process_annotations(self.strawberry_annotations, strawberry_cats)
        flower_dict = self.process_annotations(self.flower_annotations, flower_cats, new_flower_id=id_flower_new)

        print("🔗 Merging annotations...")
        images, annotations, stats = self.combine_datasets(straw_dict, flower_dict)

        print("💾 Saving merged file...")
        merged_data = {
            "info": self.strawberry_annotations[0].get("info", {}),
            "licenses": self.strawberry_annotations[0].get("licenses", []),
            "images": images,
            "annotations": annotations,
            "categories": [
                {"id": id_fruit_ripe, "name": "fruit_ripe"},
                {"id": id_fruit_unripe, "name": "fruit_unripe"},
                {"id": id_flower_new, "name": "flower"}
            ]
        }

        save_path = Path(self.output_file).resolve()
        with open(save_path, "w") as f:
            json.dump(merged_data, f, indent=4)

        # Print summary
        print("\n📊 Final Statistics:")
        for cat in merged_data["categories"]:
            print(f"  - {cat['name']} (ID {cat['id']}): {stats.get(cat['id'], 0)} annotations")

        print(f"\n🖼️ Total Images: {len(images)}")
        print(f"🏷️ Total Annotations: {len(annotations)}")
        print(f"\n✅ Merged annotation file saved at: {save_path}")
