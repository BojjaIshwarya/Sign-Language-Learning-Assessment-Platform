"""
Learning Progress Intelligence Engine
"""

progress_history = []


def save_progress(sign, assessment):

    progress_history.append({

        "sign": sign,

        "overall_accuracy": assessment["overall_accuracy"],

        "hand_shape": assessment["hand_shape_accuracy"],

        "position": assessment["position_accuracy"],

        "motion": assessment["motion_accuracy"],

        "timing": assessment["timing_accuracy"],

        "movement": assessment["movement_quality"]

    })
    
def get_learning_statistics():

    if not progress_history:
        return None

    accuracies = [
        item["overall_accuracy"]
        for item in progress_history
    ]

    return {

        "total_practice": len(progress_history),

        "average_accuracy": round(
            sum(accuracies) / len(accuracies),
            2
        ),

        "best_accuracy": round(max(accuracies), 2),

        "worst_accuracy": round(min(accuracies), 2)
    }
  
def get_skill_progress():

    if len(progress_history) == 0:
        return "No Practice Yet"

    if len(progress_history) == 1:
        return "First Practice Completed"

    first = progress_history[0]["overall_accuracy"]
    latest = progress_history[-1]["overall_accuracy"]

    difference = latest - first

    if difference >= 10:
        return "Improving"

    elif difference <= -10:
        return "Needs Improvement"

    else:
        return "Stable"
        
def get_weak_area():

    if not progress_history:
        return "No data"

    hand = sum(x["hand_shape"] for x in progress_history) / len(progress_history)

    position = sum(x["position"] for x in progress_history) / len(progress_history)

    motion = sum(x["motion"] for x in progress_history) / len(progress_history)

    timing = sum(x["timing"] for x in progress_history) / len(progress_history)

    movement = sum(x["movement"] for x in progress_history) / len(progress_history)

    scores = {
        "Hand Shape": hand,
        "Position": position,
        "Motion": motion,
        "Timing": timing,
        "Movement": movement
    }

    weakest = min(scores, key=scores.get)

    return weakest
    
def get_recommendation():

    weak = get_weak_area()

    recommendations = {

        "Hand Shape":
            "Practice basic finger positioning exercises.",

        "Position":
            "Practice keeping your hand in the correct position.",

        "Motion":
            "Practice moving your hand in the correct direction.",

        "Timing":
            "Practice maintaining a steady gesture speed.",

        "Movement":
            "Practice smoother hand movements."

    }

    return recommendations.get(
        weak,
        "Keep practicing."
    )
def get_performance_forecast():

    if len(progress_history) < 5:
        return "Practice at least 5 times for prediction."

    avg = sum(
        x["overall_accuracy"]
        for x in progress_history[-5:]
    ) / 5

    if avg >= 90:
        return "Ready for Advanced Level."

    elif avg >= 75:
        return "Ready for Intermediate Level."

    elif avg >= 60:
        return "Keep practicing. You are improving."

    else:
        return "Practice more before taking assessments."
