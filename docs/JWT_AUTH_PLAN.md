# JWT Authentication Plan

## Goals
- Add JWT-based authentication and authorization to the FastAPI API.
- Protect existing user CRUD endpoints behind authenticated access.
- Provide login and registration endpoints that issue access tokens.
- Keep configuration and secrets in environment variables.

## Assumptions
- FastAPI remains the entry point (main.py).
- SQLAlchemy is used for persistence.
- Users table will store a password hash (not plain text).
- Tokens will be stateless JWTs (access tokens only to start).
- CRUD endpoints will be migrated to JSON request bodies.

## High-Level Design
1. Passwords are hashed using a strong algorithm (bcrypt).
2. Login endpoint verifies credentials and returns a JWT access token.
3. Protected endpoints require a valid bearer token.
4. Token claims include subject (user_id or email) and expiry.
5. Secret key and token settings are loaded from .env.

## Configuration
Add to .env:
- JWT_SECRET_KEY=<random-secret>
- JWT_ALGORITHM=HS256
- JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

## Data Model Changes
- Add column: password_hash (string) to the User model.
- Optional: add column is_active (boolean) for account status.
- Optional: add column created_at (timestamp) for auditing.

## API Additions
- POST /auth/register
  - Accepts user details + password (JSON body)
  - Creates user with hashed password
- POST /auth/login
  - Accepts email + password (JSON body)
  - Returns access_token and token_type=bearer
- GET /auth/me
  - Returns current user based on token

## Security Controls
- Enforce HTTPS in production.
- Validate password strength at registration.
- Set short token expiry; consider refresh tokens later.
- Default to Authorization: Bearer <token> header.

## Error Handling
- 401 for invalid or missing token.
- 403 for inactive or unauthorized user.
- 409 for duplicate email during registration.

## Implementation Steps
1. Add dependencies:
  - python-jose[cryptography]
  - passlib[bcrypt]
2. Add Pydantic schemas for auth and user input validation.
3. Create auth utilities:
  - hash_password()
  - verify_password()
  - create_access_token()
4. Add auth routes (new router file or within main.py).
5. Update user creation to store password_hash.
6. Add dependency to extract current user from JWT.
7. Protect existing CRUD endpoints.
8. Migrate CRUD endpoints to JSON bodies (update routes, schemas, and docs).
9. Update tests and docs.

## Tests
- Register user success
- Login success and token returned
- Login with bad password -> 401
- Access protected endpoint without token -> 401
- Access protected endpoint with valid token -> 200

## Rollout Notes
- Backfill existing users with reset passwords if any exist.
- Rotate JWT secret on a schedule; invalidate old tokens if required.

## Decisions
- Login will use email only.
- Registration will be open.
- Migrate CRUD endpoints to JSON bodies.
