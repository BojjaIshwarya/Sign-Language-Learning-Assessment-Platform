import joblib
import numpy as np

from ai.config import MODEL_DIR


# -----------------------------
# Load model only once
# -----------------------------
CLASSIFIER_PATH = MODEL_DIR / "landmark_classifier.pkl"
ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"

classifier = joblib.load(CLASSIFIER_PATH)
label_encoder = joblib.load(ENCODER_PATH)

def predict(features):
    """
    Predict ASL sign from landmark features.

    Parameters:
        features : list or numpy array of 63 normalized landmarks
    """

    features = np.array(features).reshape(1, -1)

    prediction = classifier.predict(features)[0]

    probabilities = classifier.predict_proba(features)[0]

    confidence = float(np.max(probabilities))

    label = label_encoder.inverse_transform([prediction])[0]

    return label, confidence
