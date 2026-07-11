from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/announcements",
    tags=["Announcements"]
)

@router.post(
    "/",
    response_model=schemas.AnnouncementResponse
)
def create_announcement(
    announcement: schemas.AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role not in [
        "Administrator",
        "Instructor"
    ]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized."
        )

    return crud.create_announcement(
        db,
        current_user,
        announcement
    )
    
@router.get(
    "/",
    response_model=list[schemas.AnnouncementResponse]
)
def get_announcements(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.get_announcements(db)
    
@router.put(
    "/{announcement_id}",
    response_model=schemas.AnnouncementResponse
)
def update_announcement(
    announcement_id: int,
    announcement: schemas.AnnouncementUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role not in [
        "Administrator",
        "Instructor"
    ]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized."
        )

    updated = crud.update_announcement(
        db,
        announcement_id,
        announcement
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Announcement not found."
        )

    return updated
    
@router.delete("/{announcement_id}")
def delete_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role not in [
        "Administrator",
        "Instructor"
    ]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized."
        )

    success = crud.delete_announcement(
        db,
        announcement_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Announcement not found."
        )

    return {
        "message": "Announcement deleted successfully."
    }
