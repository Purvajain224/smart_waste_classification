from pathlib import Path
import random
import shutil

# Location of the original dataset
DATASET_DIR = Path("ml/dataset")

# Classes we want to use
CLASSES = [
    "glass",
    "metal",
    "organic",
    "paper",
    "plastic",
]

# Split percentages
TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15

# Make the split reproducible
RANDOM_SEED = 42

random.seed(RANDOM_SEED)


def split_class(class_name):
    source_dir = DATASET_DIR / class_name

    # Get all JPG images
    images = list(source_dir.glob("*.jpg"))

    if not images:
        print(f"No images found for {class_name}")
        return

    # Shuffle images randomly
    random.shuffle(images)

    total = len(images)

    train_count = int(total * TRAIN_RATIO)
    validation_count = int(total * VALIDATION_RATIO)

    train_images = images[:train_count]
    validation_images = images[
        train_count:train_count + validation_count
    ]
    test_images = images[
        train_count + validation_count:
    ]

    splits = {
        "train": train_images,
        "validation": validation_images,
        "test": test_images,
    }

    for split_name, split_images in splits.items():
        destination_dir = DATASET_DIR / split_name / class_name
        destination_dir.mkdir(parents=True, exist_ok=True)

        for image in split_images:
            shutil.copy2(
                image,
                destination_dir / image.name
            )

    print(
        f"{class_name}: "
        f"{len(train_images)} train, "
        f"{len(validation_images)} validation, "
        f"{len(test_images)} test"
    )


def main():
    print("Starting dataset split...\n")

    for class_name in CLASSES:
        split_class(class_name)

    print("\nDataset split completed successfully.")


if __name__ == "__main__":
    main()