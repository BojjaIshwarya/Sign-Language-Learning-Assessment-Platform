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
    image: UploadFile = File(...)
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

    return {
        "success": True,
        "expected_sign": expected_sign,
        "predicted_sign": predicted_sign,
        "confidence": round(confidence, 4),
        "correct": expected_sign == predicted_sign
    }
