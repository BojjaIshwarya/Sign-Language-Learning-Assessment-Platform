import cv2
import mediapipe as mp
import time

from ai.landmark_dataset import save_landmarks

# -----------------------------
# MediaPipe
# -----------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# -----------------------------
# Webcam
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open webcam.")
    exit()

current_label = "A"

recording = False
samples_saved = 0
target_samples = 300

last_save_time = 0
save_interval = 0.05  # Save every 50 ms

print("--------------------------------")
print("Landmark Dataset Collector")
print("--------------------------------")
print("A-Z : Change Label")
print("R   : Start Recording")
print("T   : Stop Recording")
print("Q   : Quit")
print("--------------------------------")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    # Display information
    cv2.putText(
        frame,
        f"Label : {current_label}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Samples : {samples_saved}/{target_samples}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    status = "RECORDING" if recording else "IDLE"

    color = (0, 0, 255) if recording else (255, 255, 255)

    cv2.putText(
        frame,
        status,
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        color,
        2
    )

    if results.multi_hand_landmarks:

        hand_landmarks = results.multi_hand_landmarks[0]

        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        if recording:

            current_time = time.time()

            if current_time - last_save_time >= save_interval:

                save_landmarks(hand_landmarks, current_label)

                samples_saved += 1

                last_save_time = current_time

                if samples_saved >= target_samples:
                    recording = False
                    print(f"{current_label} completed!")

    cv2.imshow("Landmark Collector", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break

    # SPACE starts recording
    elif key == 32:
        recording = True
        samples_saved = 0
        print(f"Recording {current_label}...")

    # BACKSPACE stops recording
    elif key == 8:
        recording = False
        print("Recording stopped.")

    elif ord("a") <= key <= ord("z"):
        current_label = chr(key).upper()
        recording = False
        samples_saved = 0
        print(f"Current label: {current_label}")

cap.release()
hands.close()
cv2.destroyAllWindows()
