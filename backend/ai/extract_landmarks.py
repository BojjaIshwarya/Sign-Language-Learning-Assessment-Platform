import os
import csv
import cv2
import mediapipe as mp
from pathlib import Path

from config import ASL_TRAIN

# -----------------------------
# MediaPipe Hands
# -----------------------------
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
)

OUTPUT_CSV = Path(__file__).parent / "landmarks.csv"

classes = sorted(os.listdir(ASL_TRAIN))

header = []

for i in range(21):
    header.extend([
        f"x{i}",
        f"y{i}",
        f"z{i}"
    ])

header.append("label")

saved = 0
skipped = 0

skipped_files = []

with open(OUTPUT_CSV, "w", newline="") as csv_file:

    writer = csv.writer(csv_file)

    writer.writerow(header)
    
    for label in classes:
    
        class_path = os.path.join(ASL_TRAIN, label)

        if not os.path.isdir(class_path):
            continue
            
        image_files = [
            f for f in os.listdir(class_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        total_images = len(image_files)
        processed = 0


        print(f"\nProcessing {label} ({total_images} images)")  
        
        for filename in image_files:
            
            processed += 1

            if processed % 200 == 0:
                print(f"{label}: {processed}/{total_images}")

            image_path = os.path.join(class_path, filename)
            
            image = cv2.imread(image_path)

            if image is None:
                skipped += 1
                skipped_files.append(image_path)
                continue
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)
            if not results.multi_hand_landmarks:

                skipped += 1
                skipped_files.append(image_path)

                continue
            hand_landmarks = results.multi_hand_landmarks[0]
            wrist = hand_landmarks.landmark[0]

            features = []

            for landmark in hand_landmarks.landmark:

                features.extend([
                    landmark.x - wrist.x,
                    landmark.y - wrist.y,
                    landmark.z - wrist.z
                ])
            features.append(label)
            writer.writerow(features)

            saved += 1
print("\nExtraction Completed")
print(f"Saved Samples   : {saved}")
print(f"Skipped Samples : {skipped}")

SKIPPED_LOG = Path(__file__).parent / "skipped_images.txt"

with open(SKIPPED_LOG, "w") as log:

    for file in skipped_files:
        log.write(f"{file}\n")

print(f"Skipped image list saved to: {SKIPPED_LOG}")
print(f"CSV saved to: {OUTPUT_CSV}")
print(f"Skipped log saved to: {SKIPPED_LOG}")

hands.close()
