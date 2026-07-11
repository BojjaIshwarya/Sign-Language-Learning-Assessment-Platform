from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud, schemas
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/trainer",
    tags=["Trainer"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post(
    "/assign",
    response_model=schemas.TrainerAssignmentResponse
)
def assign_learner(
    assignment: schemas.TrainerAssignmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Administrator":
        raise HTTPException(
            status_code=403,
            detail="Only Administrator can assign learners."
        )

    result = crud.assign_learner_to_trainer(
        db,
        assignment.trainer_id,
        assignment.learner_profile_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Trainer or Learner not found."
        )

    return result
    
@router.get(
    "/learners",
    response_model=list[schemas.TrainerAssignmentResponse]
)
def trainer_learners(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Trainer":
        raise HTTPException(
            status_code=403,
            detail="Only Trainers can access."
        )

    return crud.get_trainer_learners(
        db,
        current_user.id
    )
    
@router.get(
    "/dashboard",
    response_model=schemas.TrainerDashboardResponse
)
def trainer_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Trainer":
        raise HTTPException(
            status_code=403,
            detail="Only Trainers can access."
        )

    return crud.get_trainer_dashboard(
        db,
        current_user.id
    )
    
@router.get(
    "/learner-progress",
    response_model=list[schemas.TrainerLearnerProgressResponse]
)
def learner_progress(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Trainer":
        raise HTTPException(
            status_code=403,
            detail="Only Trainers can access."
        )

    return crud.get_trainer_learner_progress(
        db,
        current_user.id
    )
    
@router.post(
    "/feedback",
    response_model=schemas.TrainerFeedbackResponse
)
def create_feedback(
    feedback: schemas.TrainerFeedbackCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Trainer":
        raise HTTPException(
            status_code=403,
            detail="Only Trainers can access."
        )

    return crud.create_trainer_feedback(
        db,
        current_user.id,
        feedback
    )
    
@router.get(
    "/feedback/{learner_profile_id}",
    response_model=list[schemas.TrainerFeedbackResponse]
)
def learner_feedback(
    learner_profile_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role not in ["Trainer", "Administrator"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied."
        )

    return crud.get_learner_feedback(
        db,
        learner_profile_id
    )
    
@router.delete("/feedback/{feedback_id}")
def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Trainer":
        raise HTTPException(
            status_code=403,
            detail="Only Trainers can access."
        )

    success = crud.delete_trainer_feedback(
        db,
        current_user.id,
        feedback_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Feedback not found."
        )

    return {
        "message": "Feedback deleted successfully."
    }
    

