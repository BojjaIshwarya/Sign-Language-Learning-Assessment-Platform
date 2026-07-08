from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    ForeignKey
)
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

    courses = relationship(
        "Course",
        back_populates="instructor",
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

    learning_level = Column(
        String,
        default="Beginner"
    )

    preferred_language = Column(
        String,
        default="English"
    )

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

    goal_title = Column(
        String,
        nullable=False
    )

    description = Column(String)

    status = Column(
        String,
        default="Pending"
    )

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

    skill_name = Column(
        String,
        nullable=False
    )

    skill_level = Column(
        String,
        default="Beginner"
    )

    mastery_percentage = Column(
        Float,
        default=0
    )

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
    
    expected_sign = Column(String)

    predicted_sign = Column(String)

    confidence = Column(Float)

    assessed_on = Column(
        DateTime,
        default=datetime.utcnow
    )

    learner_profile = relationship(
        "LearnerProfile",
        back_populates="assessment_history"
    )


# =====================================================
# COURSE MANAGEMENT
# =====================================================

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    category = Column(
        String,
        nullable=False
    )

    level = Column(
        String,
        nullable=False
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    instructor = relationship(
        "User",
        back_populates="courses"
    )
    
    lessons = relationship(
    "Lesson",
    back_populates="course",
    cascade="all, delete-orphan"
    )
	
    modules = relationship(
    "CourseModule",
    back_populates="course",
    cascade="all, delete-orphan"
    )

# =====================================================
# COURSE MODULE MANAGEMENT
# =====================================================

class CourseModule(Base):
    __tablename__ = "course_modules"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False
    )

    title = Column(String, nullable=False)

    description = Column(String)

    module_order = Column(Integer, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    course = relationship(
        "Course",
        back_populates="modules"
    )

    lessons = relationship(
        "Lesson",
        back_populates="module",
        cascade="all, delete-orphan"
    )
	
# =====================================================
# LESSON MANAGEMENT
# =====================================================

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False
    )
    
    module_id = Column(
    Integer,
    ForeignKey("course_modules.id"),
    nullable=True
    )

    title = Column(String, nullable=False)

    description = Column(String)

    lesson_order = Column(Integer, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    course = relationship(
        "Course",
        back_populates="lessons"
    )
    
    module = relationship(
    "CourseModule",
    back_populates="lessons"
    )
    
    contents = relationship(
    "LessonContent",
    back_populates="lesson",
    cascade="all, delete-orphan"
    ) 
# =====================================================
# LESSON CONTENT MANAGEMENT
# =====================================================

class LessonContent(Base):
    __tablename__ = "lesson_contents"

    id = Column(Integer, primary_key=True, index=True)

    lesson_id = Column(
        Integer,
        ForeignKey("lessons.id"),
        nullable=False
    )

    title = Column(
        String,
        nullable=False
    )

    content_type = Column(
        String,
        nullable=False
    )  # Video, PDF, Image, Text

    content_url = Column(
        String,
        nullable=False
    )

    description = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    lesson = relationship(
        "Lesson",
        back_populates="contents"
    )
   
# =====================================================
# LEARNING PATH MANAGEMENT
# =====================================================

class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    courses = relationship(
        "LearningPathCourse",
        back_populates="learning_path",
        cascade="all, delete-orphan"
    )


class LearningPathCourse(Base):
    __tablename__ = "learning_path_courses"

    id = Column(Integer, primary_key=True, index=True)

    learning_path_id = Column(
        Integer,
        ForeignKey("learning_paths.id"),
        nullable=False
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False
    )

    learning_path = relationship(
        "LearningPath",
        back_populates="courses"
    )

    course = relationship("Course")
