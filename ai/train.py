from pathlib import Path

from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint
)

from ai.config import MODEL_PATH
from ai.model import build_model
from ai.preprocessing import preprocess_asl


def train():
    # Load dataset
    train_generator, validation_generator = preprocess_asl(
        image_size=(64, 64),
        batch_size=32
    )

    # Build model
    model = build_model(num_classes=train_generator.num_classes)

    # Ensure model directory exists
    Path(MODEL_PATH).parent.mkdir(parents=True, exist_ok=True)

    # Callbacks
    checkpoint = ModelCheckpoint(
        filepath=str(MODEL_PATH),
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1
    )

    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
        verbose=1
    )

    # Train
    history = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=5,
        callbacks=[
            checkpoint,
            early_stopping
        ]
    )

    return history


if __name__ == "__main__":
    train()
