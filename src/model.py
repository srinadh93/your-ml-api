import numpy as np
from PIL import Image
import io
import os

# Try to import tensorflow first, fall back to keras if not available
keras_available = False
try:
    import tensorflow as tf
    keras = tf.keras
    keras_available = True
except ImportError:
    try:
        import keras
        keras_available = True
    except ImportError:
        keras = None
        keras_available = False

# Global variable to hold the loaded model
MODEL = None
# Define target image size based on your model's input requirements
IMAGE_SIZE = (32, 32)  # CIFAR-10 standard size
CLASS_LABELS = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]  # CIFAR-10 class labels


def load_model(model_path: str = None):
    """Load the pre-trained Keras model once globally."""
    global MODEL
    if MODEL is None:
        # Default model path, can be overridden by environment variable
        effective_model_path = (
            model_path
            if model_path
            else os.environ.get("MODEL_PATH", "models/my_classifier_model.h5")
        )
        if not os.path.exists(effective_model_path):
            raise FileNotFoundError(f"Model file not found at {effective_model_path}")
        
        if not keras_available:
            raise ImportError(
                "TensorFlow/Keras not available. "
                "Please install keras or tensorflow: pip install keras or pip install tensorflow"
            )
        
        try:
            MODEL = keras.models.load_model(effective_model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load model from {effective_model_path}: {e}")
    
    return MODEL


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Preprocess image from bytes to model input format."""
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize(IMAGE_SIZE)
        image_array = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
        # Add batch dimension (batch_size, height, width, channels)
        image_array = np.expand_dims(image_array, axis=0)
        return image_array
    except Exception as e:
        raise ValueError(f"Error processing image: {e}")


def predict_image(preprocessed_image: np.ndarray):
    """Make a prediction on preprocessed image."""
    model = load_model()  # Ensure model is loaded
    predictions = model.predict(preprocessed_image, verbose=0)
    # Convert raw predictions (e.g., softmax outputs) into meaningful class labels and probabilities
    predicted_class_idx = np.argmax(predictions, axis=1)[0]
    probabilities = predictions[0].tolist()  # Convert numpy array to list for JSON serialization

    return {
        "class_label": CLASS_LABELS[predicted_class_idx],
        "probabilities": probabilities,
    }
