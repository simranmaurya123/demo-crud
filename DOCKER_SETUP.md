# Docker Setup Guide

## Quick Start

### Prerequisites
- Docker installed on your system
- Docker Compose installed

### Running with Docker Compose (Recommended)

1. **Create `.env` file from template:**
   ```bash
   cp .env.example .env
   ```

2. **Start the services:**
   ```bash
   docker-compose up -d
   ```
   This will:
   - Start PostgreSQL database container
   - Build and start the FastAPI application container
   - Create necessary networks and volumes

3. **Access the application:**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

### Stopping Services

```bash
docker-compose down
```

To also remove the database volume:
```bash
docker-compose down -v
```

---

## Building Docker Image Manually

### Build the Image

```bash
docker build -t project-api:latest .
```

### Run Container

With PostgreSQL in a separate container:
```bash
# Start PostgreSQL
docker run -d \
  --name project_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=project_db \
  -p 5432:5432 \
  postgres:15-alpine

# Run the API container
docker run -d \
  --name project_api \
  -e DATABASE_URL=postgresql://postgres:postgres@project_db:5432/project_db \
  -p 8000:8000 \
  --link project_db \
  project-api:latest
```

Or use SQLite (for development only):
```bash
docker run -d \
  --name project_api \
  -p 8000:8000 \
  project-api:latest
```

---

## Docker Compose Details

### Services

**db**: PostgreSQL 15
- Port: 5432 (accessible on host)
- Volume: `postgres_data` (persistent storage)
- Health check: Validates database readiness

**api**: FastAPI Application
- Port: 8000 (accessible on host)
- Depends on: Database service
- Auto-reload enabled for development

### Environment Variables

Edit `.env` file to customize:
- `DB_USER` - PostgreSQL username
- `DB_PASSWORD` - PostgreSQL password
- `DB_NAME` - Database name
- `JWT_SECRET_KEY` - JWT secret (change in production!)
- Other JWT settings as needed

---

## Common Commands

```bash
# View logs
docker-compose logs -f api
docker-compose logs -f db

# Access database
docker-compose exec db psql -U postgres -d project_db

# Rebuild image
docker-compose build --no-cache

# Scale services (if needed)
docker-compose up -d --scale api=3

# Stop but keep containers
docker-compose stop

# Restart services
docker-compose restart
```

---

## Production Considerations

### Before deploying to production:

1. **Change JWT_SECRET_KEY** in `.env` to a strong random value
2. **Use environment-specific configs** - separate dev/staging/prod `.env` files
3. **Set secure database passwords**
4. **Use `.env` in `.gitignore`** (already done)
5. **Add resource limits** to docker-compose.yml
6. **Use managed database services** (AWS RDS, Azure Database, etc.)
7. **Enable HTTPS/TLS** with a reverse proxy (nginx, traefik)
8. **Use secrets management** (Docker Secrets, HashiCorp Vault, etc.)

### Example Production Additions

```yaml
# Add to api service in docker-compose.yml
resources:
  limits:
    cpus: '1'
    memory: 512M
  reservations:
    cpus: '0.5'
    memory: 256M
```

---

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL container is running: `docker ps`
- Check logs: `docker-compose logs db`
- Verify DATABASE_URL in `.env`

### API Container Won't Start
- Check logs: `docker-compose logs api`
- Verify port 8000 isn't already in use
- Ensure requirements.txt is in root directory

### Permission Denied
- On Linux, you may need to use `sudo` or add user to docker group

### Port Already in Use
- Change ports in docker-compose.yml (e.g., `"8001:8000"`)
- Or kill the process using the port

---

## File Descriptions

- **Dockerfile** - Container image definition
- **docker-compose.yml** - Multi-container orchestration configuration
- **.dockerignore** - Files to exclude from Docker build context
- **requirements.txt** - Python package dependencies
- **.env.example** - Template for environment variables
