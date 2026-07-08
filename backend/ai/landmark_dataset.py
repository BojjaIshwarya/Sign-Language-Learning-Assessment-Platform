import csv
from pathlib import Path

# Dataset directory
DATASET_DIR = Path(__file__).resolve().parent.parent.parent / "datasets" / "landmarks"
DATASET_DIR.mkdir(parents=True, exist_ok=True)


def save_landmarks(hand_landmarks, label):
    """
    Save one hand landmark sample into a CSV file.

    Each row contains:
    x1,y1,z1,x2,y2,z2,...,x21,y21,z21
    """

    file_path = DATASET_DIR / f"{label}.csv"

    row = []

    for lm in hand_landmarks.landmark:
        row.extend([
            lm.x,
            lm.y,
            lm.z
        ])

    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)

    print(f"Saved sample for {label}")
