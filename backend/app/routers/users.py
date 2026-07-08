from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import schemas, crud
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["User Profile Management"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================
# View Profile
# ==========================
@router.get("/me", response_model=schemas.UserProfile)
def get_profile(
    current_user=Depends(get_current_user)
):
    return current_user


# ==========================
# Update Profile
# ==========================
@router.put("/me", response_model=schemas.UserProfile)
def update_profile(
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # Check if another user already uses this email
    existing = crud.get_user_by_email(db, user.email)

    if existing and existing.id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return crud.update_user_profile(
        db,
        current_user,
        user
    )


# ==========================
# Change Password
# ==========================
@router.put("/change-password")
def change_password(
    password_data: schemas.ChangePassword,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user = crud.change_password(
        db,
        current_user,
        password_data
    )

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    return {
        "message": "Password changed successfully"
    }
