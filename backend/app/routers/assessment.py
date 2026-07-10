from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import get_db
from app import models
from fastapi import APIRouter, UploadFile, File, Form
import numpy as np
import cv2

from ai.feature_extractor import extract_features
from ai.predictor import predict

router = APIRouter(
    prefix="/assessment",
    tags=["Assessment"]
)


@router.post("/predict")
async def predict_sign(
    expected_sign: str = Form(...),
    learner_profile_id: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    image_bytes = await image.read()

    np_image = np.frombuffer(image_bytes, np.uint8)

    frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    features = extract_features(frame)

    if features is None:
        return {
            "success": False,
            "message": "No hand detected."
        }

    predicted_sign, confidence = predict(features)
    
    score = 100 if expected_sign == predicted_sign else 0

    if predicted_sign == expected_sign:

        if confidence >= 95:

            feedback = "Excellent! Your sign is highly accurate."

        elif confidence >= 80:

            feedback = "Good job! Practice a little more for better accuracy."

        else:

            feedback = "Correct sign detected, but confidence is low. Keep practicing."

    else:

        feedback = (
        f"Incorrect sign detected. Expected '{expected_sign}', "
        f"but recognized '{predicted_sign}'. Please practice this lesson again."
    )
    
    assessment = models.AssessmentHistory(
        learner_profile_id=learner_profile_id,
        assessment_name="Alphabet Assessment",
        score=score,
        level="Beginner",
        expected_sign=expected_sign,
        predicted_sign=predicted_sign,
        confidence=confidence,
        feedback=feedback
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return {
        "success": True,
        "assessment_id": assessment.id,
        "expected_sign": expected_sign,
        "predicted_sign": predicted_sign,
        "confidence": round(confidence, 4),
        "correct": expected_sign == predicted_sign,
        "feedback": feedback,
    }
