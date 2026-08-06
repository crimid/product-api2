import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app
import os
import tempfile

@pytest.fixture(scope="function")
def client():
    """Create a test client for the FastAPI app."""
    # Use a temporary file for test database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)
    test_db_url = f"sqlite:///{db_path}"
    
    # Create test engine
    test_engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    
    # Create tables
    SQLModel.metadata.create_all(test_engine)
    
    # Override the database dependency
    def get_test_session():
        with Session(test_engine) as session:
            yield session
    
    from app.database.session import get_session
    app.dependency_overrides[get_session] = get_test_session
    
    # Create test client
    with TestClient(app) as test_client:
        yield test_client
    
    # Cleanup
    app.dependency_overrides.clear()
    test_engine.dispose()
    
    # Remove the temporary file
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except PermissionError:
            pass

@pytest.fixture
def test_user():
    """Create a test user for authentication tests."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }

@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for protected endpoints."""
    # Register user
    client.post("/register", json=test_user)
    
    # Login
    response = client.post(
        "/login",
        data={"username": test_user["username"], "password": test_user["password"]}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_product():
    """Create a sample product for tests."""
    return {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 99.99,
        "stock": 10
    }
