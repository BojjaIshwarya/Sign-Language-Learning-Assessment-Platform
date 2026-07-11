from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, schemas
from app.security import hash_password, verify_password


# ==========================================
# USER AUTHENTICATION
# ==========================================

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(
        models.User.email == email
    ).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(
        models.User.id == user_id
    ).first()


def create_user(db: Session, user: schemas.UserCreate):

    hashed_password = hash_password(user.password)

    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Automatically create learner profile
    if db_user.role == "Learner":

        learner_profile = models.LearnerProfile(
            user_id=db_user.id,
            learning_level="Beginner",
            preferred_language="English"
        )

        db.add(learner_profile)
        db.commit()

    return db_user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = get_user_by_email(db, email)

    if user is None:
        return None

    if not verify_password(password, user.password):
        return None

    return user


# ==========================================
# USER PROFILE MANAGEMENT
# ==========================================

def update_user_profile(
    db: Session,
    current_user,
    user_data: schemas.UserUpdate
):

    db_user = db.query(models.User).filter(
        models.User.id == current_user.id
    ).first()

    if db_user is None:
        return None

    db_user.name = user_data.name
    db_user.email = user_data.email

    db.commit()
    db.refresh(db_user)

    return db_user


def change_password(
    db: Session,
    current_user,
    password_data: schemas.ChangePassword
):

    db_user = db.query(models.User).filter(
        models.User.id == current_user.id
    ).first()

    if db_user is None:
        return None

    if not verify_password(
        password_data.current_password,
        db_user.password
    ):
        return None

    db_user.password = hash_password(
        password_data.new_password
    )

    db.commit()
    db.refresh(db_user)

    return db_user


# ==========================================
# LEARNER PROFILE MANAGEMENT
# ==========================================

def create_learner_profile(
    db: Session,
    current_user,
    profile: schemas.LearnerProfileCreate
):

    existing = db.query(models.LearnerProfile).filter(
        models.LearnerProfile.user_id == current_user.id
    ).first()

    if existing:
        return None

    learner_profile = models.LearnerProfile(
    user_id=current_user.id,
    learning_level=profile.learning_level,
    preferred_language=profile.preferred_language
    )

    db.add(learner_profile)
    db.commit()
    db.refresh(learner_profile)

    return learner_profile


def get_learner_profile(
    db: Session,
    current_user
):

    return db.query(models.LearnerProfile).filter(
        models.LearnerProfile.user_id == current_user.id
    ).first()


def update_learner_profile(
    db: Session,
    current_user,
    profile: schemas.LearnerProfileUpdate
):

    learner = db.query(models.LearnerProfile).filter(
        models.LearnerProfile.user_id == current_user.id
    ).first()

    if learner is None:
        return None
        
    if profile.learning_level is not None:
        learner.learning_level = profile.learning_level

    if profile.preferred_language is not None:
        learner.preferred_language = profile.preferred_language

    db.commit()
    db.refresh(learner)

    return learner


def get_practice_history(
    db: Session,
    current_user
):

    learner = get_learner_profile(db, current_user)

    if learner is None:
        return []

    return learner.practice_history


def get_assessment_history(
    db: Session,
    current_user
):

    learner = get_learner_profile(db, current_user)

    if learner is None:
        return []

    return learner.assessment_history
    
def create_learning_goal(db: Session, current_user, goal: schemas.LearningGoalCreate):

    learner = get_learner_profile(db, current_user)

    if not learner:
        return None

    db_goal = models.LearningGoal(
        learner_profile_id=learner.id,
        goal_title=goal.goal_title,
        description=goal.description,
        status="Pending"
    )

    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)

    return db_goal
    
def get_learning_goals(db: Session, current_user):

    learner = get_learner_profile(db, current_user)

    if not learner:
        return []

    return db.query(models.LearningGoal).filter(
        models.LearningGoal.learner_profile_id == learner.id
    ).all()
    
def update_learning_goal(db: Session, current_user, goal_id: int, goal: schemas.LearningGoalUpdate):

    learner = get_learner_profile(db, current_user)

    db_goal = db.query(models.LearningGoal).filter(
        models.LearningGoal.id == goal_id,
        models.LearningGoal.learner_profile_id == learner.id
    ).first()

    if not db_goal:
        return None

    if goal.goal_title is not None:
        db_goal.goal_title = goal.goal_title

    if goal.description is not None:
        db_goal.description = goal.description

    if goal.status is not None:
        db_goal.status = goal.status

    db.commit()
    db.refresh(db_goal)

    return db_goal
    
