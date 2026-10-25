import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load .env.local (Neon/local overrides) and .env
load_dotenv(".env.local")
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/taskdb")

# Ensure the connection string uses psycopg2 driver for SQLAlchemy
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# Configure connection pool settings:
# pool_pre_ping=True: checks connection liveness before checkout to prevent stale socket errors
# (especially vital for serverless databases like Neon or cloud Aurora/RDS).
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency for obtaining an isolated database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
