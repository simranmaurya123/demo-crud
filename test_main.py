import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set test database URL and JWT config before importing main
os.environ["DATABASE_URL"] = "sqlite:///./test_db.db"
os.environ["JWT_SECRET_KEY"] = "test-secret-key"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

from main import app, get_db
from users_model import User, Base

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Test user credentials
TEST_USER_REGISTER = {
    "first_name": "Test",
    "last_name": "User",
    "email": "testuser@example.com",
    "age": 30,
    "password": "testpassword123"
}

TEST_USER_LOGIN = {
    "email": "testuser@example.com",
    "password": "testpassword123"
}


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Setup test database before each test and cleanup after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user_token():
    """Register a test user and return auth token"""
    # Register user
    response = client.post("/auth/register", json=TEST_USER_REGISTER)
    assert response.status_code == 201
    
    # Login to get token
    response = client.post("/auth/login", json=TEST_USER_LOGIN)
    assert response.status_code == 200
    token = response.json()["access_token"]
    return token


class TestAuthRegister:
    """Test cases for POST /auth/register"""
    
    def test_register_success(self):
        """Test successful user registration"""
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "age": 30,
            "password": "securepass123"
        }
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["first_name"] == "John"
        assert data["email"] == "john@example.com"
        assert "password_hash" not in data  # Should not return password_hash
        assert "user_id" in data

    def test_register_duplicate_email(self):
        """Test registration fails with duplicate email"""
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "age": 30,
            "password": "securepass123"
        }
        client.post("/auth/register", json=payload)
        
        # Try registering with same email
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 409
        assert "already registered" in response.json()["detail"]

    def test_register_missing_password(self):
        """Test registration fails with missing password"""
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "age": 28
        }
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 422


class TestAuthLogin:
    """Test cases for POST /auth/login"""
    
    def test_login_success(self, test_user_token):
        """Test successful login returns token"""
        response = client.post("/auth/login", json=TEST_USER_LOGIN)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_email(self):
        """Test login fails with invalid email"""
        payload = {
            "email": "nonexistent@example.com",
            "password": "anypassword"
        }
        response = client.post("/auth/login", json=payload)
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

    def test_login_wrong_password(self, test_user_token):
        """Test login fails with wrong password"""
        payload = {
            "email": TEST_USER_LOGIN["email"],
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=payload)
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]


class TestAuthMe:
    """Test cases for GET /auth/me"""
    
    def test_get_current_user_success(self, test_user_token):
        """Test getting current authenticated user"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == TEST_USER_LOGIN["email"]
        assert data["first_name"] == TEST_USER_REGISTER["first_name"]

    def test_get_current_user_missing_token(self):
        """Test accessing /auth/me without token fails"""
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self):
        """Test accessing /auth/me with invalid token fails"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 401


class TestCreateUser:
    """Test cases for POST /users/"""
    
    def test_create_user_success(self, test_user_token):
        """Test successful user creation with valid data"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "age": 30
        }
        response = client.post("/users/", json=payload, headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
        assert data["email"] == "john@example.com"
        assert data["age"] == 30
        assert "user_id" in data

    def test_create_user_without_token(self):
        """Test creating user without authentication fails"""
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "age": 30
        }
        response = client.post("/users/", json=payload)
        assert response.status_code == 401

    def test_create_user_missing_field(self, test_user_token):
        """Test user creation fails with missing required field"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
            # Missing age field
        }
        response = client.post("/users/", json=payload, headers=headers)
        assert response.status_code == 422

    def test_create_multiple_users(self, test_user_token):
        """Test creating multiple users"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        users_data = [
            {"first_name": "Alice", "last_name": "White", "email": "alice@example.com", "age": 25},
            {"first_name": "Bob", "last_name": "Black", "email": "bob@example.com", "age": 35},
        ]
        
        for user_data in users_data:
            response = client.post("/users/", json=user_data, headers=headers)
            assert response.status_code == 201


class TestReadUsers:
    """Test cases for GET /users/"""
    
    def test_read_users_empty(self, test_user_token):
        """Test reading users when no additional users exist"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/users/", headers=headers)
        assert response.status_code == 200
        # The test user itself is in the database, so there's at least 1 user
        assert len(response.json()) >= 1

    def test_read_users_with_data(self, test_user_token):
        """Test reading users when database has data"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        # Create a user first
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "age": 30
        }
        client.post("/users/", json=payload, headers=headers)
        
        # Read users
        response = client.get("/users/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_read_users_without_token(self):
        """Test reading users without authentication fails"""
        response = client.get("/users/")
        assert response.status_code == 401


class TestReadUserById:
    """Test cases for GET /users/{user_id}"""
    
    def test_read_user_success(self, test_user_token):
        """Test reading a specific user"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        # Create a user
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "age": 30
        }
        create_response = client.post("/users/", json=payload, headers=headers)
        user_id = create_response.json()["user_id"]
        
        # Read the user
        response = client.get(f"/users/{user_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == user_id
        assert data["first_name"] == "John"

    def test_read_user_without_token(self):
        """Test reading user without authentication fails"""
        response = client.get("/users/1")
        assert response.status_code == 401


class TestUpdateUser:
    """Test cases for PUT /users/{user_id}"""
    
    def test_update_user_success(self, test_user_token):
        """Test successful user update"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        # Create a user
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "age": 30
        }
        create_response = client.post("/users/", json=payload, headers=headers)
        user_id = create_response.json()["user_id"]
        
        # Update the user
        update_payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "age": 28
        }
        response = client.put(f"/users/{user_id}", json=update_payload, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Jane"
        assert data["last_name"] == "Smith"
        assert data["age"] == 28

    def test_update_user_without_token(self):
        """Test updating user without authentication fails"""
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "age": 28
        }
        response = client.put("/users/1", json=payload)
        assert response.status_code == 401


class TestDeleteUser:
    """Test cases for DELETE /users/{user_id}"""
    
    def test_delete_user_success(self, test_user_token):
        """Test successful user deletion"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        # Create a user
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "age": 30
        }
        create_response = client.post("/users/", json=payload, headers=headers)
        user_id = create_response.json()["user_id"]
        
        # Delete the user
        response = client.delete(f"/users/{user_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["user_id"] == user_id

    def test_delete_user_without_token(self):
        """Test deleting user without authentication fails"""
        response = client.delete("/users/1")
        assert response.status_code == 401
