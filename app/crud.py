from sqlalchemy.orm import Session

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
