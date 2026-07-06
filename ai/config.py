from pathlib import Path

# Project Root (Sign_pro/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Dataset paths
DATASETS_DIR = PROJECT_ROOT / "datasets"

ASL_DATASET = DATASETS_DIR / "asl_alphabet"
ASL_TRAIN = (
    ASL_DATASET
    / "asl_alphabet_train"
    / "asl_alphabet_train"
)

ASL_TEST = (
    ASL_DATASET
    / "asl_alphabet_test"
    / "asl_alphabet_test"
)

MNIST_DATASET = DATASETS_DIR / "sign_mnist"
MNIST_TRAIN = MNIST_DATASET / "sign_mnist_train.csv"
MNIST_TEST = MNIST_DATASET / "sign_mnist_test.csv"

WLASL_DATASET = DATASETS_DIR / "wlasl"
RWTH_DATASET = DATASETS_DIR / "rwth_phoenix"

# Model directory
MODEL_DIR = Path(__file__).resolve().parent / "models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "gesture_classifier.keras"
