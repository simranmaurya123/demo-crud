# Project Architecture Documentation

## 1. Overview

This is a **FastAPI-based REST API application** for managing user data. It implements a layered architecture pattern with clear separation of concerns between API endpoints, business logic, and database operations.

**Primary Purpose:** Provide RESTful CRUD operations for user management with PostgreSQL database persistence.

---

## 2. Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | FastAPI | High-performance web framework for REST APIs |
| **Database** | PostgreSQL | Relational database for persistent data storage |
| **ORM** | SQLAlchemy | Object-Relational Mapping for database interactions |
| **Database Driver** | psycopg2 | Python-PostgreSQL adapter (used in legacy scripts) |
| **Config Management** | python-dotenv | Environment variable management |

---

## 3. Project Structure

```
project/
├── main.py              # FastAPI application & REST API endpoints
├── models.py            # SQLAlchemy ORM models
├── database.py          # Database configuration & session factory
├── crud.py              # CRUD business logic functions
├── db_connect.py        # Direct PostgreSQL connection (legacy)
├── insert_user.py       # User insertion script (legacy/utility)
├── __pycache__/         # Python cache files
├── package_needed/      # Dependencies folder
└── docs/                # Architecture documentation
```

---

## 4. Architecture Layers

The application follows a **3-tier layered architecture:**

```
┌─────────────────────────────────────┐
│      API LAYER (main.py)            │
│   - FastAPI routes & endpoints      │
│   - HTTP request handling           │
│   - Dependency injection (db session)
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│   BUSINESS LOGIC LAYER (crud.py)    │
│   - CRUD operations                 │
│   - Data validation & processing    │
│   - Query execution                 │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│    DATA ACCESS LAYER                │
│  ┌──────────────────────────────┐   │
│  │ models.py: ORM entities      │   │
│  │ database.py: SQLAlchemy cfg  │   │
│  └──────────────────────────────┘   │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│   DATABASE LAYER                    │
│   PostgreSQL Database               │
└─────────────────────────────────────┘
```

---

## 5. Component Descriptions

### 5.1 API Layer (`main.py`)

**Responsibility:** Handle HTTP requests and responses

- Defines FastAPI application instance
- Implements 5 REST API endpoints for user management
- Uses dependency injection (`get_db()`) to provide database sessions
- All endpoints delegate business logic to CRUD module

**Endpoints:**
- `POST /users/` - Create new user
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user details
- `DELETE /users/{user_id}` - Delete user

### 5.2 Business Logic Layer (`crud.py`)

**Responsibility:** Implement CRUD operations

- `create_user()` - Create and persist new user
- `get_users()` - Fetch all users from database
- `get_user()` - Fetch specific user by ID
- `update_user()` - Modify user attributes
- `delete_user()` - Remove user from database

All functions accept SQLAlchemy `Session` object and return User model instances or None.

### 5.3 Models Layer (`models.py`)

**Responsibility:** Define data structure and schema

- **User Model:** SQLAlchemy ORM class mapped to `users` table
  - `user_id` (INT, PRIMARY KEY) - Unique identifier
  - `first_name` (VARCHAR 255) - User's first name
  - `last_name` (VARCHAR 255) - User's last name
  - `email` (VARCHAR 100, UNIQUE) - User's email address
  - `age` (INT) - User's age

### 5.4 Database Configuration (`database.py`)

**Responsibility:** Initialize and manage database connections

- **Engine:** SQLAlchemy engine configured with DATABASE_URL from environment
- **SessionLocal:** Session factory for creating database sessions
- **Base:** Declarative base for ORM models
- Loads configuration from `.env` file (via `python-dotenv`)

### 5.5 Database Connection (`db_connect.py`)

**Responsibility:** Direct PostgreSQL connectivity (legacy support)

- Provides `get_connection()` function for raw psycopg2 connections
- Used in `insert_user.py` script
- Loads database credentials from environment variables

### 5.6 Utility Script (`insert_user.py`)

