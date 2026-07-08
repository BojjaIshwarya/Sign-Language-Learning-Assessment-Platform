import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from ai.config import (
    ASL_TRAIN,
    MNIST_TRAIN,
    MNIST_TEST
)


def load_asl_dataset(image_size=(64, 64), batch_size=32):
    """
    Load ASL Alphabet Dataset.

    Uses validation_split because the provided
    asl_alphabet_test folder contains only one
    sample image per class.
    """

    datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        validation_split=0.2
    )

    train_generator = datagen.flow_from_directory(
        ASL_TRAIN,
        target_size=image_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="training",
        shuffle=True
    )

    validation_generator = datagen.flow_from_directory(
        ASL_TRAIN,
        target_size=image_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="validation",
        shuffle=False
    )

    return train_generator, validation_generator


def load_mnist_dataset():
    """
    Load Sign Language MNIST CSV files.
    """

    train_df = pd.read_csv(MNIST_TRAIN)
    test_df = pd.read_csv(MNIST_TEST)

    return train_df, test_df
