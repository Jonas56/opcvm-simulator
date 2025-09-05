"""
Pydantic schemas for fund-related data.
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class FundBase(BaseModel):
    """Base fund schema."""
    name: str = Field(..., description="Fund name")
    category: str = Field(..., description="Fund category")
    horizon_years: float = Field(..., description="Recommended investment horizon in years")
    cumulative_return: float = Field(..., description="Historical cumulative return")
    nav: float = Field(..., description="Net Asset Value")
    risk_profile: str = Field(..., description="Risk level (low, medium, high)")
    recommended_holding: str = Field(..., description="Recommended holding period")
    objective: str = Field(..., description="Fund investment objective")
    strategy: str = Field(..., description="Fund investment strategy")
    default_tax_rate: float = Field(..., description="Default tax rate for category")
    default_volatility: float = Field(..., description="Default volatility for category")


class FundCreate(FundBase):
    """Schema for creating a new fund."""
    pass


class FundUpdate(BaseModel):
    """Schema for updating a fund."""
    name: Optional[str] = None
    category: Optional[str] = None
    horizon_years: Optional[float] = None
    cumulative_return: Optional[float] = None
    nav: Optional[float] = None
    risk_profile: Optional[str] = None
    recommended_holding: Optional[str] = None
    objective: Optional[str] = None
    strategy: Optional[str] = None
    default_tax_rate: Optional[float] = None
    default_volatility: Optional[float] = None


class Fund(FundBase):
    """Schema for fund response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FundList(BaseModel):
    """Schema for list of funds."""
    funds: list[Fund]
    total: int
