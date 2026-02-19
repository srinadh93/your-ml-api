from fastapi.testclient import TestClient
from src.main import app
import pytest
from unittest.mock import patch, MagicMock
import io
from PIL import Image
import numpy as np

client = TestClient(app)


def test_health_check_endpoint():
    """Test the /health endpoint to ensure it returns a 200 OK status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "model is loaded" in response.json()["message"].lower()


# Use patches to mock the heavy ML model operations during unit tests
@patch('src.main.predict_image')
@patch('src.main.preprocess_image')
def test_predict_success_with_mocked_model(mock_preprocess_image, mock_predict_image):
    """Test successful prediction with mocked model."""
    # Configure mocks to return predefined values for controlled testing
    mock_preprocess_image.return_value = np.array([[[[0.1, 0.2, 0.3]]]])
    mock_predict_image.return_value = {
        "class_label": "dog",
        "probabilities": [0.05, 0.95, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }

    # Create a dummy image file in-memory for the test request
    dummy_image = Image.new('RGB', (32, 32), color='blue')
    img_byte_arr = io.BytesIO()
    dummy_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)  # Reset stream position to the beginning

    # Send a POST request to the /predict endpoint
    response = client.post(
        "/predict",
        files={
            "file": ("test_image.png", img_byte_arr, "image/png")
        }
    )
    # Assert the response status code and content
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["class_label"] == "dog"
    assert len(response_data["probabilities"]) == 10
    # Verify that the mocked functions were called as expected
    mock_preprocess_image.assert_called_once()
    mock_predict_image.assert_called_once()


def test_predict_invalid_file_type_handling():
    """Test behavior when an unsupported file type is sent."""
    response = client.post(
        "/predict",
        files={
            "file": ("document.txt", b"This is not an image.", "text/plain")
        }
    )
    # Assert that the API correctly rejects invalid file types with a 400 status
    assert response.status_code == 400
    assert "Only image files (e.g., JPEG, PNG) are allowed for prediction." in response.json()["detail"]


def test_predict_missing_file_upload():
    """Test behavior when no file is uploaded."""
    response = client.post(
        "/predict",
        data={}
    )
    # FastAPI automatically handles missing required fields with a 422 Unprocessable Entity
    assert response.status_code == 422
    assert "field required" in response.json()["detail"][0]["msg"].lower()


@patch('src.main.predict_image')
@patch('src.main.preprocess_image')
def test_predict_with_jpg_image(mock_preprocess_image, mock_predict_image):
    """Test prediction with a JPG image file."""
    mock_preprocess_image.return_value = np.array([[[[0.1, 0.2, 0.3]]]])
    mock_predict_image.return_value = {
        "class_label": "cat",
        "probabilities": [0.0, 0.0, 0.0, 0.8, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0]
    }

    dummy_image = Image.new('RGB', (32, 32), color='red')
    img_byte_arr = io.BytesIO()
    dummy_image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    response = client.post(
        "/predict",
        files={
            "file": ("test_image.jpg", img_byte_arr, "image/jpeg")
        }
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["class_label"] == "cat"


@patch('src.main.preprocess_image')
def test_predict_with_corrupted_image(mock_preprocess_image):
    """Test behavior when a corrupted image is sent."""
    mock_preprocess_image.side_effect = ValueError("Error processing image: cannot identify image file")

    response = client.post(
        "/predict",
        files={
            "file": ("corrupted.png", b"This is corrupted data", "image/png")
        }
    )

    assert response.status_code == 422
    assert "Image processing failed" in response.json()["detail"]


@patch('src.main.predict_image')
@patch('src.main.preprocess_image')
def test_predict_response_structure(mock_preprocess_image, mock_predict_image):
    """Test that prediction response has the correct structure."""
    mock_preprocess_image.return_value = np.array([[[[0.1, 0.2, 0.3]]]])
    mock_predict_image.return_value = {
        "class_label": "airplane",
        "probabilities": [0.9, 0.05, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }

    dummy_image = Image.new('RGB', (32, 32), color='green')
    img_byte_arr = io.BytesIO()
    dummy_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    response = client.post(
        "/predict",
        files={
            "file": ("test_image.png", img_byte_arr, "image/png")
        }
    )

    assert response.status_code == 200
    response_data = response.json()
    
    # Check structure
    assert "class_label" in response_data
    assert "probabilities" in response_data
    assert isinstance(response_data["class_label"], str)
    assert isinstance(response_data["probabilities"], list)
    assert len(response_data["probabilities"]) == 10