def delete_learning_goal(
    db: Session,
    current_user,
    goal_id: int
):

    learner = get_learner_profile(db, current_user)

    if learner is None:
        return None

    goal = db.query(models.LearningGoal).filter(
        models.LearningGoal.id == goal_id,
        models.LearningGoal.learner_profile_id == learner.id
    ).first()

    if goal is None:
        return None

    db.delete(goal)
    db.commit()

    return True
    
def create_skill(db: Session, current_user, skill: schemas.SkillCreate):

    learner = get_learner_profile(db, current_user)

    if learner is None:
        return None

    db_skill = models.Skill(
        learner_profile_id=learner.id,
        skill_name=skill.skill_name,
        skill_level=skill.skill_level,
        mastery_percentage=skill.mastery_percentage
    )

    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)

    return db_skill
    
def get_skills(db: Session, current_user):

    learner = get_learner_profile(db, current_user)

    return db.query(models.Skill).filter(
        models.Skill.learner_profile_id == learner.id
    ).all()
    
def update_skill(db: Session, current_user, skill_id: int, skill: schemas.SkillUpdate):

    learner = get_learner_profile(db, current_user)

    db_skill = db.query(models.Skill).filter(
        models.Skill.id == skill_id,
        models.Skill.learner_profile_id == learner.id
    ).first()

    if not db_skill:
        return None

    if skill.skill_level is not None:
        db_skill.skill_level = skill.skill_level

    if skill.mastery_percentage is not None:
        db_skill.mastery_percentage = skill.mastery_percentage

    db.commit()
    db.refresh(db_skill)

    return db_skill
    
# ==========================================
# DELETE SKILL
# ==========================================

def delete_skill(db: Session, current_user, skill_id: int):

    learner = get_learner_profile(db, current_user)

    if learner is None:
        return False

    skill = db.query(models.Skill).filter(
        models.Skill.id == skill_id,
        models.Skill.learner_profile_id == learner.id
    ).first()

    if skill is None:
        return False

    db.delete(skill)
    db.commit()

    return True
    
# ==========================================
# COURSE MANAGEMENT
# ==========================================

def create_course(
    db: Session,
    current_user,
    course: schemas.CourseCreate
):

    db_course = models.Course(
        title=course.title,
        description=course.description,
        category=course.category,
        level=course.level,
        created_by=current_user.id
    )

    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course


def get_all_courses(db: Session):

    return db.query(models.Course).all()


def get_course_by_id(
    db: Session,
    course_id: int
):

    return db.query(models.Course).filter(
        models.Course.id == course_id
    ).first()


def update_course(
    db: Session,
    course_id: int,
    course: schemas.CourseUpdate
):

    db_course = get_course_by_id(
        db,
        course_id
    )

    if db_course is None:
        return None

    if course.title is not None:
        db_course.title = course.title

    if course.description is not None:
        db_course.description = course.description

    if course.category is not None:
        db_course.category = course.category

    if course.level is not None:
        db_course.level = course.level

    db.commit()
    db.refresh(db_course)

    return db_course


def delete_course(
    db: Session,
    course_id: int
):

    db_course = get_course_by_id(
        db,
        course_id
    )

    if db_course is None:
        return None

    db.delete(db_course)
    db.commit()

    return db_course

# ==========================================
# CREATE PRACTICE HISTORY
# ==========================================

def create_practice_history(
    db: Session,
    current_user,
    practice: schemas.PracticeHistoryCreate
):

    learner = get_learner_profile(db, current_user)

    if learner is None:
        return None

    db_practice = models.PracticeHistory(
        learner_profile_id=learner.id,
        lesson_name=practice.lesson_name,
        score=practice.score,
        duration=practice.duration
    )

    db.add(db_practice)
    db.commit()
    db.refresh(db_practice)

    return db_practice
    
# ==========================================
# CREATE ASSESSMENT HISTORY
# ==========================================

def create_assessment_history(
    db: Session,
    current_user,
    assessment: schemas.AssessmentHistoryCreate
):

    learner = get_learner_profile(db, current_user)

    if learner is None:
        return None

    db_assessment = models.AssessmentHistory(
        learner_profile_id=learner.id,
        assessment_name=assessment.assessment_name,
        score=assessment.score,
        level=assessment.level
    )

    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    
    notify_user(
        db,
        current_user.id,
        "Assessment Completed",
        f"You scored {assessment.score}% in {assessment.assessment_name}."
    )

    return db_assessment
    
