"""
Health check API endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.models.fund import Fund

router = APIRouter()


@router.get("/")
def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "OPCVM Simulator API"}


@router.get("/db")
def database_health_check(db: Session = Depends(get_db_session)):
    """Database health check endpoint."""
    try:
        # Try to query the database
        fund_count = db.query(Fund).count()
        return {
            "status": "healthy",
            "database": "connected",
            "fund_count": fund_count
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
