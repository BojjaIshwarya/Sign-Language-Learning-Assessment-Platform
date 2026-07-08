"""
Sign Accuracy Assessment Engine
"""

def assess_sign(expected_label, predicted_label, confidence):
    """
    Compare expected and predicted sign.

    Returns:
        {
            "expected": ...,
            "predicted": ...,
            "correct": ...,
            "confidence": ...,
            "score": ...
        }
    """

    correct = expected_label.upper() == predicted_label.upper()

    if correct:
        score = round(confidence * 100, 2)
    else:
        score = 0.0

    return {
        "expected": expected_label,
        "predicted": predicted_label,
        "correct": correct,
        "confidence": round(confidence * 100, 2),
        "score": score
    }
