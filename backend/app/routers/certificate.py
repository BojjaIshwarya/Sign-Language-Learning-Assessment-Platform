from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud, schemas
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/certificate",
    tags=["Certificates"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post(
    "/generate/{course_id}",
    response_model=schemas.CertificateResponse
)
def generate_certificate(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    learner = current_user.learner_profile

    if learner is None:
        raise HTTPException(
            status_code=404,
            detail="Learner profile not found."
        )

    progress = crud.get_course_progress(
        db,
        learner.id,
        course_id
    )

    if progress["progress_percentage"] < 100:
        raise HTTPException(
            status_code=400,
            detail="Course not completed."
        )

    return crud.generate_certificate(
        db,
        learner.id,
        course_id
    )
    
@router.get(
    "",
    response_model=list[schemas.CertificateResponse]
)
def my_certificates(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    learner = current_user.learner_profile

    if learner is None:
        raise HTTPException(
            status_code=404,
            detail="Learner profile not found."
        )

    return crud.get_certificates(
        db,
        learner.id
    )
    
@router.get(
    "/verify/{certificate_number}",
    response_model=schemas.CertificateResponse
)
def verify_certificate(
    certificate_number: str,
    db: Session = Depends(get_db)
):

    certificate = crud.verify_certificate(
        db,
        certificate_number
    )

    if certificate is None:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found."
        )

    return certificate
