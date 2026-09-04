import sys
import numpy as np
import tensorflow as tf
from PIL import Image

MODEL_PATH = "ml/model/waste_classifier_best.keras"

IMG_SIZE = (224, 224)

CLASS_NAMES = [
    "glass",
    "metal",
    "organic",
    "paper",
    "plastic"
]

BIN_RECOMMENDATIONS = {
    "glass": "Glass / Recyclable Bin",
    "metal": "Metal / Recyclable Bin",
    "organic": "Organic / Compost Bin",
    "paper": "Paper / Dry Waste Bin",
    "plastic": "Plastic / Recyclable Bin"
}


def predict_image(image_path):
    # Load trained model
    model = tf.keras.models.load_model(MODEL_PATH)

    # Open image
    image = Image.open(image_path).convert("RGB")

    # Resize image to the model's expected input size
    image = image.resize(IMG_SIZE)

    # Convert image to NumPy array
    image_array = np.array(image, dtype=np.float32)

    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)

    # Make prediction
    predictions = model.predict(image_array, verbose=0)

    # Find class with highest probability
    predicted_index = np.argmax(predictions[0])
    predicted_class = CLASS_NAMES[predicted_index]

    # Convert probability to percentage
    confidence = float(predictions[0][predicted_index]) * 100

    # Get recommended bin
    recommended_bin = BIN_RECOMMENDATIONS[predicted_class]

    return predicted_class, confidence, recommended_bin


def main():
    if len(sys.argv) != 2:
        print("Usage: python ml/predict.py <image_path>")
        return

    image_path = sys.argv[1]

    try:
        predicted_class, confidence, recommended_bin = predict_image(
            image_path
        )

        print("\nPrediction Result")
        print("-----------------")
        print(f"Category: {predicted_class.capitalize()}")
        print(f"Confidence: {confidence:.2f}%")
        print(f"Recommended Bin: {recommended_bin}")

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()