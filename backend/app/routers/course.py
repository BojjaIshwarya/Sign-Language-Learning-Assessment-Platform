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

@router.post(
    "/learning-paths",
    response_model=schemas.LearningPathResponse
)
def create_learning_path(
    path: schemas.LearningPathCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.create_learning_path(db, path)
    
@router.get(
    "/learning-paths",
    response_model=list[schemas.LearningPathResponse]
)
def get_learning_paths(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_learning_paths(db)
    
@router.get(
    "/learning-paths/{path_id}",
    response_model=schemas.LearningPathResponse
)
def get_learning_path(
    path_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    path = crud.get_learning_path(db, path_id)

    if path is None:
        raise HTTPException(
            status_code=404,
            detail="Learning path not found"
        )

    return path
    
@router.put(
    "/learning-paths/{path_id}",
    response_model=schemas.LearningPathResponse
)
def update_learning_path(
    path_id: int,
    path: schemas.LearningPathUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated = crud.update_learning_path(
        db,
        path_id,
        path
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Learning path not found"
        )

    return updated
    
@router.delete("/learning-paths/{path_id}")
def delete_learning_path(
    path_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    success = crud.delete_learning_path(
        db,
        path_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Learning path not found"
        )

    return {
        "message": "Learning path deleted successfully"
    }
    
@router.post(
    "/learning-paths/{path_id}/courses/{course_id}",
    response_model=schemas.LearningPathCourseResponse
)
def add_course_to_learning_path(
    path_id: int,
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    mapping = crud.add_course_to_learning_path(
        db,
        path_id,
        course_id
    )

    if mapping is None:
        raise HTTPException(
            status_code=404,
            detail="Learning path or course not found"
        )

    return mapping
    
@router.get(
    "/learning-paths/{path_id}/courses",
    response_model=list[schemas.LearningPathCourseResponse]
)
def get_learning_path_courses(
    path_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_learning_path_courses(
        db,
        path_id
    )
    
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
    "/{course_id}/modules",
    response_model=schemas.ModuleResponse
)
def create_module(
    course_id: int,
    module: schemas.ModuleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    db_module = crud.create_module(
        db,
        course_id,
        module
    )

    if db_module is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return db_module
    
@router.get(
    "/{course_id}/modules",
    response_model=list[schemas.ModuleResponse]
)
def get_modules(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.get_modules_by_course(
        db,
        course_id
    )
    
@router.get(
    "/modules/{module_id}",
    response_model=schemas.ModuleResponse
)
def get_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    module = crud.get_module(
        db,
        module_id
    )

    if module is None:
        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )

    return module
    
@router.put(
    "/modules/{module_id}",
    response_model=schemas.ModuleResponse
)
def update_module(
    module_id: int,
    module: schemas.ModuleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    updated = crud.update_module(
        db,
        module_id,
        module
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )

    return updated
    
@router.delete("/modules/{module_id}")
def delete_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    success = crud.delete_module(
        db,
        module_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )

    return {
        "message": "Module deleted successfully"
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
    
@router.post(
    "/lessons/{lesson_id}/content",
    response_model=schemas.LessonContentResponse
)
def create_lesson_content(
    lesson_id: int,
    content: schemas.LessonContentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    db_content = crud.create_lesson_content(
        db,
        lesson_id,
        content
    )

    if db_content is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return db_content
    
@router.get(
    "/lessons/{lesson_id}/content",
    response_model=list[schemas.LessonContentResponse]
)
def get_lesson_contents(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.get_lesson_contents(
        db,
        lesson_id
    )
    
@router.get(
    "/content/{content_id}",
    response_model=schemas.LessonContentResponse
)
def get_lesson_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    content = crud.get_lesson_content(
        db,
        content_id
    )

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Content not found"
        )

    return content
    
@router.put(
    "/content/{content_id}",
    response_model=schemas.LessonContentResponse
)
def update_lesson_content(
    content_id: int,
    content: schemas.LessonContentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    updated = crud.update_lesson_content(
        db,
        content_id,
        content
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Content not found"
        )

    return updated
    
@router.delete("/content/{content_id}")
def delete_lesson_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    success = crud.delete_lesson_content(
        db,
        content_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Content not found"
        )

    return {
        "message": "Lesson content deleted successfully"
    }
