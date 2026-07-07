import cv2
import mediapipe as mp

from ai.landmarks import get_finger_states
from ai.predictor import predict
from ai.assessment import assess_sign

# -----------------------------
# MediaPipe Hands
# -----------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open webcam.")
    exit()

print("Press 'q' to quit.")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        h, w, _ = frame.shape

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            finger_states = get_finger_states(hand_landmarks)

            # -----------------------------
            # Bounding Box
            # -----------------------------
            x_list = []
            y_list = []

            for lm in hand_landmarks.landmark:
                x_list.append(int(lm.x * w))
                y_list.append(int(lm.y * h))

            margin = 40

            x_min = max(min(x_list) - margin, 0)
            y_min = max(min(y_list) - margin, 0)

            x_max = min(max(x_list) + margin, w)
            y_max = min(max(y_list) + margin, h)

            cv2.rectangle(
                frame,
                (x_min, y_min),
                (x_max, y_max),
                (0, 255, 0),
                2
            )

            try:

                wrist = hand_landmarks.landmark[0]

                features = []

                for landmark in hand_landmarks.landmark:

                    features.extend([
                        landmark.x - wrist.x,
                        landmark.y - wrist.y,
                        landmark.z - wrist.z
                    ])

                label, confidence = predict(features)

                expected_sign = "A"

                assessment = assess_sign(
                    expected_sign,
                    label,
                    confidence
                )

                print(assessment)

                if confidence < 0.70:
                    label = "Unknown"

                cv2.putText(
                    frame,
                    f"{label} ({confidence*100:.1f}%)",
                    (x_min, y_min - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,0),
                    2
                )

            except Exception as e:
                print(e)

            cv2.putText(
                frame,
                str(finger_states),
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2
            )

    cv2.imshow("Sign Language Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()