def create_lesson(db: Session, course_id: int, lesson: schemas.LessonCreate):

    course = db.query(models.Course).filter(
        models.Course.id == course_id
    ).first()

    if not course:
        return None

    db_lesson = models.Lesson(
        course_id=course_id,
        title=lesson.title,
        description=lesson.description,
        lesson_order=lesson.lesson_order
    )

    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)

    return db_lesson
    
def get_lessons_by_course(db: Session, course_id: int):

    return db.query(models.Lesson).filter(
        models.Lesson.course_id == course_id
    ).order_by(
        models.Lesson.lesson_order
    ).all()
    
def get_lesson(db: Session, lesson_id: int):

    return db.query(models.Lesson).filter(
        models.Lesson.id == lesson_id
    ).first()
    
def update_lesson(
    db: Session,
    lesson_id: int,
    lesson: schemas.LessonUpdate
):

    db_lesson = get_lesson(db, lesson_id)

    if not db_lesson:
        return None

    update_data = lesson.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_lesson, key, value)

    db.commit()
    db.refresh(db_lesson)

    return db_lesson
    
def delete_lesson(db: Session, lesson_id: int):

    lesson = get_lesson(db, lesson_id)

    if not lesson:
        return False

    db.delete(lesson)
    db.commit()

    return True
    
def create_module(
    db: Session,
    course_id: int,
    module: schemas.ModuleCreate
):

    course = db.query(models.Course).filter(
        models.Course.id == course_id
    ).first()

    if not course:
        return None

    db_module = models.CourseModule(
        course_id=course_id,
        title=module.title,
        description=module.description,
        module_order=module.module_order
    )

    db.add(db_module)
    db.commit()
    db.refresh(db_module)

    return db_module
    
def get_modules_by_course(
    db: Session,
    course_id: int
):

    return db.query(models.CourseModule).filter(
        models.CourseModule.course_id == course_id
    ).order_by(
        models.CourseModule.module_order
    ).all()
    
def get_module(
    db: Session,
    module_id: int
):

    return db.query(models.CourseModule).filter(
        models.CourseModule.id == module_id
    ).first()
    
def update_module(
    db: Session,
    module_id: int,
    module: schemas.ModuleUpdate
):

    db_module = get_module(db, module_id)

    if not db_module:
        return None

    update_data = module.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_module, key, value)

    db.commit()
    db.refresh(db_module)

    return db_module
    
def delete_module(
    db: Session,
    module_id: int
):

    db_module = get_module(db, module_id)

    if not db_module:
        return False

    db.delete(db_module)
    db.commit()

    return True
    
def create_lesson_content(
    db: Session,
    lesson_id: int,
    content: schemas.LessonContentCreate
):

    lesson = db.query(models.Lesson).filter(
        models.Lesson.id == lesson_id
    ).first()

    if not lesson:
        return None

    db_content = models.LessonContent(
        lesson_id=lesson_id,
        title=content.title,
        content_type=content.content_type,
        content_url=content.content_url,
        description=content.description
    )

    db.add(db_content)
    db.commit()
    db.refresh(db_content)

    return db_content
    
def get_lesson_contents(
    db: Session,
    lesson_id: int
):

    return db.query(models.LessonContent).filter(
        models.LessonContent.lesson_id == lesson_id
    ).all()
    
def get_lesson_content(
    db: Session,
    content_id: int
):

    return db.query(models.LessonContent).filter(
        models.LessonContent.id == content_id
    ).first()
    
def update_lesson_content(
    db: Session,
    content_id: int,
    content: schemas.LessonContentUpdate
):

    db_content = get_lesson_content(db, content_id)

    if not db_content:
        return None

    update_data = content.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_content, key, value)

    db.commit()
    db.refresh(db_content)

    return db_content
    
def delete_lesson_content(
    db: Session,
    content_id: int
):

    db_content = get_lesson_content(db, content_id)

    if not db_content:
        return False

    db.delete(db_content)
    db.commit()

    return True
    
def create_learning_path(
    db: Session,
    path: schemas.LearningPathCreate
):

    db_path = models.LearningPath(
        title=path.title,
        description=path.description
    )

    db.add(db_path)
    db.commit()
    db.refresh(db_path)

    return db_path
    
