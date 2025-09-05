"""
Fund-related API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.services.fund_service import FundService
from app.schemas.fund import Fund, FundCreate, FundUpdate, FundList

router = APIRouter()


@router.get("/", response_model=FundList)
def get_funds(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db_session)
):
    """Get all funds with pagination."""
    funds = FundService.get_funds(db, skip=skip, limit=limit)
    total = len(funds)  # In a real app, you'd get total count separately
    return FundList(funds=funds, total=total)


@router.get("/{fund_name}", response_model=Fund)
def get_fund(fund_name: str, db: Session = Depends(get_db_session)):
    """Get a specific fund by name."""
    fund = FundService.get_fund_by_name(db, fund_name)
    if not fund:
        raise HTTPException(status_code=404, detail=f"Fund '{fund_name}' not found")
    return fund


@router.get("/category/{category}", response_model=List[Fund])
def get_funds_by_category(category: str, db: Session = Depends(get_db_session)):
    """Get all funds in a specific category."""
    funds = FundService.get_funds_by_category(db, category)
    return funds


@router.get("/categories/list", response_model=List[str])
def get_categories(db: Session = Depends(get_db_session)):
    """Get all available fund categories."""
    return FundService.get_categories(db)


@router.post("/", response_model=Fund)
def create_fund(fund: FundCreate, db: Session = Depends(get_db_session)):
    """Create a new fund."""
    # Check if fund already exists
    existing_fund = FundService.get_fund_by_name(db, fund.name)
    if existing_fund:
        raise HTTPException(status_code=400, detail=f"Fund '{fund.name}' already exists")
    
    return FundService.create_fund(db, fund)


@router.put("/{fund_name}", response_model=Fund)
def update_fund(
    fund_name: str, 
    fund_update: FundUpdate, 
    db: Session = Depends(get_db_session)
):
    """Update an existing fund."""
    updated_fund = FundService.update_fund(db, fund_name, fund_update)
    if not updated_fund:
        raise HTTPException(status_code=404, detail=f"Fund '{fund_name}' not found")
    return updated_fund


@router.delete("/{fund_name}")
def delete_fund(fund_name: str, db: Session = Depends(get_db_session)):
    """Delete a fund."""
    success = FundService.delete_fund(db, fund_name)
    if not success:
        raise HTTPException(status_code=404, detail=f"Fund '{fund_name}' not found")
    return {"message": f"Fund '{fund_name}' deleted successfully"}
