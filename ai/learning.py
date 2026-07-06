import cv2
import random
import mediapipe as mp

from ai.landmarks import get_finger_states
from ai.predictor import predict

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

LETTERS = [
    "A","B","C","D","E",
    "F","G","H","I","J",
    "K","L","M","N","O",
    "P","Q","R","S","T",
    "U","V","W","X","Y","Z"
]

target = random.choice(LETTERS)

score = 0

print("Press 'n' for next letter")
print("Press 'q' to quit")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    cv2.putText(
        frame,
        f"Target : {target}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,255),
        2
    )

    cv2.putText(
        frame,
        f"Score : {score}",
        (20,80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,0),
        2
    )

    if results.multi_hand_landmarks:

        h, w, _ = frame.shape

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            x_list = []
            y_list = []

            for lm in hand_landmarks.landmark:
                x_list.append(int(lm.x*w))
                y_list.append(int(lm.y*h))

            margin = 40

            x_min = max(min(x_list)-margin,0)
            y_min = max(min(y_list)-margin,0)

            x_max = min(max(x_list)+margin,w)
            y_max = min(max(y_list)+margin,h)

            cv2.rectangle(
                frame,
                (x_min,y_min),
                (x_max,y_max),
                (0,255,0),
                2
            )

            hand = frame[y_min:y_max, x_min:x_max]

            if hand.size != 0:

                try:

                    label, confidence = predict(hand)

                    if confidence < 0.70:
                        label = "Unknown"

                    cv2.putText(
                        frame,
                        f"{label} ({confidence*100:.1f}%)",
                        (x_min,y_min-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0,255,0),
                        2
                    )

                    if label == target:

                        cv2.putText(
                            frame,
                            "CORRECT!",
                            (20,130),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0,255,0),
                            3
                        )

                except Exception as e:
                    print(e)

    cv2.imshow("Learning Mode", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("n"):
        target = random.choice(LETTERS)
        score += 1

    elif key == ord("q"):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()
