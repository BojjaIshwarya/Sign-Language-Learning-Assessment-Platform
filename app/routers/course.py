from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app import schemas, crud
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/courses",
    tags=["Course Management"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# CREATE COURSE
# ==========================================

@router.post("/", response_model=schemas.CourseResponse)
def create_course(
    course: schemas.CourseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role not in [
        "Instructor",
        "Accessibility Trainer",
        "Administrator"
    ]:
        raise HTTPException(
            status_code=403,
            detail="Only instructors or administrators can create courses."
        )

    return crud.create_course(
        db,
        current_user,
        course
    )


# ==========================================
# GET ALL COURSES
# ==========================================

@router.get("/", response_model=List[schemas.CourseResponse])
def get_courses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.get_all_courses(db)


# ==========================================
# GET COURSE BY ID
# ==========================================

@router.get("/{course_id}", response_model=schemas.CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    course = crud.get_course_by_id(
        db,
        course_id
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


# ==========================================
# UPDATE COURSE
# ==========================================

@router.put("/{course_id}", response_model=schemas.CourseResponse)
def update_course(
    course_id: int,
    updated_course: schemas.CourseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role not in [
        "Instructor",
        "Accessibility Trainer",
        "Administrator"
    ]:
        raise HTTPException(
            status_code=403,
            detail="Permission denied."
        )

    course = crud.update_course(
        db,
        course_id,
        updated_course
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


# ==========================================
# DELETE COURSE
# ==========================================

@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Administrator":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can delete courses."
        )

    course = crud.delete_course(
        db,
        course_id
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return {
        "message": "Course deleted successfully."
    }
    
@router.post(
    "/{course_id}/lessons",
    response_model=schemas.LessonResponse
)
def create_lesson(
    course_id: int,
    lesson: schemas.LessonCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    db_lesson = crud.create_lesson(
        db,
        course_id,
        lesson
    )

    if db_lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return db_lesson
    
@router.get(
    "/{course_id}/lessons",
    response_model=list[schemas.LessonResponse]
)
def get_lessons(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.get_lessons_by_course(
        db,
        course_id
    )
    
@router.get(
    "/lessons/{lesson_id}",
    response_model=schemas.LessonResponse
)
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    lesson = crud.get_lesson(
        db,
        lesson_id
    )

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return lesson
    
@router.put(
    "/lessons/{lesson_id}",
    response_model=schemas.LessonResponse
)
def update_lesson(
    lesson_id: int,
    lesson: schemas.LessonUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    updated = crud.update_lesson(
        db,
        lesson_id,
        lesson
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return updated
    
@router.delete("/lessons/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    success = crud.delete_lesson(
        db,
        lesson_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return {
        "message": "Lesson deleted successfully"
    }
