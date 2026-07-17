"""
Practice Assessment Engine
"""

assessment_questions = [

    "A",
    "B",
    "C",
    "D",
    "E"

]

current_question = 0

assessment_scores = []

assessment_saved = False

exam_completed = False

assessment_reports = []

report_saved = False

def get_current_sign():

    return assessment_questions[current_question]


def next_sign():

    global current_question
    global exam_completed

    if current_question < len(assessment_questions) - 1:

        current_question += 1

    else:

        exam_completed = True

    return get_current_sign()


def assessment_completed():
    return exam_completed
    
def can_move_next():
    global assessment_saved
    return not assessment_saved


def mark_completed():
    global assessment_saved
    assessment_saved = True


def reset_assessment():
    global assessment_saved
    assessment_saved = False
    
def get_question_number():
    return current_question + 1


def get_total_questions():
    return len(assessment_questions)
    
def save_assessment_score(score):

    assessment_scores.append(score)
    
def get_final_score():

    if not assessment_scores:
        return 0

    return round(
        sum(assessment_scores) /
        len(assessment_scores),
        2
    )
    
def get_grade():

    score = get_final_score()

    if score >= 90:
        return "A+"

    elif score >= 80:
        return "A"

    elif score >= 70:
        return "B"

    elif score >= 60:
        return "C"

    elif score >= 50:
        return "D"

    return "F"
    
def get_result():

    if get_final_score() >= 50:
        return "PASS"

    return "FAIL"
    
def reset_exam():

    global current_question
    global exam_completed
    global report_saved

    current_question = 0
    exam_completed = False
    report_saved = False

    assessment_scores.clear()

    reset_assessment()
    
from datetime import datetime

def save_assessment_report():

    global report_saved

    report = {

        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "score": get_final_score(),

        "grade": get_grade(),

        "result": get_result(),

        "questions": len(assessment_questions)

    }

    assessment_reports.append(report)
    
    report_saved = True
    
def get_latest_report():

    if not assessment_reports:
        return None

    return assessment_reports[-1]
    
def report_already_saved():
    return report_saved