**Responsibility:** Command-line user insertion tool

- Standalone script for inserting users via direct database connection
- Prompts user for input (first name, last name, email, age)
- Executes raw SQL INSERT statement
- Not integrated with main FastAPI application

---

## 6. Data Flow

### Create User Flow:
```
HTTP POST /users/ 
    ↓
main.py: create_user() endpoint
    ↓
crud.py: create_user() function
    ↓
models.py: User model instantiation
    ↓
database.py: SessionLocal (SQLAlchemy session)
    ↓
PostgreSQL: INSERT INTO users table
    ↓
ORM: Refresh user object with ID
    ↓
HTTP Response: Created user object (JSON)
```

### Read User Flow:
```
HTTP GET /users/{user_id}
    ↓
main.py: read_user() endpoint
    ↓
crud.py: get_user() function
    ↓
database.py: Query execution via session
    ↓
PostgreSQL: SELECT FROM users WHERE user_id
    ↓
models.py: Map result to User object
    ↓
HTTP Response: User data (JSON)
```

---

## 7. Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INTEGER NOT NULL
);
```

**Indexes:**
- Primary key on `user_id` (auto-indexed)
- Unique index on `email`

---

## 8. Configuration Management

Environment variables are loaded from `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DB_NAME=dbname
DB_USER=username
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

**Note:** Database credentials are not hardcoded; must be provided via `.env` file.

---

## 9. Key Design Patterns

### 9.1 Dependency Injection
- FastAPI's `Depends()` mechanism injects database session into route handlers
- Ensures proper session lifecycle management (creation, cleanup)

### 9.2 Layered Architecture
- Clear separation between API, business logic, and data access layers
- Improves maintainability, testability, and scalability

### 9.3 ORM Pattern
- SQLAlchemy ORM abstracts SQL queries into Python objects
- Provides type safety and reduces SQL injection risks

### 9.4 CRUD Pattern
- All database operations centralized in `crud.py`
- Makes business logic reusable and testable

---

## 10. Current Issues & Recommendations

### Issues:
1. **Mixed Database Approaches:** Both SQLAlchemy ORM (main.py) and raw psycopg2 (insert_user.py) are used
   - **Recommendation:** Use SQLAlchemy consistently throughout
   
2. **Missing Error Handling:** No try-catch blocks in CRUD operations or API endpoints
   - **Recommendation:** Add proper exception handling and HTTP error responses

3. **No Input Validation:** API endpoints accept raw string/int parameters
   - **Recommendation:** Use Pydantic models for request/response validation

4. **No Authentication/Authorization:** All endpoints are publicly accessible
   - **Recommendation:** Implement JWT or API key authentication

5. **Missing Database Created:** Schema doesn't show how tables are created
   - **Recommendation:** Use SQLAlchemy migrations (Alembic) or initialization script

### Recommended Enhancements:
- Add Pydantic schemas for API request/response validation
- Implement structured logging
- Add unit and integration tests
- Use SQLAlchemy migrations (Alembic)
- Add API documentation (Swagger/OpenAPI)
- Implement proper error handling with custom exceptions
- Add authentication and authorization layers

---

## 11. Dependencies

Based on the imports used:

- `fastapi` - Web framework
- `sqlalchemy` - ORM library
- `psycopg2` - PostgreSQL driver
- `python-dotenv` - Environment configuration

**Installation:**
```bash
pip install fastapi sqlalchemy psycopg2-binary python-dotenv uvicorn
```

---

## 12. How to Run

### 1. Start the Application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

Swagger documentation available at `http://localhost:8000/docs`

### 2. Run Insert Script (Legacy):
```bash
python insert_user.py
```

---

## 13. Summary

This project demonstrates a fundamental REST API with proper separation of concerns using FastAPI and SQLAlchemy. It's suitable for small to medium-scale applications but would benefit from:

- Standardized error handling
- Input validation
- Authentication
- Database migrations
- Comprehensive testing

The architecture is clean and maintainable, making it easy to extend with new features or improvements.
