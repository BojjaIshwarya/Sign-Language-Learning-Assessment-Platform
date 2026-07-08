import numpy as np
from tensorflow.keras.utils import to_categorical

from ai.dataset_loader import (
    load_asl_dataset,
    load_mnist_dataset
)


def preprocess_asl(image_size=(64, 64), batch_size=32):
    """
    Load and preprocess the ASL Alphabet Dataset.

    Returns:
        train_generator
        validation_generator
    """

    train_generator, validation_generator = load_asl_dataset(
        image_size=image_size,
        batch_size=batch_size
    )

    return train_generator, validation_generator


def preprocess_mnist():
    """
    Load and preprocess the Sign Language MNIST dataset.

    Returns:
        x_train
        y_train
        x_test
        y_test
    """

    # Load CSV files
    train_df, test_df = load_mnist_dataset()

    # Separate labels and images
    y_train = train_df.iloc[:, 0].values
    y_test = test_df.iloc[:, 0].values

    x_train = train_df.iloc[:, 1:].values
    x_test = test_df.iloc[:, 1:].values

    # Normalize pixel values
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    # Reshape to (28,28,1)
    x_train = x_train.reshape((-1, 28, 28, 1))
    x_test = x_test.reshape((-1, 28, 28, 1))

    # -------------------------------------------------------
    # Remap labels because Sign Language MNIST skips J and Z
    # Original labels:
    # 0,1,2,3,4,5,6,7,8,10,11,...24
    # -------------------------------------------------------

    unique_labels = sorted(np.unique(y_train))

    label_map = {
        label: index
        for index, label in enumerate(unique_labels)
    }

    y_train = np.array(
        [label_map[label] for label in y_train]
    )

    y_test = np.array(
        [label_map[label] for label in y_test]
    )

    num_classes = len(unique_labels)

    # One-hot encoding
    y_train = to_categorical(
        y_train,
        num_classes=num_classes
    )

    y_test = to_categorical(
        y_test,
        num_classes=num_classes
    )

    return (
        x_train,
        y_train,
        x_test,
        y_test
    )
