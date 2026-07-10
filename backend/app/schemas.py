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

class LoginUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    user: LoginUser
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
    name: Optional[str] = None
    email: Optional[EmailStr] = None


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
    mastery_percentage: float = 0


class SkillUpdate(BaseModel):
    skill_name: Optional[str] = None
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
        
# =====================================================
# COURSE MODULE MANAGEMENT
# =====================================================

class ModuleCreate(BaseModel):
    title: str
    description: Optional[str] = None
    module_order: int


class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    module_order: Optional[int] = None


class ModuleResponse(BaseModel):
    id: int
    course_id: int
    title: str
    description: Optional[str]
    module_order: int
    created_at: datetime

    class Config:
        from_attributes = True
# =====================================================
# LESSON MANAGEMENT
# =====================================================

class LessonCreate(BaseModel):
    title: str
    description: str
    lesson_order: int


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    lesson_order: Optional[int] = None


class LessonResponse(BaseModel):
    id: int
    course_id: int
    title: str
    description: str
    lesson_order: int
    created_at: datetime

    class Config:
        from_attributes = True

# =====================================================
# LESSON CONTENT MANAGEMENT
# =====================================================

class LessonContentCreate(BaseModel):
    title: str
    content_type: str
    content_url: str
    description: Optional[str] = None


class LessonContentUpdate(BaseModel):
    title: Optional[str] = None
    content_type: Optional[str] = None
    content_url: Optional[str] = None
    description: Optional[str] = None


class LessonContentResponse(BaseModel):
    id: int
    lesson_id: int
    title: str
    content_type: str
    content_url: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
 
# =====================================================
# LEARNING PATH MANAGEMENT
# =====================================================

class LearningPathCreate(BaseModel):
    title: str
    description: Optional[str] = None


class LearningPathUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class LearningPathResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class LearningPathCourseResponse(BaseModel):
    id: int
    learning_path_id: int
    course_id: int

    class Config:
        from_attributes = True           
# ==========================================
# PRACTICE HISTORY
# ==========================================

class PracticeHistoryCreate(BaseModel):
    lesson_name: str
    score: float
    duration: int


class PracticeHistoryResponse(BaseModel):
    id: int
    learner_profile_id: int
    lesson_name: str
    score: float
    duration: int
    practiced_on: datetime

    class Config:
        from_attributes = True
        
# ==========================================
# ASSESSMENT HISTORY
# ==========================================

class AssessmentHistoryCreate(BaseModel):
    assessment_name: str
    score: float
    level: str


class AssessmentHistoryResponse(BaseModel):
    id: int
    learner_profile_id: int
    assessment_name: str
    score: float
    level: str
    assessed_on: datetime

    class Config:
        from_attributes = True
        
# =====================================================
# ASSESSMENT
# =====================================================

class AssessmentStartResponse(BaseModel):
    lesson_id: int
    expected_sign: str
    status: str


class AssessmentResultResponse(BaseModel):
    expected_sign: str
    predicted_sign: str
    confidence: float
    correct: bool
    
# =====================================================
# LESSON PROGRESS
# =====================================================

class LessonProgressResponse(BaseModel):
    id: int
    learner_profile_id: int
    lesson_id: int
    completed: str
    completed_at: datetime

    class Config:
        from_attributes = True
        
class CourseProgressResponse(BaseModel):
    course_id: int
    total_lessons: int
    completed_lessons: int
    progress_percentage: float

    class Config:
        from_attributes = True
        
class LearningAnalyticsResponse(BaseModel):

    courses_enrolled: int
    lessons_completed: int
    average_assessment_score: float
    practice_sessions: int
    current_level: str
    
class LessonRecommendationResponse(BaseModel):

    lesson_id: int
    lesson_title: str
    reason: str
