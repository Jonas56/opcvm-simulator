"""
API dependencies for FastAPI endpoints.
"""

from typing import Generator
from sqlalchemy.orm import Session
from app.core.database import get_db

# Re-export the database dependency for convenience
get_db_session = get_db
