"""
Database models for the OPCVM Simulator application.
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Fund(Base):
    """
    Fund model representing investment funds with their performance and metadata.
    
    This model combines:
    - Performance data (from hardcoded FUND_DATA)
    - Metadata (from funds.json)
    - Category-based defaults (tax rates, volatility)
    """
    __tablename__ = "funds"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Fund identification
    name = Column(String(255), unique=True, nullable=False, index=True)
    
    # Performance data (from hardcoded FUND_DATA)
    category = Column(String(50), nullable=False, index=True)
    horizon_years = Column(Float, nullable=False)
    cumulative_return = Column(Float, nullable=False)
    
    # Metadata (from funds.json)
    nav = Column(Float, nullable=True)  # Net Asset Value
    risk_profile = Column(String(20), nullable=True)  # low, medium, high
    recommended_holding = Column(String(20), nullable=True)  # short, medium, long
    objective = Column(Text, nullable=True)
    strategy = Column(Text, nullable=True)
    
    # Fund-specific financial parameters
    management_fee = Column(Float, nullable=False, default=1.5)  # Annual management fee in percentage
    expected_return = Column(Float, nullable=True)  # Expected annual return in percentage (calculated from cumulative_return)
    
    # Category-based defaults
    default_tax_rate = Column(Float, nullable=False)
    default_volatility = Column(Float, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Fund(name='{self.name}', category='{self.category}')>"
    
    def calculate_expected_return(self) -> float:
        """
        Calculate expected annual return from cumulative return using CAGR formula.
        
        Returns:
            Expected annual return as a percentage
        """
        if self.cumulative_return is None or self.horizon_years is None:
            return None
        
        # CAGR formula: (1 + cumulative_return)^(1/horizon_years) - 1
        cagr = (1.0 + self.cumulative_return) ** (1.0 / self.horizon_years) - 1.0
        return cagr * 100  # Convert to percentage
    
    def to_dict(self):
        """Convert fund to dictionary format for API responses."""
        return {
            "name": self.name,
            "nav": self.nav,
            "riskProfile": self.risk_profile,
            "recommendedHolding": self.recommended_holding,
            "objective": self.objective,
            "strategy": self.strategy,
            "category": self.category,
            "horizon_years": self.horizon_years,
            "cumulative_return": self.cumulative_return,
            "management_fee": self.management_fee,
            "expected_return": self.expected_return,
            "default_tax_rate": self.default_tax_rate,
            "default_volatility": self.default_volatility
        }
