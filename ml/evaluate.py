import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

from data_loader import load_datasets

MODEL_PATH = "ml/model/waste_classifier_best.keras"


def main():
    print("Loading test dataset...")
    _, _, test_dataset = load_datasets()

    print("Loading trained model...")
    model = tf.keras.models.load_model(MODEL_PATH)

    print("\nEvaluating model...")
    test_loss, test_accuracy = model.evaluate(test_dataset, verbose=1)

    print("\nTest Results")
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

    print("\nGenerating predictions...")

    y_true = np.concatenate([labels.numpy() for _, labels in test_dataset])
    predictions = model.predict(test_dataset, verbose=1)
    y_pred = np.argmax(predictions, axis=1)

    class_names = test_dataset.class_names

    print("\nClassification Report")
    print(
        classification_report(
            y_true,
            y_pred,
            target_names=class_names,
            digits=4
        )
    )

    print("Confusion Matrix")
    print(confusion_matrix(y_true, y_pred))


if __name__ == "__main__":
    main()