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
    
def delete_learning_goal(db: Session, current_user, goal_id: int):

    learner = get_learner_profile(db, current_user)

    db_goal = db.query(models.LearningGoal).filter(
        models.LearningGoal.id == goal_id,
        models.LearningGoal.learner_profile_id == learner.id
    ).first()

    if not db_goal:
        return False

    db.delete(db_goal)
    db.commit()

    return True
    
def create_skill(db: Session, current_user, skill: schemas.SkillCreate):

    learner = get_learner_profile(db, current_user)

    db_skill = models.Skill(
        learner_profile_id=learner.id,
        skill_name=skill.skill_name,
        skill_level=skill.skill_level,
        mastery_percentage=0
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
