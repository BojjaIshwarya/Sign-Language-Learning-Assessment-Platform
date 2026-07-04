from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import schemas, crud
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/learning",
    tags=["Learner Profile Management"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================================================
# LEARNER PROFILE
# =====================================================

@router.post("/profile", response_model=schemas.LearnerProfileResponse)
def create_profile(
    profile: schemas.LearnerProfileCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    learner = crud.create_learner_profile(
        db,
        current_user,
        profile
    )

    if learner is None:
        raise HTTPException(
            status_code=400,
            detail="Learner profile already exists"
        )

    return learner


@router.get("/profile", response_model=schemas.LearnerProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    learner = crud.get_learner_profile(
        db,
        current_user
    )

    if learner is None:
        raise HTTPException(
            status_code=404,
            detail="Learner profile not found"
        )

    return learner


@router.put("/profile", response_model=schemas.LearnerProfileResponse)
def update_profile(
    profile: schemas.LearnerProfileUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    learner = crud.update_learner_profile(
        db,
        current_user,
        profile
    )

    if learner is None:
        raise HTTPException(
            status_code=404,
            detail="Learner profile not found"
        )

    return learner


# =====================================================
# LEARNING GOAL MANAGEMENT
# =====================================================

@router.post("/goals", response_model=schemas.LearningGoalResponse)
def create_goal(
    goal: schemas.LearningGoalCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.create_learning_goal(
        db,
        current_user,
        goal
    )


@router.get("/goals", response_model=list[schemas.LearningGoalResponse])
def get_goals(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.get_learning_goals(
        db,
        current_user
    )


@router.put("/goals/{goal_id}", response_model=schemas.LearningGoalResponse)
def update_goal(
    goal_id: int,
    goal: schemas.LearningGoalUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    updated_goal = crud.update_learning_goal(
        db,
        current_user,
        goal_id,
        goal
    )

    if updated_goal is None:
        raise HTTPException(
            status_code=404,
            detail="Learning goal not found"
        )

    return updated_goal


@router.delete("/goals/{goal_id}")
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    success = crud.delete_learning_goal(
        db,
        current_user,
        goal_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Learning goal not found"
        )

    return {
        "message": "Learning goal deleted successfully"
    }


# =====================================================
# SKILL TRACKING
# =====================================================

@router.post("/skills", response_model=schemas.SkillResponse)
def create_skill(
    skill: schemas.SkillCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.create_skill(
        db,
        current_user,
        skill
    )


@router.get("/skills", response_model=list[schemas.SkillResponse])
def get_skills(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.get_skills(
        db,
        current_user
    )


@router.put("/skills/{skill_id}", response_model=schemas.SkillResponse)
def update_skill(
    skill_id: int,
    skill: schemas.SkillUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    updated_skill = crud.update_skill(
        db,
        current_user,
        skill_id,
        skill
    )

    if updated_skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    return updated_skill

# ==========================================
# DELETE SKILL
# ==========================================

@router.delete("/skills/{skill_id}")
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    success = crud.delete_skill(
        db,
        current_user,
        skill_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    return {
        "message": "Skill deleted successfully."
    }
    
# =====================================================
# PRACTICE HISTORY
# =====================================================

# ==========================================
# CREATE PRACTICE HISTORY
# ==========================================

@router.post(
    "/practice",
    response_model=schemas.PracticeHistoryResponse
)
def create_practice(
    practice: schemas.PracticeHistoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    result = crud.create_practice_history(
        db,
        current_user,
        practice
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Learner profile not found"
        )

    return result
    
@router.get(
    "/practice-history",
    response_model=list[schemas.PracticeHistoryResponse]
)
def practice_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.get_practice_history(
        db,
        current_user
    )


# =====================================================
# ASSESSMENT HISTORY
# =====================================================

# ==========================================
# CREATE ASSESSMENT HISTORY
# ==========================================

@router.post(
    "/assessment",
    response_model=schemas.AssessmentHistoryResponse
)
def create_assessment(
    assessment: schemas.AssessmentHistoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    result = crud.create_assessment_history(
        db,
        current_user,
        assessment
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Learner profile not found"
        )

    return result

@router.get(
    "/assessment-history",
    response_model=list[schemas.AssessmentHistoryResponse]
)
def assessment_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.get_assessment_history(
        db,
        current_user
    )
