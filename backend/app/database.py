from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings
import os

settings = get_settings()

# Use SQLite for development if PostgreSQL is not available
db_url = settings.DATABASE_URL
if os.getenv("ENV") == "development" or "localhost" in db_url:
    # Try PostgreSQL first
    try:
        from sqlalchemy import text
        test_engine = create_engine(db_url, connect_args={"timeout": 5})
        with test_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        # Fall back to SQLite
        print("⚠️  PostgreSQL not available, using SQLite instead")
        db_url = "sqlite:///./audio_processor.db"

# Create database engine
engine = create_engine(
    db_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    connect_args={"timeout": 30} if "sqlite" in db_url else {},
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
