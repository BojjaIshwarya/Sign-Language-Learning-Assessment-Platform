from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


# =====================================================
# USER
# =====================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="Learner")

    learner_profile = relationship(
        "LearnerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


# =====================================================
# LEARNER PROFILE
# =====================================================

class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True
    )

    learning_level = Column(String, default="Beginner")

    preferred_language = Column(String, default="English")

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="learner_profile"
    )

    learning_goals = relationship(
        "LearningGoal",
        back_populates="learner_profile",
        cascade="all, delete-orphan"
    )

    skills = relationship(
        "Skill",
        back_populates="learner_profile",
        cascade="all, delete-orphan"
    )

    practice_history = relationship(
        "PracticeHistory",
        back_populates="learner_profile",
        cascade="all, delete-orphan"
    )

    assessment_history = relationship(
        "AssessmentHistory",
        back_populates="learner_profile",
        cascade="all, delete-orphan"
    )


# =====================================================
# LEARNING GOALS
# =====================================================

class LearningGoal(Base):
    __tablename__ = "learning_goals"

    id = Column(Integer, primary_key=True, index=True)

    learner_profile_id = Column(
        Integer,
        ForeignKey("learner_profiles.id")
    )

    goal_title = Column(String, nullable=False)

    description = Column(String)

    status = Column(String, default="Pending")

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    learner_profile = relationship(
        "LearnerProfile",
        back_populates="learning_goals"
    )


# =====================================================
# SKILLS
# =====================================================

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)

    learner_profile_id = Column(
        Integer,
        ForeignKey("learner_profiles.id")
    )

    skill_name = Column(String, nullable=False)

    skill_level = Column(String, default="Beginner")

    mastery_percentage = Column(Float, default=0)

    last_practiced = Column(
        DateTime,
        default=datetime.utcnow
    )

    learner_profile = relationship(
        "LearnerProfile",
        back_populates="skills"
    )


# =====================================================
# PRACTICE HISTORY
# =====================================================

class PracticeHistory(Base):
    __tablename__ = "practice_history"

    id = Column(Integer, primary_key=True, index=True)

    learner_profile_id = Column(
        Integer,
        ForeignKey("learner_profiles.id")
    )

    lesson_name = Column(String)

    score = Column(Float)

    duration = Column(Integer)

    practiced_on = Column(
        DateTime,
        default=datetime.utcnow
    )

    learner_profile = relationship(
        "LearnerProfile",
        back_populates="practice_history"
    )


# =====================================================
# ASSESSMENT HISTORY
# =====================================================

class AssessmentHistory(Base):
    __tablename__ = "assessment_history"

    id = Column(Integer, primary_key=True, index=True)

    learner_profile_id = Column(
        Integer,
        ForeignKey("learner_profiles.id")
    )

    assessment_name = Column(String)

    score = Column(Float)

    level = Column(String)

    assessed_on = Column(
        DateTime,
        default=datetime.utcnow
    )

    learner_profile = relationship(
        "LearnerProfile",
        back_populates="assessment_history"
    )
