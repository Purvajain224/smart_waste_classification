import os
import shutil
from pathlib import Path

import numpy as np
import tensorflow as tf

from binary_data_loader import load_binary_datasets


MODEL_PATH = "ml/model/binary_waste_classifier.keras"
TEST_DIR = "ml/binary_dataset/test"
OUTPUT_DIR = "ml/model/misclassified_test_images"

CLASS_NAMES = ["Inorganic", "Organic"]


def main():
    print("Loading test dataset...")
    _, _, test_dataset = load_binary_datasets()

    print("\nLoading trained model...")
    model = tf.keras.models.load_model(MODEL_PATH)

    print("\nGenerating predictions...")
    predictions = model.predict(test_dataset, verbose=0).flatten()

    y_true = np.concatenate([
        labels.numpy().flatten().astype(int)
        for _, labels in test_dataset
    ])

    y_pred = (predictions >= 0.5).astype(int)

    # Match the alphabetical class-folder and filename order
    image_paths = sorted(
        str(path)
        for path in Path(TEST_DIR).glob("*/*")
        if path.suffix.lower() in [".jpg", ".jpeg", ".png"]
    )

    if len(image_paths) != len(y_true):
        raise ValueError(
            f"Image count ({len(image_paths)}) does not match "
            f"test labels ({len(y_true)}). Check TEST_DIR."
        )

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    error_count = 0

    for index, (actual, predicted) in enumerate(zip(y_true, y_pred)):
        if actual == predicted:
            continue

        error_count += 1

        actual_name = CLASS_NAMES[actual]
        predicted_name = CLASS_NAMES[predicted]

        confidence = (
            predictions[index]
            if predicted == 1
            else 1 - predictions[index]
        )

        original_path = image_paths[index]
        filename = os.path.basename(original_path)

        new_filename = (
            f"{error_count:03d}_actual-{actual_name}"
            f"_predicted-{predicted_name}"
            f"_confidence-{confidence:.2f}_{filename}"
        )

        destination = os.path.join(OUTPUT_DIR, new_filename)
        shutil.copy2(original_path, destination)

        print(
            f"{error_count}. Actual: {actual_name} | "
            f"Predicted: {predicted_name} | "
            f"Confidence: {confidence:.2f}"
        )

    print(f"\nTotal incorrect predictions: {error_count}")
    print(f"Images copied to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()