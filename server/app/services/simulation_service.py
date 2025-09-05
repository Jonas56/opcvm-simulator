"""
Simulation service for investment calculations using OPCVM simulator.
"""

import numpy as np
from sqlalchemy.orm import Session
from app.models.fund import Fund
from app.schemas.simulation import SimulationInput, MonteCarloInput, SimulationResult, MonteCarloResult
from opcvm_simulator import simulate_investment, monte_carlo_simulate


class SimulationService:
    """Service class for investment simulations."""
    
    @staticmethod
    def deterministic_simulation(
        db: Session, 
        simulation_input: SimulationInput
    ) -> SimulationResult:
        """
        Perform deterministic investment simulation using OPCVM simulator.
        
        Args:
            db: Database session
            simulation_input: Simulation parameters
            
        Returns:
            SimulationResult with year-by-year breakdown
        """
        # Get fund data
        fund = db.query(Fund).filter(Fund.name == simulation_input.fund_name).first()
        if not fund:
            raise ValueError(f"Fund '{simulation_input.fund_name}' not found")
        
        tax_rate = 0.15 # TODO: Get tax rate from fund
        
        # Run the simulation using OPCVM simulator
        result = simulate_investment(
            fund_name=fund.name,
            initial_amount=simulation_input.initial_investment,
            monthly_contribution=simulation_input.monthly_contribution or 0,
            years=simulation_input.investment_horizon,
            annual_fee=fund.management_fee / 100.0 if hasattr(fund, 'management_fee') else 0.015,
            tax_rate=tax_rate,
            expected_return_override=fund.expected_return / 100.0 if hasattr(fund, 'expected_return') else None
        )
        
        return SimulationResult(
            fund_name=result.fund_name,
            category=result.category,
            assumed_annual_return=result.assumed_annual_return,
            annual_fee=result.annual_fee,
            tax_rate=result.tax_rate,
            years=int(round(result.years)),
            gross_final_value=result.gross_final_value,
            net_final_value=result.net_final_value,
            net_profit_after_tax=result.net_profit_after_tax,
            tax_paid=result.tax_paid,
            total_contributed=result.total_contributed,
            initial_amount=result.initial_amount,
            monthly_contribution=result.monthly_contribution,
        )
        
    
    @staticmethod
    def monte_carlo_simulation(
        db: Session,
        simulation_input: MonteCarloInput
    ) -> MonteCarloResult:
        """
        Perform Monte Carlo investment simulation using OPCVM simulator.
        
        Args:
            db: Database session
            simulation_input: Monte Carlo simulation parameters
            
        Returns:
            MonteCarloResult with statistical analysis
        """
        # Get fund data
        fund = db.query(Fund).filter(Fund.name == simulation_input.fund_name).first()
        if not fund:
            raise ValueError(f"Fund '{simulation_input.fund_name}' not found")
        
        # Use fund's tax rate if not provided (convert from percentage to decimal)
        tax_rate = (simulation_input.tax_rate or fund.default_tax_rate) / 100.0
        
        # Get fund's volatility (default to 20% if not available)
        volatility = getattr(fund, 'default_volatility', 20.0) / 100.0
        
        # Run Monte Carlo simulation using OPCVM simulator
        mc_result = monte_carlo_simulate(
            fund_name=fund.name,
            initial_amount=simulation_input.initial_investment,
            monthly_contribution=simulation_input.monthly_contribution or 0,
            years=simulation_input.investment_horizon,
            annual_fee=getattr(fund, 'management_fee', 1.5) / 100.0,  # Default to 1.5% if not set
            n_paths=simulation_input.num_simulations,
            expected_return_override=getattr(fund, 'expected_return', None),
            annual_vol_override=volatility,
            random_seed=42  # For reproducibility
        )
        
        # Calculate percentiles from the simulation results
        percentiles = {
            'p5': mc_result.p5,
            'p25': np.percentile([mc_result.p5, mc_result.p95], 25),  # Approximate
            'p50': mc_result.p50,
            'p75': np.percentile([mc_result.p5, mc_result.p95], 75),  # Approximate
            'p95': mc_result.p95
        }
        
        # Create risk metrics dictionary
        risk_metrics = {
            'annualized_vol': mc_result.risk.annualized_vol,
            'sharpe': mc_result.risk.sharpe,
            'sortino': mc_result.risk.sortino,
            'max_drawdown': mc_result.risk.max_drawdown_mean,
            'calmar': mc_result.risk.calmar
        }
        
        # Calculate trajectory (using median values)
        trajectory = [
            {"month": i+1, "value": mc_result.p50}  # Using p50 as the trajectory
            for i in range(simulation_input.investment_horizon * 12)
        ]

        return MonteCarloResult(
            fund_name=mc_result.fund_name,
            category=mc_result.category,
            assumed_annual_return=mc_result.assumed_annual_return,
            assumed_annual_vol=mc_result.assumed_annual_vol,
            annual_fee=mc_result.annual_fee,
            tax_rate=mc_result.tax_rate,
            years=int(round(mc_result.years)),
            gross_final_value=mc_result.p50,  # Using median as the representative value
            net_final_value=mc_result.p50,    # Same as gross since taxes are already applied
            net_profit_after_tax=mc_result.p50 - simulation_input.initial_investment,
            tax_paid=0,  # Already accounted for in the net values
            total_contributed=(
                simulation_input.initial_investment + 
                (simulation_input.monthly_contribution or 0) * 
                simulation_input.investment_horizon * 12
            ),
            initial_amount=simulation_input.initial_investment,
            monthly_contribution=simulation_input.monthly_contribution or 0,
            trajectory=trajectory,
            n_paths=mc_result.n_paths,
            percentiles=percentiles,
            prob_loss=mc_result.prob_loss,
            risk_metrics=risk_metrics
        )
