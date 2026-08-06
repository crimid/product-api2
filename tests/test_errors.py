import pytest
from tests.conftest import client, auth_headers

def test_404_error(client):
    """Test 404 error handling."""
    response = client.get("/non-existent-endpoint")
    assert response.status_code == 404
    data = response.json()
    # FastAPI returns a different format for 404 errors
    assert "detail" in data or "error" in data

def test_validation_error(client, auth_headers):
    """Test validation error handling."""
    product_data = {
        "name": "",
        "description": "This is a test product",
        "price": -10,
        "stock": -5
    }
    response = client.post("/products", json=product_data, headers=auth_headers)
    # Validation errors in FastAPI return 422 Unprocessable Entity
    assert response.status_code == 422
    data = response.json()
    # Check that the response contains validation error details
    assert "detail" in data

def test_unauthorized_access(client):
    """Test unauthorized access to protected endpoints."""
    response = client.get("/users/me")
    assert response.status_code == 401

def test_invalid_token(client):
    """Test access with invalid token."""
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/products", headers=headers)
    assert response.status_code == 401
