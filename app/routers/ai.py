from fastapi import APIRouter

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.get("/")
def ai_home():
    return {
        "message": "AI module is working."
    }


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "Random Forest Landmark Classifier",
        "dataset": "ASL Alphabet"
    }
