import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from binary_data_loader import load_binary_datasets

MODEL_PATH = "ml/model/binary_waste_classifier.keras"

def main():
    _, _, test_dataset = load_binary_datasets()
    model = tf.keras.models.load_model(MODEL_PATH)

    y_true = []
    y_pred = []

    for images, labels in test_dataset:
        predictions = model.predict(images, verbose=0)

        y_true.extend(labels.numpy().flatten().astype(int))
        y_pred.extend((predictions.flatten() >= 0.5).astype(int))

    class_names = ["Inorganic", "Organic"]

    cm = confusion_matrix(y_true, y_pred)

    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=class_names
    )

    display.plot(cmap="Blues", values_format="d")
    plt.title("Binary Waste Classification - Confusion Matrix")
    plt.tight_layout()

    plt.savefig("ml/model/binary_confusion_matrix.png", dpi=300)
    plt.show()

    print("Confusion matrix saved successfully!")

if __name__ == "__main__":
    main()