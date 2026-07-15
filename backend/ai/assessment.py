"""
Sign Accuracy Assessment Engine
"""


def assess_sign(
    expected_label,
    predicted_label,
    confidence,
    hand_shape_accuracy=None,
    position_accuracy=None,
    motion_accuracy=None,
    timing_accuracy=None,
    movement_quality=None
):
    """
    Advanced Sign Assessment
    """

    correct = expected_label.upper() == predicted_label.upper()

    confidence = round(confidence * 100, 2)

    # -----------------------------
    # Hand Shape Accuracy
    # -----------------------------
    if hand_shape_accuracy is None:
        if correct:
            hand_shape_accuracy = confidence
        else:
            hand_shape_accuracy = 0.0

    # -----------------------------
    # Position Accuracy
    # -----------------------------
    if position_accuracy is None:
        position_accuracy = 100.0

    # -----------------------------
    # Motion Accuracy
    # -----------------------------
    if motion_accuracy is None:
        motion_accuracy = 100.0

    # -----------------------------
    # Timing Accuracy
    # -----------------------------
    if timing_accuracy is None:
        timing_accuracy = 100.0
        
    if movement_quality is None:
        movement_quality = 100.0

    # -----------------------------
    # Overall Accuracy
    # -----------------------------
    overall_accuracy = round(
        (
            hand_shape_accuracy +
            position_accuracy +
            motion_accuracy +
            timing_accuracy +
            movement_quality
        ) / 5,
        2
    )

    return {

        "expected": expected_label,

        "predicted": predicted_label,

        "correct": correct,

        "confidence": confidence,

        "hand_shape_accuracy": hand_shape_accuracy,

        "position_accuracy": position_accuracy,

        "motion_accuracy": motion_accuracy,

        "timing_accuracy": timing_accuracy,

        "overall_accuracy": overall_accuracy,
        
        "movement_quality": movement_quality

    }
