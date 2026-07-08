import joblib
import pandas as pd
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from config import MODEL_DIR

DATASET_PATH = Path(__file__).parent / "landmarks.csv"

dataset = pd.read_csv(DATASET_PATH)

print(dataset.head())

print(dataset.shape)

X = dataset.drop("label", axis=1)

y = dataset["label"]

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"Training Samples : {len(X_train)}")
print(f"Testing Samples  : {len(X_test)}")

classifier = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

print("\nTraining Random Forest...")

classifier.fit(X_train, y_train)

print("Training Completed!")

predictions = classifier.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"\nAccuracy: {accuracy * 100:.2f}%")

MODEL_PATH = MODEL_DIR / "landmark_classifier.pkl"
ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"

joblib.dump(classifier, MODEL_PATH)
joblib.dump(label_encoder, ENCODER_PATH)

print(f"Model saved to: {MODEL_PATH}")
print(f"Label encoder saved to: {ENCODER_PATH}")
