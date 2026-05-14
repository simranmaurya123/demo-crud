# User Management REST API

A modern, fast REST API built with **FastAPI** and **SQLAlchemy** for managing user data. This project demonstrates clean architecture principles with proper separation of concerns between API routes, business logic, and data access layers.

## 🚀 Features

- ✅ **Full CRUD Operations** - Create, Read, Update, Delete users
- ✅ **FastAPI** - Modern, high-performance web framework with automatic API documentation
- ✅ **SQLAlchemy ORM** - Object-relational mapping for database interactions
- ✅ **PostgreSQL** - Robust relational database for data persistence
- ✅ **Environment Configuration** - Secure credential management via `.env`
- ✅ **Layered Architecture** - Clean separation between API, business logic, and data layers
- ✅ **Auto-generated API Docs** - Swagger UI and ReDoc documentation

## 📋 Prerequisites

- **Python 3.8** or higher
- **PostgreSQL 12** or higher
- **pip** (Python package manager)

## 🔧 Installation

### 1. Clone or Download the Project
```bash
cd c:\Users\Developer\Desktop\Project
```

### 2. Create a Python Virtual Environment (Recommended)
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install fastapi sqlalchemy psycopg2-binary python-dotenv uvicorn python-jose[cryptography] passlib[bcrypt]
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Replace the values with your PostgreSQL credentials and generate a secure JWT_SECRET_KEY.**

### 6. Create Database Tables

Run the application once to let SQLAlchemy create the database tables:
```bash
uvicorn main:app --reload
```

The `users` table will be created automatically on first run.

## 🏃 Running the Application

### Start the Development Server
```bash
uvicorn main:app --reload
```

The API will be available at: **http://localhost:8000**

### Access API Documentation

- **Swagger UI (Interactive):** http://localhost:8000/docs
- **ReDoc (Alternative):** http://localhost:8000/redoc

## 📡 API Endpoints

### Base URL
```
http://localhost:8000
```

### Authentication Endpoints

#### 1. Register a New User
```http
POST /auth/register
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "age": 30,
  "password": "securepassword123"
}
```

**Response (201):**
```json
{
  "user_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "age": 30
}
```

#### 2. Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 3. Get Current User
```http
GET /auth/me
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "user_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "age": 30
}
```

### Protected CRUD Endpoints (Require Authentication)

**All CRUD endpoints now require a valid JWT token in the Authorization header:**

```
Authorization: Bearer {access_token}
```

#### 1. Create a New User
```http
POST /users/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@example.com",
  "age": 28
}
```

**Response (201):**
```json
{
  "user_id": 2,
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@example.com",
  "age": 28
}
```

#### 2. Get All Users
```http
GET /users/
Authorization: Bearer {access_token}
```

**Response (200):**
```json
[
  {
    "user_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "age": 30
  }
]
```

#### 3. Get User by ID
```http
GET /users/1
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "user_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "age": 30
}
```

#### 4. Update User
```http
PUT /users/1
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "first_name": "Jonathan",
  "last_name": "Doe",
  "email": "jonathan@example.com",
  "age": 31
}
```

**Response (200):**
```json
{
  "user_id": 1,
  "first_name": "Jonathan",
  "last_name": "Doe",
  "email": "jonathan@example.com",
  "age": 31
}
```

#### 5. Delete User
```http
DELETE /users/1
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "user_id": 1,
  "first_name": "Jonathan",
  "last_name": "Doe",
  "email": "jonathan@example.com",
  "age": 31
}
```

## 📚 Testing with cURL

```bash
# Create user
curl -X POST "http://localhost:8000/users/?first_name=John&last_name=Doe&email=john@example.com&age=30"

# Get all users
curl -X GET "http://localhost:8000/users/"

# Get user by ID
curl -X GET "http://localhost:8000/users/1"

# Update user
curl -X PUT "http://localhost:8000/users/1?first_name=Jane&last_name=Doe&email=jane@example.com&age=28"

# Delete user
curl -X DELETE "http://localhost:8000/users/1"
```

## 📁 Project Structure

```
project/
├── main.py                    # FastAPI application and endpoints
├── crud.py                    # CRUD business logic functions
├── models.py                  # SQLAlchemy ORM models
├── database.py                # Database configuration
├── db_connect.py              # Direct database connection (legacy)
├── insert_user.py             # Command-line user insertion tool
├── .env                       # Environment variables (create this)
├── README.md                  # This file
├── docs/                      # Architecture documentation
│   ├── ARCHITECTURE.md        # Detailed architecture overview
│   ├── QUICK_REFERENCE.md     # Developer quick reference
│   └── TECHNICAL_SPECIFICATIONS.md  # API and technical specs
└── package_needed/            # Dependencies folder
```

## 🗄️ Database Schema

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

**Constraints:**
- `user_id` is auto-incrementing primary key
- `email` must be unique
- All fields are required (NOT NULL)

## 🛠️ Development

### Code Structure

- **`main.py`** - FastAPI app instance and all HTTP endpoints
- **`crud.py`** - All database CRUD operations
- **`models.py`** - SQLAlchemy User model definition
- **`database.py`** - Database session factory and engine setup

### Adding a New Field to User

1. Update the model in `models.py`:
```python
class User(Base):
    __tablename__="users"
    user_id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String(255))
    last_name=Column(String(255))
    email=Column(String(100),unique=True)
    age=Column(Integer)
    new_field=Column(String(100))  # Add new column
```

2. Update CRUD functions in `crud.py` to include the new field

3. Update all endpoints in `main.py` to accept the new parameter

## 🔒 Security Notes

**Current Implementation Notes:**
- No authentication/authorization implemented
- Consider adding JWT token-based authentication for production
- Input validation should be added using Pydantic models
- Consider implementing rate limiting
- Use HTTPS in production

## 📚 Documentation

For more detailed information, see the documentation in the `docs/` folder:

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Complete system architecture and design patterns
- **[QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)** - Quick developer reference
- **[TECHNICAL_SPECIFICATIONS.md](docs/TECHNICAL_SPECIFICATIONS.md)** - Detailed API specifications

## 🚀 Deployment

### Using Gunicorn (Recommended for Production)

```bash
pip install gunicorn

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Environment Variables for Production

Always ensure `.env` is configured with production database credentials and secure settings.

## 🐛 Troubleshooting

### Issue: "Database connection refused"
- Ensure PostgreSQL is running
- Verify `DATABASE_URL` in `.env` is correct
- Check username, password, and database name

### Issue: "Module not found"
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` (or install dependencies manually)

### Issue: "Email already exists"
- The email field has a UNIQUE constraint
- Use a different email address

## 📝 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Feel free to improve this project by:
- Adding input validation using Pydantic
- Implementing authentication
- Adding pagination for user list
- Creating unit tests
- Adding database migrations with Alembic

## 📞 Support

For issues or questions, refer to:
- FastAPI documentation: https://fastapi.tiangolo.com
- SQLAlchemy documentation: https://docs.sqlalchemy.org
- PostgreSQL documentation: https://www.postgresql.org/docs

---

**Last Updated:** May 4, 2026

**Happy coding! 🎉**
