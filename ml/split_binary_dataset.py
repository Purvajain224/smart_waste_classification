import random
import shutil
from pathlib import Path

# Dataset locations
DATASET_DIR = Path("ml/binary_dataset")
CLASSES = ["Organic", "Inorganic"]

# Split ratios
TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15

# Reproducible split
random.seed(42)

# Supported image formats
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

for class_name in CLASSES:
    source_dir = DATASET_DIR / class_name
    images = [
        file for file in source_dir.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    ]

    random.shuffle(images)

    total = len(images)
    train_count = int(total * TRAIN_RATIO)
    validation_count = int(total * VALIDATION_RATIO)

    splits = {
        "train": images[:train_count],
        "validation": images[train_count:train_count + validation_count],
        "test": images[train_count + validation_count:]
    }

    for split_name, split_images in splits.items():
        destination_dir = DATASET_DIR / split_name / class_name
        destination_dir.mkdir(parents=True, exist_ok=True)

        for image in split_images:
            shutil.copy2(image, destination_dir / image.name)

        print(f"{class_name} - {split_name}: {len(split_images)} images")

print("\nDataset splitting completed!")