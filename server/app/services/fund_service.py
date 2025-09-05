"""
Fund service layer for business logic.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.fund import Fund
from app.schemas.fund import FundCreate, FundUpdate


class FundService:
    """Service class for fund operations."""
    
    @staticmethod
    def get_funds(db: Session, skip: int = 0, limit: int = 100) -> List[Fund]:
        """Get all funds with pagination."""
        return db.query(Fund).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_fund_by_name(db: Session, fund_name: str) -> Optional[Fund]:
        """Get a fund by name."""
        return db.query(Fund).filter(Fund.name == fund_name).first()
    
    @staticmethod
    def get_funds_by_category(db: Session, category: str) -> List[Fund]:
        """Get all funds in a specific category."""
        return db.query(Fund).filter(Fund.category == category).all()
    
    @staticmethod
    def get_categories(db: Session) -> List[str]:
        """Get all unique fund categories."""
        return [row[0] for row in db.query(Fund.category).distinct().all()]
    
    @staticmethod
    def create_fund(db: Session, fund: FundCreate) -> Fund:
        """Create a new fund."""
        db_fund = Fund(**fund.dict())
        db.add(db_fund)
        db.commit()
        db.refresh(db_fund)
        return db_fund
    
    @staticmethod
    def update_fund(db: Session, fund_name: str, fund_update: FundUpdate) -> Optional[Fund]:
        """Update an existing fund."""
        db_fund = FundService.get_fund_by_name(db, fund_name)
        if not db_fund:
            return None
        
        update_data = fund_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_fund, field, value)
        
        db.commit()
        db.refresh(db_fund)
        return db_fund
    
    @staticmethod
    def delete_fund(db: Session, fund_name: str) -> bool:
        """Delete a fund."""
        db_fund = FundService.get_fund_by_name(db, fund_name)
        if not db_fund:
            return False
        
        db.delete(db_fund)
        db.commit()
        return True