def get_learning_paths(db: Session):

    return db.query(
        models.LearningPath
    ).all()
    
def get_learning_path(
    db: Session,
    path_id: int
):

    return db.query(
        models.LearningPath
    ).filter(
        models.LearningPath.id == path_id
    ).first()
    
def update_learning_path(
    db: Session,
    path_id: int,
    path: schemas.LearningPathUpdate
):

    db_path = get_learning_path(
        db,
        path_id
    )

    if not db_path:
        return None

    update_data = path.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(db_path, key, value)

    db.commit()
    db.refresh(db_path)

    return db_path
    
def delete_learning_path(
    db: Session,
    path_id: int
):

    db_path = get_learning_path(
        db,
        path_id
    )

    if not db_path:
        return False

    db.delete(db_path)
    db.commit()

    return True
    
def add_course_to_learning_path(
    db: Session,
    path_id: int,
    course_id: int
):

    path = get_learning_path(
        db,
        path_id
    )

    if not path:
        return None

    course = db.query(
        models.Course
    ).filter(
        models.Course.id == course_id
    ).first()

    if not course:
        return None

    mapping = models.LearningPathCourse(
        learning_path_id=path_id,
        course_id=course_id
    )

    db.add(mapping)
    db.commit()
    db.refresh(mapping)

    return mapping
    
def get_learning_path_courses(
    db: Session,
    path_id: int
):

    return db.query(
        models.LearningPathCourse
    ).filter(
        models.LearningPathCourse.learning_path_id == path_id
    ).all()
    
def complete_lesson(db, learner_profile_id, lesson_id):

    progress = db.query(models.LessonProgress).filter(
        models.LessonProgress.learner_profile_id == learner_profile_id,
        models.LessonProgress.lesson_id == lesson_id
    ).first()

    if progress:
        return progress

    progress = models.LessonProgress(
        learner_profile_id=learner_profile_id,
        lesson_id=lesson_id,
        completed="Yes"
    )

    db.add(progress)
    db.commit()
    db.refresh(progress)
    
    lesson = db.query(models.Lesson).filter(
        models.Lesson.id == lesson_id
    ).first()

    skill = db.query(models.Skill).filter(
        models.Skill.learner_profile_id == learner_profile_id,
        models.Skill.skill_name == lesson.title
    ).first()

    if skill:

        skill.mastery_percentage = 100
        skill.skill_level = "Advanced"

    else:

        skill = models.Skill(
            learner_profile_id=learner_profile_id,
            skill_name=lesson.title,
            mastery_percentage=100,
            skill_level="Advanced"
        )

        db.add(skill)

    db.commit()
    
    learner = db.query(models.LearnerProfile).filter(
        models.LearnerProfile.id == learner_profile_id
    ).first()

    notify_user(
        db,
        learner.user_id,
        "Lesson Completed",
        f"You completed '{lesson.title}'."
    )

    return progress
    
def get_course_progress(db, learner_profile_id, course_id):

    total_lessons = db.query(models.Lesson).filter(
        models.Lesson.course_id == course_id
    ).count()

    completed_lessons = (
        db.query(models.LessonProgress)
        .join(
            models.Lesson,
            models.Lesson.id == models.LessonProgress.lesson_id
        )
        .filter(
            models.Lesson.course_id == course_id,
            models.LessonProgress.learner_profile_id == learner_profile_id,
            models.LessonProgress.completed == "Yes"
        )
        .count()
    )

    progress_percentage = 0

    if total_lessons > 0:
        progress_percentage = round(
            (completed_lessons / total_lessons) * 100,
            2
        )

    return {
        "course_id": course_id,
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "progress_percentage": progress_percentage
    }
    
from sqlalchemy import func

def get_learning_analytics(db, learner_profile_id):

    learner = db.query(models.LearnerProfile).filter(
        models.LearnerProfile.id == learner_profile_id
    ).first()

    if learner is None:
        return None

    courses_enrolled = db.query(models.Course).count()

    lessons_completed = db.query(models.LessonProgress).filter(
        models.LessonProgress.learner_profile_id == learner_profile_id,
        models.LessonProgress.completed == "Yes"
    ).count()

    average_score = db.query(
        func.avg(models.AssessmentHistory.score)
    ).filter(
        models.AssessmentHistory.learner_profile_id == learner_profile_id
    ).scalar()

    if average_score is None:
        average_score = 0

    practice_sessions = db.query(models.PracticeHistory).filter(
        models.PracticeHistory.learner_profile_id == learner_profile_id
    ).count()

    return {
        "courses_enrolled": courses_enrolled,
        "lessons_completed": lessons_completed,
        "average_assessment_score": round(average_score, 2),
        "practice_sessions": practice_sessions,
        "current_level": learner.learning_level
    }    
    
