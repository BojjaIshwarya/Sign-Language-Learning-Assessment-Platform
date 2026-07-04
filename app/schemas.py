from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# =====================================================
# AUTHENTICATION
# =====================================================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "Learner"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# =====================================================
# USER PROFILE MANAGEMENT
# =====================================================

class UserProfile(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str
    email: EmailStr


class ChangePassword(BaseModel):
    current_password: str
    new_password: str


# =====================================================
# LEARNER PROFILE
# =====================================================

class LearnerProfileCreate(BaseModel):
    learning_level: str
    preferred_language: str


class LearnerProfileUpdate(BaseModel):
    learning_level: Optional[str] = None
    preferred_language: Optional[str] = None


class LearnerProfileResponse(BaseModel):
    id: int
    user_id: int
    learning_level: str
    preferred_language: str
    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# LEARNING GOALS
# =====================================================

class LearningGoalCreate(BaseModel):
    goal_title: str
    description: Optional[str] = None


class LearningGoalUpdate(BaseModel):
    goal_title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class LearningGoalResponse(BaseModel):
    id: int
    learner_profile_id: int
    goal_title: str
    description: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# SKILL TRACKING
# =====================================================

class SkillCreate(BaseModel):
    skill_name: str
    skill_level: str = "Beginner"


class SkillUpdate(BaseModel):
    skill_level: Optional[str] = None
    mastery_percentage: Optional[float] = None


class SkillResponse(BaseModel):
    id: int
    learner_profile_id: int
    skill_name: str
    skill_level: str
    mastery_percentage: float
    last_practiced: datetime

    class Config:
        from_attributes = True


# =====================================================
# PRACTICE HISTORY
# =====================================================

class PracticeHistoryResponse(BaseModel):
    id: int
    lesson_name: str
    score: float
    duration: int
    practiced_on: datetime

    class Config:
        from_attributes = True


# =====================================================
# ASSESSMENT HISTORY
# =====================================================

class AssessmentHistoryResponse(BaseModel):
    id: int
    assessment_name: str
    score: float
    level: str
    assessed_on: datetime

    class Config:
        from_attributes = True
        
# =====================================================
# COURSE MANAGEMENT
# =====================================================

class CourseCreate(BaseModel):
    title: str
    description: str
    category: str
    level: str


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    level: str
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True
