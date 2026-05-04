# Quick Reference Guide

## Project at a Glance

**Type:** FastAPI REST API for User Management  
**Database:** PostgreSQL  
**ORM:** SQLAlchemy  
**Entry Point:** `main.py`

---

## File Reference

| File | Purpose | Key Functions/Classes |
|------|---------|----------------------|
| `main.py` | FastAPI application & routes | `app`, `get_db()`, 5 endpoints |
| `crud.py` | Business logic | `create_user()`, `get_user()`, `get_users()`, `update_user()`, `delete_user()` |
| `models.py` | Database schema | `User` class |
| `database.py` | DB config | `engine`, `SessionLocal`, `Base` |
| `db_connect.py` | Direct connection | `get_connection()` |
| `insert_user.py` | CLI tool | `insert_user()` function |

---

## API Endpoints

```bash
# Create user
POST /users/?first_name=John&last_name=Doe&email=john@example.com&age=30

# Get all users
GET /users/

# Get user by ID
GET /users/1

# Update user
PUT /users/1?first_name=Jane&last_name=Doe&email=jane@example.com&age=25

# Delete user
DELETE /users/1
```

---

## Database Setup

1. Create PostgreSQL database
2. Create `.env` file with:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   ```
3. Run the application (SQLAlchemy will create tables automatically)

---

## Common Tasks

### Add a new field to User model:
1. Update `models.py` - add column to User class
2. Update `crud.py` - include new field in functions
3. Update `main.py` - add parameter to endpoints

### Run the API:
```bash
uvicorn main:app --reload
```

### Test an endpoint:
```bash
curl -X GET http://localhost:8000/users/
```

---

## Architecture Pattern

- **API Layer:** Handles HTTP requests/responses
- **Business Layer:** Contains CRUD logic
- **Data Layer:** Manages database operations via SQLAlchemy
- **Database:** PostgreSQL

---

## Next Steps to Improve

1. Add Pydantic models for validation
2. Add error handling (try-except blocks)
3. Add authentication/authorization
4. Add comprehensive logging
5. Write unit tests
6. Use database migrations (Alembic)
7. Add input validation on all endpoints
