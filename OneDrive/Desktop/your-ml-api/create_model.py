#!/usr/bin/env python3
"""
Script to create a simple CIFAR-10 image classification model for the ML API.
This creates a lightweight CNN trained on CIFAR-10 dataset.
"""

import os
import sys
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

def create_simple_cifar_model():
    """Create and train a simple CIFAR-10 classification model."""
    
    print("Loading CIFAR-10 dataset...")
    (x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
    
    # Normalize pixel values
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    
    # For quick demo, use only a subset of data
    x_train = x_train[:5000]
    y_train = y_train[:5000]
    x_test = x_test[:1000]
    y_test = y_test[:1000]
    
    print("Building model architecture...")
    model = keras.Sequential([
        layers.Input(shape=(32, 32, 3)),
        
        # First convolutional block
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2),
        layers.Dropout(0.25),
        
        # Second convolutional block
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2),
        layers.Dropout(0.25),
        
        # Third convolutional block
        layers.Conv2D(128, 3, padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(128, 3, padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2),
        layers.Dropout(0.25),
        
        # Flatten and dense layers
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')  # 10 CIFAR-10 classes
    ])
    
    print("Compiling model...")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("Training model (this will take a moment)...")
    model.fit(
        x_train, y_train,
        batch_size=128,
        epochs=5,  # Quick training
        validation_split=0.2,
        verbose=1
    )
    
    print("\nEvaluating on test set...")
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"Test accuracy: {test_accuracy:.4f}")
    
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    print("\nSaving model...")
    model_path = "models/my_classifier_model.h5"
    model.save(model_path)
    print(f"Model saved to {model_path}")
    
    # Verify model can be loaded
    print("\nVerifying model load...")
    loaded_model = keras.models.load_model(model_path)
    print("Model loaded successfully!")
    
    # Test prediction
    print("\nTesting prediction on random image...")
    test_image = np.random.random((1, 32, 32, 3))
    prediction = loaded_model.predict(test_image, verbose=0)
    predicted_class = np.argmax(prediction[0])
    confidence = prediction[0][predicted_class]
    print(f"Sample prediction: Class {predicted_class}, Confidence: {confidence:.4f}")
    
    print("\n✅ Model creation complete!")
    return model_path

if __name__ == "__main__":
    try:
        model_path = create_simple_cifar_model()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error creating model: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
