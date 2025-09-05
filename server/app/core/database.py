"""
Database configuration and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import Base from models to ensure all models use the same Base class
from app.models.fund import Base

def get_db():
    """
    Dependency function to get database session.
    
    This function creates a new database session and ensures it's properly closed
    after use. It's designed to be used as a dependency in FastAPI endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database by creating all tables.
    
    This function should be called once when setting up the application
    to ensure all database tables exist.
    """
    Base.metadata.create_all(bind=engine)
