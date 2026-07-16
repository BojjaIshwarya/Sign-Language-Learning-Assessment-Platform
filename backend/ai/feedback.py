"""
AI Feedback & Correction Engine
"""


def generate_feedback(assessment):

    feedback = []

    # -------------------------
    # Correct Sign
    # -------------------------

    if assessment["correct"] and assessment["overall_accuracy"] >= 90:

        feedback.append("Excellent! Correct Sign")
        feedback.append("Outstanding Performance!")
        feedback.append("Proceed to the next lesson.")
        return feedback

    elif assessment["correct"] and assessment["overall_accuracy"] >= 70:

        feedback.append("Good Job!")
        feedback.append("Practice once more to improve accuracy.")
        return feedback

    elif assessment["correct"]:

        feedback.append("Sign recognized.")
        feedback.append("Improve your hand position and movement.")
        return feedback

    # -------------------------
    # Hand Shape
    # -------------------------

    if assessment["hand_shape_accuracy"] < 80:

        feedback.append("Correct your hand shape.")
        feedback.append("Practice finger positioning.")

    # -------------------------
    # Position
    # -------------------------

    if assessment["position_accuracy"] < 80:

        feedback.append("Move your hand to the correct position.")
        feedback.append("Keep your hand near the reference position.")

    # -------------------------
    # Motion
    # -------------------------

    if assessment["motion_accuracy"] < 80:

        feedback.append("Move your hand in the correct direction.")
        feedback.append("Follow the demonstrated movement.")

    # -------------------------
    # Timing
    # -------------------------

    if assessment["timing_accuracy"] < 80:

        feedback.append("Perform the gesture at a better speed.")
        feedback.append("Maintain a steady pace.")

    # -------------------------
    # Movement Quality
    # -------------------------

    if assessment["movement_quality"] < 80:

        feedback.append("Move your hand more smoothly.")
        feedback.append("Avoid sudden or jerky movements.")

    return feedback
def generate_improvement_plan(assessment):

    scores = {
        "Hand Shape": assessment["hand_shape_accuracy"],
        "Position": assessment["position_accuracy"],
        "Motion": assessment["motion_accuracy"],
        "Timing": assessment["timing_accuracy"],
        "Movement": assessment["movement_quality"]
    }

    weakest = min(scores, key=scores.get)

    plans = {
        "Hand Shape": "Practice basic finger shape exercises.",
        "Position": "Practice keeping your hand in the correct position.",
        "Motion": "Practice moving your hand in the correct direction.",
        "Timing": "Practice maintaining a steady gesture speed.",
        "Movement": "Practice smooth and continuous movements."
    }

    return plans[weakest]
