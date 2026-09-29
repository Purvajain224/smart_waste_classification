import os
import io

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image


MODEL_PATH = "ml/model/waste_classifier_best.keras"

IMG_SIZE = (224, 224)

CLASS_NAMES = [
    "glass",
    "metal",
    "organic",
    "paper",
    "plastic",
]

BIN_RECOMMENDATIONS = {
    "glass": "Glass / Recyclable Bin",
    "metal": "Metal / Recyclable Bin",
    "organic": "Organic / Compost Bin",
    "paper": "Paper / Dry Waste Bin",
    "plastic": "Plastic / Recyclable Bin",
}


app = FastAPI(
    title="Smart Waste Classification API",
    description="API for classifying waste images using a trained MobileNetV2 model.",
    version="1.0.0",
)


# Allow the React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load the trained model once when the API starts
model = None


@app.on_event("startup")
def load_model():
    global model

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Trained model not found at: {MODEL_PATH}"
        )

    model = tf.keras.models.load_model(MODEL_PATH)


@app.get("/")
def root():
    return {
        "message": "Smart Waste Classification API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_data = await file.read()

    image = Image.open(
        io.BytesIO(image_data)
    ).convert("RGB")

    image = image.resize(IMG_SIZE)

    image_array = np.array(
        image,
        dtype=np.float32
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    predictions = model.predict(
        image_array,
        verbose=0
    )

    predicted_index = int(
        np.argmax(predictions[0])
    )

    predicted_class = CLASS_NAMES[predicted_index]

    confidence = float(
        predictions[0][predicted_index]
    ) * 100

    return {
        "category": predicted_class,
        "confidence": round(confidence, 2),
        "recommended_bin": BIN_RECOMMENDATIONS[predicted_class],
    }