"""
Certification Engine
"""

def generate_certificate(
    assessment_score,
    quiz_score,
    total_questions
):

    quiz_percentage = (
        quiz_score / total_questions
    ) * 100

    final_score = round(
        (assessment_score + quiz_percentage) / 2,
        2
    )

    if final_score >= 80:

        return {
            "eligible": True,
            "certificate": "CERTIFIED",
            "final_score": final_score
        }

    return {
        "eligible": False,
        "certificate": "NOT ELIGIBLE",
        "final_score": final_score
    }
