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
    
    # Category-based defaults
    default_tax_rate = Column(Float, nullable=False)
    default_volatility = Column(Float, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Fund(name='{self.name}', category='{self.category}')>"
    
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
            "default_tax_rate": self.default_tax_rate,
            "default_volatility": self.default_volatility
        }
