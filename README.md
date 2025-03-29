# 🧠 COCO Annotation Merger - GUI Tool

**Author:** Yael Vicente  
**Last Updated:** March 2025  
**License:** MIT

---

## 🧾 Description

**COCO Annotation Merger** is a desktop application with a graphical interface (GUI) that allows users to merge annotation files formatted in the [COCO dataset format](https://cocodataset.org/#format-data).  

This tool is especially useful for combining machine learning datasets in object detection, instance segmentation, and annotation tasks.

### Features

✅ Merge multiple JSON files with the **same categories**  
✅ Merge two files with **different categories** (e.g., strawberries + flowers)  
✅ Merge all JSONs from two folders (e.g., for different annotation types)  
✅ Automatically handle unique image/annotation IDs  
✅ Prevent category ID conflicts  
✅ Show per-category annotation stats after merging  
✅ Intuitive, beginner-friendly **Tkinter GUI**

---

## 📸 Screenshot

![COCO Annotation Merger GUI](assets/screenshot.png)

> Preview of the interface (light theme, blue palette, multi-task options)

---

## 📂 Project Structure

```
COCO_Annotation_Merger/
├── assets/                           # Logo and image resources
│   ├── logo.ico                      # Icon for app window
│   └── logo.png                      # GUI/logo image
├── gui_components/                   # GUI panels per task
│   ├── task_selector.py              # Task selection interface
│   ├── task_merger_single.py         # Merge multiple (same category)
│   ├── task_merger_dual.py           # Merge 2 files (different categories)
│   └── task_merger_multi.py          # Merge all from two folders
├── scripts/                          # Backend logic (POO)
│   ├── coco_annotation_merger.py
│   ├── strawberry_flower_annotation.py
│   └── strawberry_flower_annotations_combiner.py
├── main.py                           # Entry point of the GUI app
├── requirements.txt                  # Python dependencies
└── README.md                         # You are here 📘
```

---

## 🚀 Installation & Usage

Follow these steps to install and run the app.

### 1. 🧬 Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/COCO_Annotation_Merger.git
cd COCO_Annotation_Merger
```

### 2. 🐍 Create a Virtual Environment (Optional but Recommended)

```bash
# Linux/macOS
python3 -m venv env_gui
source env_gui/bin/activate

# Windows
python -m venv env_gui
env_gui\Scripts\activate
```

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. ▶️ Run the App

```bash
python main.py
```

The GUI should launch automatically.

---

## 🧠 How It Works

### 🔹 Mode 1: Merge Multiple JSONs with Same Categories

- Use when all annotation files have the same category IDs and names.
- Automatically resolves image/annotation ID conflicts.

### 🔹 Mode 2: Merge Two JSONs with Different Categories

- For example, one JSON for `fruit_ripe`/`fruit_unripe`, and another for `flower`.
- The app will reassign the flower category ID to avoid overlaps.

### 🔹 Mode 3: Merge All Files from Two Folders

- You select two folders (strawberries and flowers).
- Each file is associated by image filename and merged.
- Outputs a unified COCO JSON with updated IDs and categories.

---

## 📊 Statistics Output

After merging, the app displays:

- Total number of images merged 🖼️  
- Total number of annotations 🏷️  
- Category-wise annotation counts with names and IDs 📚

---

## 🧰 Future Features (Coming Soon)

✅ Compute **IoU (Intersection over Union)** between annotations  
✅ Evaluate **Fleiss' Kappa** inter-annotator agreement  
✅ Add support for **instance masks**  
✅ Export annotations to other formats (Pascal VOC, YOLOv8, etc.)  
✅ Dark mode theme 🌑  
✅ Drag-and-drop folders support 🖱️  

---

## 🪟 App Icon

The app uses a custom logo:

```bash
assets/logo.ico   # Used as GUI window icon
```

To change the logo:
- Replace `logo.ico` in the `assets/` folder
- Use `.ico` format for compatibility on Windows

---

## 🧑‍💻 Maintainer

**Yael Vicente**  
Director Nacional - IAAS México  
B.Sc. in Agricultural Mechatronics Engineering (7th Semester)  
March 2025

📫 Email: yael@example.com (replace with your actual contact)

---

## 📄 License

This project is licensed under the **MIT License**.  
Feel free to fork, extend, or contribute.

---

> ⭐ If this project helped you, please consider giving it a star and sharing it with others working with COCO annotations!
