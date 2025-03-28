"""
Combination strawberry flower annotations

Optimized COCO Annotation Merger

Author: Yael Vicente
Date: March 26, 2025
Version: 2.0 (OOP Refactored)

Description:
    - This script merges two COCO annotation files: one for strawberries and one for flowers.
    - Assigns a unique ID for the 'flower' category to avoid conflicts.
    - Preserves category IDs for 'fruit_ripe' and 'fruit_unripe'.
    - Outputs a combined COCO file with all merged annotations.

Usage:
    - Instantiate the COCOAnnotationMerger class with input paths.
    - Call the merge() method to generate the combined JSON.
"""

import json
from collections import defaultdict, Counter
from pathlib import Path


class COCOAnnotationMerger:
    def __init__(self, strawberry_file, flower_file, output_file):
        self.strawberry_file = strawberry_file
        self.flower_file = flower_file
        self.output_file = output_file

    def load_json(self, filepath):
        with open(filepath, "r") as f:
            return json.load(f)

    def get_category_ids(self, data):
        return {cat["name"]: cat["id"] for cat in data["categories"]}

    def organize_annotations(self, data, valid_categories, new_flower_id=None):
        image_map = {img["id"]: img["file_name"] for img in data["images"]}
        annotations = defaultdict(list)

        for ann in data["annotations"]:
            if ann["category_id"] in valid_categories.values():
                file_name = image_map.get(ann["image_id"])
                if file_name:
                    if new_flower_id and ann["category_id"] == valid_categories["flower"]:
                        ann["category_id"] = new_flower_id
                    annotations[file_name].append(ann)

        return annotations

    def merge_annotations(self, strawberry_imgs, flower_imgs, strawberry_anns, flower_anns):
        merged_images, merged_annotations = {}, []
        img_id_counter, ann_id_counter = 1, 1

        for file_name in set(strawberry_imgs) | set(flower_imgs):
            img = strawberry_imgs.get(file_name, flower_imgs.get(file_name))
            img["id"] = img_id_counter
            merged_images[file_name] = img
            img_id_counter += 1

        for file_name, img in merged_images.items():
            image_id = img["id"]
            combined_anns = strawberry_anns.get(file_name, []) + flower_anns.get(file_name, [])

            for ann in combined_anns:
                ann["image_id"] = image_id
                ann["id"] = ann_id_counter
                ann_id_counter += 1
                merged_annotations.append(ann)

        return list(merged_images.values()), merged_annotations

    def count_categories(self, annotations):
        return Counter(ann["category_id"] for ann in annotations)

    def save_json(self, data):
        output_path = Path(self.output_file).resolve()
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
        return output_path

    def merge(self):
        strawberries_data = self.load_json(self.strawberry_file)
        flowers_data = self.load_json(self.flower_file)

        strawberry_cats = self.get_category_ids(strawberries_data)
        flower_cats = self.get_category_ids(flowers_data)

        fruit_ripe_id = strawberry_cats.get("fruit_ripe")
        fruit_unripe_id = strawberry_cats.get("fruit_unripe")
        flower_original_id = flower_cats.get("flower")

        if not all([fruit_ripe_id, fruit_unripe_id, flower_original_id]):
            raise ValueError("Missing expected categories in input files.")

        flower_new_id = max(fruit_ripe_id, fruit_unripe_id) + 1

        strawberry_anns = self.organize_annotations(strawberries_data, strawberry_cats)
        flower_anns = self.organize_annotations(flowers_data, {"flower": flower_original_id}, flower_new_id)

        strawberry_imgs = {img["file_name"]: img for img in strawberries_data["images"]}
        flower_imgs = {img["file_name"]: img for img in flowers_data["images"]}

        merged_images, merged_annotations = self.merge_annotations(
            strawberry_imgs, flower_imgs, strawberry_anns, flower_anns
        )

        final_coco = {
            "info": strawberries_data.get("info", {}),
            "licenses": strawberries_data.get("licenses", []),
            "images": merged_images,
            "annotations": merged_annotations,
            "categories": [
                {"id": fruit_ripe_id, "name": "fruit_ripe"},
                {"id": fruit_unripe_id, "name": "fruit_unripe"},
                {"id": flower_new_id, "name": "flower"}
            ]
        }

        save_path = self.save_json(final_coco)

        final_counts = self.count_categories(merged_annotations)
        category_names = {cat["id"]: cat["name"] for cat in final_coco["categories"]}

        print("\n📊 Merged Annotation Statistics:")
        for cat_id, count in sorted(final_counts.items()):
            print(f"  - {category_names.get(cat_id, 'Unknown')} (ID {cat_id}): {count} annotations")

        print(f"\n✅ Merged annotation file saved at: {save_path}")
