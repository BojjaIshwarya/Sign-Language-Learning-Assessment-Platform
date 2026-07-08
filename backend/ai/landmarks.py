import mediapipe as mp

mp_hands = mp.solutions.hands


def get_finger_states(hand_landmarks):
    landmarks = hand_landmarks.landmark

    fingers = []

    # Thumb
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Index
    fingers.append(
        1 if landmarks[8].y < landmarks[6].y else 0
    )

    # Middle
    fingers.append(
        1 if landmarks[12].y < landmarks[10].y else 0
    )

    # Ring
    fingers.append(
        1 if landmarks[16].y < landmarks[14].y else 0
    )

    # Pinky
    fingers.append(
        1 if landmarks[20].y < landmarks[18].y else 0
    )

    return fingers
