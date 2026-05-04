# Technical Decisions & API Contract

## Data Models

### User Entity
```json
{
  "user_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "age": 30
}
```

---

## API Specifications

### 1. Create User
**Endpoint:** `POST /users/`

**Query Parameters:**
- `first_name` (string, required) - Max 255 characters
- `last_name` (string, required) - Max 255 characters
- `email` (string, required) - Max 100 characters, unique
- `age` (integer, required) - Valid age value

**Response:** 
- Status: `200 OK`
- Body: Created user object with generated `user_id`

**Example:**
```bash
curl -X POST "http://localhost:8000/users/?first_name=John&last_name=Doe&email=john@example.com&age=30"
```

---

### 2. Get All Users
**Endpoint:** `GET /users/`

**Query Parameters:** None

**Response:**
- Status: `200 OK`
- Body: Array of user objects

**Example:**
```bash
curl -X GET "http://localhost:8000/users/"
```

---

### 3. Get User by ID
**Endpoint:** `GET /users/{user_id}`

**Path Parameters:**
- `user_id` (integer, required) - User's unique identifier

**Response:**
- Status: `200 OK`
- Body: User object if found, `null` if not found

**Example:**
```bash
curl -X GET "http://localhost:8000/users/1"
```

---

### 4. Update User
**Endpoint:** `PUT /users/{user_id}`

**Path Parameters:**
- `user_id` (integer, required) - User's unique identifier

**Query Parameters:**
- `first_name` (string, required) - Updated first name
- `last_name` (string, required) - Updated last name
- `email` (string, required) - Updated email
- `age` (integer, required) - Updated age

**Response:**
- Status: `200 OK`
- Body: Updated user object or `null` if user not found

**Example:**
```bash
curl -X PUT "http://localhost:8000/users/1?first_name=Jane&last_name=Doe&email=jane@example.com&age=28"
```

---

### 5. Delete User
**Endpoint:** `DELETE /users/{user_id}`

**Path Parameters:**
- `user_id` (integer, required) - User's unique identifier

**Response:**
- Status: `200 OK`
- Body: Deleted user object or `null` if user not found

**Example:**
```bash
curl -X DELETE "http://localhost:8000/users/1"
```

---

## Database Schema Details

### Users Table Constraints
- **Primary Key:** `user_id` (auto-increment)
- **Unique Constraint:** `email` (one email per user)
- **Field Constraints:**
  - `first_name`: VARCHAR(255), NOT NULL
  - `last_name`: VARCHAR(255), NOT NULL
  - `email`: VARCHAR(100), NOT NULL, UNIQUE
  - `age`: INTEGER, NOT NULL

---

## Error Handling (Current State)

**Current Limitation:** No explicit error handling implemented

**Potential Issues:**
- Duplicate email insertion → Database error (not caught)
- Invalid user_id → Returns None (should be 404)
- Missing required parameters → FastAPI validation error
- Database connection issues → Unhandled exception

**Recommended Error Responses:**
```json
{
  "detail": "User not found"
}
```

---

## Performance Considerations

### Query Optimization
- `get_users()` - Loads all users (no pagination)
  - **Issue:** Memory inefficient for large datasets
  - **Recommendation:** Implement pagination (limit, offset)

- `get_user()` - Indexed lookup by primary key
  - ✅ Good performance

- Email uniqueness - Database constraint
  - ✅ Ensures data integrity

---

## Security Considerations

### Current Issues:
1. **No Authentication** - All endpoints publicly accessible
2. **No Input Validation** - Direct string/int parameters accepted
3. **No Rate Limiting** - No protection against abuse
4. **No HTTPS** - Development setup without SSL/TLS
5. **SQL Injection** - Minimal risk (SQLAlchemy prevents it) but raw psycopg2 in insert_user.py uses parameterized queries correctly

### Recommended Improvements:
```python
# Use Pydantic for validation
from pydantic import BaseModel, EmailStr, validator

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int
    
    @validator('age')
    def age_valid(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Invalid age')
        return v

# Use in endpoint
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, **user.dict())
```

---

## Development Environment

### Required Setup:
1. Python 3.8+
2. PostgreSQL 12+
3. pip packages (see ARCHITECTURE.md)
4. `.env` file with `DATABASE_URL`

### Running Application:
```bash
# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Access interactive docs
open http://localhost:8000/docs
```

---

## Testing Checklist

- [ ] Create user with valid data
- [ ] Create user with duplicate email (should fail gracefully)
- [ ] Retrieve all users
- [ ] Retrieve specific user by ID
- [ ] Update user details
- [ ] Delete user
- [ ] Attempt to retrieve deleted user
- [ ] Update non-existent user
- [ ] Delete non-existent user
- [ ] Test with invalid data types

---

## Deployment Considerations

### For Production:
1. Use WSGI server (Gunicorn) instead of uvicorn
2. Implement proper logging
3. Add monitoring/alerting
4. Use connection pooling
5. Enable CORS appropriately
6. Implement rate limiting
7. Add request/response logging
8. Use environment-based configuration
9. Set up database backups
10. Implement graceful shutdown

**Example Production Run:**
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