def get_lesson_recommendation(db, learner_profile_id):

    completed_lessons = db.query(
        models.LessonProgress.lesson_id
    ).filter(
        models.LessonProgress.learner_profile_id == learner_profile_id,
        models.LessonProgress.completed == "Yes"
    )

    lesson = db.query(models.Lesson).filter(
        ~models.Lesson.id.in_(completed_lessons)
    ).order_by(
        models.Lesson.lesson_order
    ).first()

    if lesson:

        return {
            "lesson_id": lesson.id,
            "lesson_title": lesson.title,
            "reason": "Next incomplete lesson."
        }

    return {
        "lesson_id": 0,
        "lesson_title": "No lessons remaining",
        "reason": "Congratulations! You have completed all available lessons."
    }
    
def get_skill_mastery(db, learner_profile_id):

    skills = db.query(models.Skill).filter(
        models.Skill.learner_profile_id == learner_profile_id
    ).all()

    return skills
    
def get_instructor_dashboard(db: Session):

    return {
        "total_courses": db.query(models.Course).count(),
        "total_modules": db.query(models.CourseModule).count(),
        "total_lessons": db.query(models.Lesson).count(),
        "total_contents": db.query(models.LessonContent).count()
    }
    
# ==========================================
# ADMIN DASHBOARD
# ==========================================

def get_admin_dashboard(db: Session):

    average_score = db.query(
        func.avg(models.AssessmentHistory.score)
    ).scalar()

    if average_score is None:
        average_score = 0

    return {
        "total_users": db.query(models.User).count(),
        "total_learners": db.query(models.User).filter(
            models.User.role == "Learner"
        ).count(),
        "total_instructors": db.query(models.User).filter(
            models.User.role == "Instructor"
        ).count(),
        "total_trainers": db.query(models.User).filter(
            models.User.role == "Accessibility Trainer"
        ).count(),
        "total_courses": db.query(models.Course).count(),
        "total_lessons": db.query(models.Lesson).count(),
        "total_assessments": db.query(models.AssessmentHistory).count(),
        "average_score": round(average_score, 2)
    }
    
def get_all_users(db: Session):

    return db.query(models.User).all()
    
def get_user(db: Session, user_id: int):

    return db.query(models.User).filter(
        models.User.id == user_id
    ).first()
    
def admin_update_user(
    db: Session,
    user_id: int,
    user_data
):

    user = get_user(db, user_id)

    if user is None:
        return None

    update_data = user_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user
    
def admin_delete_user(
    db: Session,
    user_id: int
):

    user = get_user(db, user_id)

    if user is None:
        return False

    db.delete(user)
    db.commit()

    return True
    
def get_admin_analytics(db: Session):

    average_score = db.query(
        func.avg(models.AssessmentHistory.score)
    ).scalar()

    if average_score is None:
        average_score = 0

    return {
        "daily_active_users": db.query(models.User).count(),
        "weekly_active_users": db.query(models.User).count(),
        "monthly_active_users": db.query(models.User).count(),
        "average_assessment_score": round(average_score, 2),
        "completed_lessons": db.query(
            models.LessonProgress
        ).filter(
            models.LessonProgress.completed == "Yes"
        ).count()
    }
    
# =====================================================
# TRAINER ASSIGNMENT
# =====================================================

