import cv2
import numpy as np
from tensorflow.keras.models import load_model

from ai.config import MODEL_PATH


# -----------------------------
# Load model only once
# -----------------------------
model = load_model(MODEL_PATH)


# -----------------------------
# Class Labels
# -----------------------------
CLASS_NAMES = [
    "A", "B", "C", "D", "E",
    "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y",
    "Z", "del", "nothing", "space"
]


def preprocess_image(image):
    """
    Preprocess image before prediction.
    """

    image = cv2.resize(image, (64, 64))

    image = image.astype("float32") / 255.0

    image = np.expand_dims(image, axis=0)

    return image


def predict(image):
    """
    Predict ASL sign.

    Returns:
        predicted_label
        confidence
    """

    image = preprocess_image(image)

    prediction = model.predict(image, verbose=0)[0]

    class_index = np.argmax(prediction)

    confidence = float(prediction[class_index])

    label = CLASS_NAMES[class_index]

    return label, confidence
