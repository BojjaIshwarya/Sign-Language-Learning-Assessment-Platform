from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud, schemas
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# GET ALL NOTIFICATIONS
# ==========================================

@router.get(
    "/",
    response_model=list[schemas.NotificationResponse]
)
def get_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.get_notifications(
        db,
        current_user
    )


# ==========================================
# MARK AS READ
# ==========================================

@router.put(
    "/{notification_id}/read",
    response_model=schemas.NotificationResponse
)
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    notification = crud.mark_notification_as_read(
        db,
        notification_id,
        current_user
    )

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found."
        )

    return notification


# ==========================================
# DELETE NOTIFICATION
# ==========================================

@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    success = crud.delete_notification(
        db,
        notification_id,
        current_user
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Notification not found."
        )

    return {
        "message": "Notification deleted successfully."
    }
