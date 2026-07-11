from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.dependencies import get_current_user
from app import crud, schemas

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "/learning",
    response_model=schemas.LearningReportResponse
)
def learning_report(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    learner = current_user.learner_profile

    if learner is None:
        raise HTTPException(
            status_code=404,
            detail="Learner profile not found."
        )

    return crud.generate_learning_report(
        db,
        learner.id
    )