def assign_learner_to_trainer(
    db: Session,
    trainer_id: int,
    learner_profile_id: int
):

    trainer = db.query(models.User).filter(
        models.User.id == trainer_id,
        models.User.role == "Trainer"
    ).first()

    if trainer is None:
        return None

    learner = db.query(models.LearnerProfile).filter(
        models.LearnerProfile.id == learner_profile_id
    ).first()

    if learner is None:
        return None

    existing = db.query(models.TrainerAssignment).filter(
        models.TrainerAssignment.learner_profile_id == learner_profile_id
    ).first()

    if existing:
        return existing

    assignment = models.TrainerAssignment(
        trainer_id=trainer_id,
        learner_profile_id=learner_profile_id
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment
    
def get_trainer_learners(
    db: Session,
    trainer_id: int
):

    return db.query(models.TrainerAssignment).filter(
        models.TrainerAssignment.trainer_id == trainer_id
    ).all()
    
def get_trainer_dashboard(db: Session, trainer_id: int):

    assignments = db.query(models.TrainerAssignment).filter(
        models.TrainerAssignment.trainer_id == trainer_id
    ).all()

    learner_ids = [a.learner_profile_id for a in assignments]

    total_learners = len(learner_ids)

    total_assessments = db.query(models.AssessmentHistory).filter(
        models.AssessmentHistory.learner_profile_id.in_(learner_ids)
    ).count()

    average_score = db.query(
        func.avg(models.AssessmentHistory.score)
    ).filter(
        models.AssessmentHistory.learner_profile_id.in_(learner_ids)
    ).scalar()

    if average_score is None:
        average_score = 0

    return {
        "total_assigned_learners": total_learners,
        "total_completed_assessments": total_assessments,
        "average_score": round(average_score, 2)
    }
    
def get_trainer_learner_progress(
    db: Session,
    trainer_id: int
):

    assignments = db.query(models.TrainerAssignment).filter(
        models.TrainerAssignment.trainer_id == trainer_id
    ).all()

    result = []

    for assignment in assignments:

        learner = assignment.learner_profile

        completed_lessons = db.query(models.LessonProgress).filter(
            models.LessonProgress.learner_profile_id == learner.id,
            models.LessonProgress.completed == "Yes"
        ).count()

        total_assessments = db.query(models.AssessmentHistory).filter(
            models.AssessmentHistory.learner_profile_id == learner.id
        ).count()

        average_score = db.query(
            func.avg(models.AssessmentHistory.score)
        ).filter(
            models.AssessmentHistory.learner_profile_id == learner.id
        ).scalar()

        if average_score is None:
            average_score = 0

        result.append({
            "learner_name": learner.user.name,
            "total_completed_lessons": completed_lessons,
            "total_assessments": total_assessments,
            "average_score": round(average_score, 2)
        })

    return result
    
def create_trainer_feedback(
    db: Session,
    trainer_id: int,
    feedback_data: schemas.TrainerFeedbackCreate
):

    feedback = models.TrainerFeedback(
        trainer_id=trainer_id,
        learner_profile_id=feedback_data.learner_profile_id,
        feedback=feedback_data.feedback
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    learner = db.query(models.LearnerProfile).filter(
        models.LearnerProfile.id == feedback_data.learner_profile_id
    ).first()
    
    notify_user(
        db,
        learner.user_id,
        "Trainer Feedback",
        "Your trainer has provided feedback on your assessment."
    )

    return feedback
    
def get_learner_feedback(
    db: Session,
    learner_profile_id: int
):

    return db.query(models.TrainerFeedback).filter(
        models.TrainerFeedback.learner_profile_id == learner_profile_id
    ).order_by(
        models.TrainerFeedback.created_at.desc()
    ).all()
    
def update_trainer_feedback(
    db: Session,
    trainer_id: int,
    feedback_id: int,
    feedback_text: str
):

    feedback = db.query(models.TrainerFeedback).filter(
        models.TrainerFeedback.id == feedback_id,
        models.TrainerFeedback.trainer_id == trainer_id
    ).first()

    if feedback is None:
        return None

    feedback.feedback = feedback_text

    db.commit()
    db.refresh(feedback)

    return feedback
    
def delete_trainer_feedback(
    db: Session,
    trainer_id: int,
    feedback_id: int
):

    feedback = db.query(models.TrainerFeedback).filter(
        models.TrainerFeedback.id == feedback_id,
        models.TrainerFeedback.trainer_id == trainer_id
    ).first()

    if feedback is None:
        return False

    db.delete(feedback)
    db.commit()

    return True
    
import uuid

# =====================================================
# CERTIFICATES
# =====================================================

def generate_certificate(
    db: Session,
    learner_profile_id: int,
    course_id: int
):

    # Check if certificate already exists
    existing = db.query(models.Certificate).filter(
        models.Certificate.learner_profile_id == learner_profile_id,
        models.Certificate.course_id == course_id
    ).first()

    if existing:
        return existing

    certificate = models.Certificate(
        learner_profile_id=learner_profile_id,
        course_id=course_id,
        certificate_number=str(uuid.uuid4())[:12].upper()
    )

    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    
    learner = db.query(models.LearnerProfile).filter(
        models.LearnerProfile.id == learner_profile_id
    ).first()

    notify_user(
        db,
        learner.user_id,
        "Certificate Generated",
        "Congratulations! Your certificate has been generated successfully."
    )

    return certificate
    
def get_certificates(
    db: Session,
    learner_profile_id: int
):

    return db.query(models.Certificate).filter(
        models.Certificate.learner_profile_id == learner_profile_id
    ).all()
    
def verify_certificate(
    db: Session,
    certificate_number: str
):

    return db.query(models.Certificate).filter(
        models.Certificate.certificate_number == certificate_number
    ).first()
    
def generate_learning_report(
    db: Session,
    learner_profile_id: int
):

    learner = db.query(models.LearnerProfile).filter(
        models.LearnerProfile.id == learner_profile_id
    ).first()

    completed_lessons = db.query(models.LessonProgress).filter(
        models.LessonProgress.learner_profile_id == learner_profile_id,
        models.LessonProgress.completed == "Yes"
    ).count()

    average_score = db.query(
        func.avg(models.AssessmentHistory.score)
    ).filter(
        models.AssessmentHistory.learner_profile_id == learner_profile_id
    ).scalar() or 0

    practice_sessions = db.query(models.PracticeHistory).filter(
        models.PracticeHistory.learner_profile_id == learner_profile_id
    ).count()

    certificates = db.query(models.Certificate).filter(
        models.Certificate.learner_profile_id == learner_profile_id
    ).count()

    return {
        "learner_name": learner.user.name,
        "completed_lessons": completed_lessons,
        "average_score": round(average_score, 2),
        "practice_sessions": practice_sessions,
        "certificates": certificates
    }
    
# =====================================================
# NOTIFICATIONS
# =====================================================

def create_notification(
    db: Session,
    notification: schemas.NotificationCreate
):

    db_notification = models.Notification(
        user_id=notification.user_id,
        title=notification.title,
        message=notification.message
    )

    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return db_notification


def get_notifications(
    db: Session,
    current_user
):

    return (
        db.query(models.Notification)
        .filter(
            models.Notification.user_id == current_user.id
        )
        .order_by(
            models.Notification.created_at.desc()
        )
        .all()
    )


def mark_notification_as_read(
    db: Session,
    notification_id: int,
    current_user
):

    notification = (
        db.query(models.Notification)
        .filter(
            models.Notification.id == notification_id,
            models.Notification.user_id == current_user.id
        )
        .first()
    )

    if notification is None:
        return None

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification


def delete_notification(
    db: Session,
    notification_id: int,
    current_user
):

    notification = (
        db.query(models.Notification)
        .filter(
            models.Notification.id == notification_id,
            models.Notification.user_id == current_user.id
        )
        .first()
    )

    if notification is None:
        return False

    db.delete(notification)
    db.commit()

    return True
    
def notify_user(
    db: Session,
    user_id: int,
    title: str,
    message: str
):

    notification = models.Notification(
        user_id=user_id,
        title=title,
        message=message
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification
    
def create_announcement(
    db: Session,
    current_user,
    announcement: schemas.AnnouncementCreate
):

    db_announcement = models.Announcement(
        title=announcement.title,
        message=announcement.message,
        created_by=current_user.id
    )

    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)

    return db_announcement
    
def get_announcements(db: Session):

    return db.query(
        models.Announcement
    ).order_by(
        models.Announcement.created_at.desc()
    ).all()
    
def update_announcement(
    db: Session,
    announcement_id: int,
    announcement: schemas.AnnouncementUpdate
):

    db_announcement = db.query(
        models.Announcement
    ).filter(
        models.Announcement.id == announcement_id
    ).first()

    if db_announcement is None:
        return None

    update_data = announcement.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_announcement, key, value)

    db.commit()
    db.refresh(db_announcement)

    return db_announcement
    
def delete_announcement(
    db: Session,
    announcement_id: int
):

    announcement = db.query(
        models.Announcement
    ).filter(
        models.Announcement.id == announcement_id
    ).first()

    if announcement is None:
        return False

    db.delete(announcement)
    db.commit()

    return True
