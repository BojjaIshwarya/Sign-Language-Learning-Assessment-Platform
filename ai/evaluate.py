from tensorflow.keras.models import load_model

from ai.config import MODEL_PATH
from ai.preprocessing import preprocess_asl


def evaluate():
    """
    Evaluate the trained CNN model on the validation dataset.
    """

    # Load validation data
    _, validation_generator = preprocess_asl(
        image_size=(64, 64),
        batch_size=32
    )

    # Load trained model
    model = load_model(MODEL_PATH)

    # Evaluate
    loss, accuracy = model.evaluate(
        validation_generator,
        verbose=1
    )

    print("\n========== MODEL EVALUATION ==========")
    print(f"Validation Loss     : {loss:.4f}")
    print(f"Validation Accuracy : {accuracy * 100:.2f}%")
    print("======================================\n")


if __name__ == "__main__":
    evaluate()
