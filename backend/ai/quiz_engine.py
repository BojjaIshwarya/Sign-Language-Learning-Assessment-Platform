"""
Quiz Engine
"""

quiz_questions = [

    {
        "question": "Which finger is used most in sign A?",
        "options": ["Thumb", "Index", "Little", "All Fingers"],
        "answer": "Thumb"
    },

    {
        "question": "Which sign language is this platform based on?",
        "options": ["ASL", "ISL", "BSL", "JSL"],
        "answer": "ASL"
    },

    {
        "question": "Why is hand position important?",
        "options": [
            "Recognition",
            "Decoration",
            "Color",
            "Brightness"
        ],
        "answer": "Recognition"
    }

]

current_quiz = 0
score = 0

def get_question():

    return quiz_questions[current_quiz]


def check_answer(answer):

    global score

    if answer == quiz_questions[current_quiz]["answer"]:
        score += 1
        return True

    return False


def next_question():

    global current_quiz

    if current_quiz < len(quiz_questions)-1:
        current_quiz += 1


def quiz_completed():

    return current_quiz == len(quiz_questions)-1


def get_score():

    return score


def reset_quiz():

    global current_quiz
    global score

    current_quiz = 0
    score = 0
