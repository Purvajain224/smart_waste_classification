import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

from binary_data_loader import load_binary_datasets

MODEL_PATH = "ml/model/binary_waste_classifier.keras"


def main():
    print("Loading test dataset...")
    _, _, test_dataset = load_binary_datasets()

    print("Loading saved model...")
    model = tf.keras.models.load_model(MODEL_PATH)

    print("\nEvaluating model...")
    loss, accuracy = model.evaluate(test_dataset)

    print(f"\nTest Loss: {loss:.4f}")
    print(f"Test Accuracy: {accuracy * 100:.2f}%")

    print("\nGenerating predictions...")
    y_true = []
    y_pred = []

    for images, labels in test_dataset:
        predictions = model.predict(images, verbose=0)

        y_true.extend(labels.numpy().flatten().astype(int))
        y_pred.extend((predictions.flatten() >= 0.5).astype(int))

    class_names = ["Inorganic", "Organic"]

    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=class_names))

    print("Confusion Matrix:")
    print(confusion_matrix(y_true, y_pred))


if __name__ == "__main__":
    main()