import cv2
import mediapipe as mp
from collections import Counter, deque
import time

from ai.landmarks import get_finger_states
from ai.predictor import predict
from ai.assessment import assess_sign
from ai.gesture_config import EXPECTED_GESTURE_TIME
from ai.feedback import generate_feedback, generate_improvement_plan
from ai.progress import (
    save_progress,
    get_learning_statistics,
    get_skill_progress,
    get_weak_area,
    get_recommendation,
    get_performance_forecast
)

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

mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open webcam.")
    exit()

print("Press 'q' to quit.")

prediction_buffer = deque(maxlen=3)
movement_buffer = deque(maxlen=10)

expected_sign = "A"

label = None
confidence = 0.0


gesture_start_time = None
gesture_time = 0.0

position_accuracy = 100.0
motion_accuracy = 100.0
timing_accuracy = 100.0
movement_quality = 100.0
gesture_saved = False

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)
    pose_results = pose.process(rgb)

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
                
                if confidence >= 0.70:
                    prediction_buffer.append(label)
                
                if len(prediction_buffer) > 0:
                    label = Counter(prediction_buffer).most_common(1)[0][0]

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
       
    else:
        gesture_saved = False      
    # -----------------------------
    # Draw Pose Landmarks
    # -----------------------------
    if pose_results.pose_landmarks:
        print("Pose Detected")
        mp_draw.draw_landmarks(
            frame,
            pose_results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )
        
        landmarks = pose_results.pose_landmarks.landmark
        print(
            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y
        )

        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        
        h, w, _ = frame.shape

        ls_x = int(left_shoulder.x * w)
        ls_y = int(left_shoulder.y * h)
        
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        
        rs_x = int(right_shoulder.x * w)
        rs_y = int(right_shoulder.y * h)

        lw_x = int(left_wrist.x * w)
        lw_y = int(left_wrist.y * h)

        rw_x = int(right_wrist.x * w)
        rw_y = int(right_wrist.y * h)
        
        movement_buffer.append({
        "left_shoulder": (ls_x, ls_y),
        "right_shoulder": (rs_x, rs_y),
        "left_wrist": (lw_x, lw_y),
        "right_wrist": (rw_x, rw_y)
        })
        
        # Distance between left shoulder and left wrist

        distance = ((lw_x - ls_x) ** 2 + (lw_y - ls_y) ** 2) ** 0.5
        
        MAX_DISTANCE = 250

        position_accuracy = max(
            0,
            100 - (distance / MAX_DISTANCE) * 100
        )

        position_accuracy = round(position_accuracy, 2)
        
        cv2.putText(
            frame,
            f"Position: {position_accuracy:.1f}%",
            (20,200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,0),
            2
        )
        
        if len(movement_buffer) >= 2:
            movement_quality = 100.0

            previous = movement_buffer[-2]
            current = movement_buffer[-1]
            prev_x, prev_y = previous["left_wrist"]
            curr_x, curr_y = current["left_wrist"]
            dx = curr_x - prev_x
            dy = curr_y - prev_y
            direction = "Still"
            expected_direction = "Right"

            if abs(dx) > abs(dy):

                if dx > 5:
                    direction = "Right"

                elif dx < -5:
                    direction = "Left"

            else:

                if dy > 5:
                    direction = "Down"

                elif dy < -5:
                    direction = "Up"
                    
            if direction != "Still" and gesture_start_time is None:
                gesture_start_time = time.time()
                
            if direction == "Still" and gesture_start_time is not None:

                gesture_time = time.time() - gesture_start_time

                gesture_start_time = None
                
            expected_time = EXPECTED_GESTURE_TIME.get(expected_sign, 1.0)

            difference = abs(gesture_time - expected_time)
            
            timing_accuracy = max(
                0,
                100 - (difference / expected_time) * 100
            )

            timing_accuracy = round(timing_accuracy, 2)
                      
            if direction == expected_direction:
                motion_accuracy = 100.0

            elif direction == "Still":
                motion_accuracy = 40.0

            else:
                motion_accuracy = 0.0
                
            cv2.putText(
                frame,
                f"Motion: {motion_accuracy:.1f}%",
                (20, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,255),
                2
            )
            
            cv2.putText(
                frame,
                f"Timing: {timing_accuracy:.1f}%",
                (20, 280),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )
                    
            cv2.putText(
                frame,
                f"Movement: {direction}",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
            
        if len(movement_buffer) >= 5:
        
            changes = []

            for i in range(1, len(movement_buffer)):

                prev = movement_buffer[i-1]["left_wrist"]
                curr = movement_buffer[i]["left_wrist"]

                dx = curr[0] - prev[0]
                dy = curr[1] - prev[1]

                changes.append(abs(dx) + abs(dy))
                
            average_change = sum(changes) / len(changes)

            variation = max(changes) - min(changes)
            
            movement_quality = max(
                0,
                100 - (variation * 0.5)
            )

            movement_quality = round(movement_quality,2)

        cv2.circle(frame, (ls_x, ls_y), 8, (0,0,255), -1)
        
        cv2.putText(
            frame,
            f"Quality: {movement_quality:.1f}%",
            (20,320),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"LS: ({ls_x}, {ls_y})",
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,255),
            2
        )
        
        cv2.putText(
            frame,
            f"Frames Stored: {len(movement_buffer)}",
            (20,120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,0),
            2
        )

        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
        
        if label is not None:
            print("Position:", position_accuracy)
            print("Motion:", motion_accuracy)
            print("Timing:", timing_accuracy)
            print("Quality:", movement_quality)
            assessment = assess_sign(
                expected_sign,
                label,
                confidence,
                position_accuracy=position_accuracy,
                motion_accuracy=motion_accuracy,
                timing_accuracy=timing_accuracy,
                movement_quality=movement_quality
            )
            
            if (
                assessment["correct"]
                and confidence >= 0.80
                and not gesture_saved
            ):


                save_progress(
                    expected_sign,
                    assessment
                )

                gesture_saved = True 
            
            stats = get_learning_statistics()
            progress = get_skill_progress()
            weak_area = get_weak_area()
            recommendation = get_recommendation()
            forecast = get_performance_forecast()
            cv2.putText(
                frame,
                "Forecast:",
                (20, 400),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,255),
                2
            )

            cv2.putText(
                frame,
                forecast,
                (20,430),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255,255,255),
                2
            )
            cv2.putText(
                frame,
                "Recommendation:",
                (20, 340),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,0),
                2
            )

            cv2.putText(
                frame,
                recommendation,
                (20, 370),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255,255,255),
                2
            )
            cv2.putText(
                frame,
                f"Weak Area: {weak_area}",
                (20, 380),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 165, 255),
                2
            )
            cv2.putText(
                frame,
                f"Progress: {progress}",
                (20, 410),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )
            print(stats)

            if stats:

                cv2.putText(

                    frame,

                    f"Avg: {stats['average_accuracy']}%",

                    (20,440),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.6,

                    (255,255,255),

                    2

                )

                cv2.putText(

                    frame,

                    f"Practice: {stats['total_practice']}",

                   (20,470),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.6,

                    (255,255,255),

                    2

                )
            
            feedback = generate_feedback(assessment)
            plan = generate_improvement_plan(assessment)
            cv2.putText(
                frame,
                f"Plan: {plan}",
                (20,500),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )   
            feedback_y = 360

            for message in feedback:
            
                if (
                    "Correct" in message
                    or "Excellent" in message
                    or "Outstanding" in message
                    or "Very Good" in message
                    or "Good Job" in message
                ):
                    color = (0,255,0)
                else:
                    color = (0,0,255)

                cv2.putText(
                    frame,
                    message,
                    (20, feedback_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2
                )

                feedback_y += 30
            for message in feedback:
                print(message)

            print(assessment)


    cv2.imshow("Sign Language Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
hands.close()
pose.close()  
cv2.destroyAllWindows()
