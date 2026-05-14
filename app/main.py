import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.init_db import init_db
from app.api.v1.users.router import router as users_router
from app.api.v1.teachers.router import router as teachers_router
from app.api.v1.students.router import router as students_router
from app.api.v1.auth.router import router as auth_router
from app.api.v1.attendance.router import router as attendance_router
from app.api.v1.subjects.router import router as subjects_router
from app.api.v1.classes.router import router as classes_router
from app.api.v1.class_timetable.router import router as class_timetable_router
from app.api.v1.teacher_timetable.router import router as teacher_timetable_router
from app.api.v1.student_timetable.router import router as student_timetable_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database tables on startup
logger.info("🔄 Initializing PostgreSQL database...")
try:
    init_db()
    logger.info("✅ PostgreSQL database initialized successfully")
except Exception as e:
    logger.error(f"❌ Error initializing database: {e}")


def create_app():
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
        swagger_ui_parameters={"tryItOutEnabled": True}
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    # Startup event
    @app.on_event("startup")
    async def startup_event():
        logger.info("✓ FastAPI app startup complete")

    # Include routers with v1 prefix
    app.include_router(users_router, prefix=settings.API_V1_STR)
    app.include_router(teachers_router, prefix=settings.API_V1_STR)
    app.include_router(students_router, prefix=settings.API_V1_STR)
    app.include_router(auth_router, prefix=settings.API_V1_STR)
    app.include_router(attendance_router, prefix=settings.API_V1_STR)
    app.include_router(subjects_router, prefix=settings.API_V1_STR)
    app.include_router(classes_router, prefix=settings.API_V1_STR)
    app.include_router(class_timetable_router, prefix=settings.API_V1_STR)
    app.include_router(teacher_timetable_router, prefix=settings.API_V1_STR)
    app.include_router(student_timetable_router, prefix=settings.API_V1_STR)
    return app


# Instantiate the app at module level for uvicorn
app = create_app()
