"""
Pydantic schemas for simulation-related data.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class SimulationInput(BaseModel):
    """Schema for simulation input parameters."""
    fund_name: str = Field(..., description="Name of the fund to simulate")
    initial_investment: float = Field(..., gt=0, description="Initial investment amount")
    investment_horizon: int = Field(..., gt=0, description="Investment horizon in years")
    monthly_contribution: Optional[float] = Field(0, ge=0, description="Monthly contribution amount")
    tax_rate: Optional[float] = Field(None, ge=0, le=100, description="Tax rate percentage")


class MonteCarloInput(SimulationInput):
    """Schema for Monte Carlo simulation input."""
    num_simulations: int = Field(1000, gt=0, le=10000, description="Number of Monte Carlo simulations")
    confidence_level: float = Field(0.95, gt=0, lt=1, description="Confidence level for results")


class SimulationResult(BaseModel):
    """Schema for simulation result."""
    fund_name: str
    category: str
    assumed_annual_return: float
    annual_fee: Optional[float] = None
    tax_rate: Optional[float] = None
    years: int
    gross_final_value: float
    net_final_value: float
    net_profit_after_tax: float
    tax_paid: float
    total_contributed: float
    initial_amount: Optional[float] = None
    monthly_contribution: Optional[float] = None
    trajectory: Optional[List[dict]] = None


class MonteCarloResult(BaseModel):
    """Schema for Monte Carlo simulation result."""
    fund_name: str
    category: str
    assumed_annual_return: float
    assumed_annual_vol: float
    annual_fee: Optional[float] = None
    tax_rate: Optional[float] = None
    years: int
    gross_final_value: float
    net_final_value: float
    net_profit_after_tax: float
    tax_paid: float
    total_contributed: float
    initial_amount: Optional[float] = None
    monthly_contribution: Optional[float] = None
    trajectory: Optional[List[dict]] = None
    # Monte Carlo specific fields
    n_paths: int
    percentiles: dict
    prob_loss: float
    risk_metrics: Optional[dict] = None
