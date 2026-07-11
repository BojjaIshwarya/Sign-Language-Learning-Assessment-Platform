from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import schemas, crud
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["Administrator"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "/dashboard",
    response_model=schemas.AdminDashboardResponse
)
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Administrator":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can access this resource."
        )

    return crud.get_admin_dashboard(db)
    
@router.get(
    "/users",
    response_model=list[schemas.AdminUserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Administrator":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can access this resource."
        )

    return crud.get_all_users(db)
    
@router.get(
    "/users/{user_id}",
    response_model=schemas.AdminUserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Administrator":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can access this resource."
        )

    user = crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
    
@router.put(
    "/users/{user_id}",
    response_model=schemas.AdminUserResponse
)
def update_user(
    user_id: int,
    user: schemas.AdminUserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Administrator":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can access this resource."
        )

    updated = crud.admin_update_user(
        db,
        user_id,
        user
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return updated
    
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Administrator":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can access this resource."
        )

    success = crud.admin_delete_user(
        db,
        user_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully."
    }
    
@router.get(
    "/analytics",
    response_model=schemas.AdminAnalyticsResponse
)
def analytics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Administrator":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can access this resource."
        )

    return crud.get_admin_analytics(db)
