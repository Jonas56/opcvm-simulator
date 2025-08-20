from fastapi import FastAPI
from pydantic import BaseModel
from opcvm_simulator import simulate_investment, monte_carlo_simulate

app = FastAPI()

class SimulationRequest(BaseModel):
    fund_name: str
    initial_amount: float
    monthly_contribution: float
    years: float
    annual_fee: float
    tax_rate: float | None = None

class MonteCarloRequest(BaseModel):
    fund_name: str
    initial_amount: float
    monthly_contribution: float
    years: float
    annual_fee: float = 0.015
    n_paths: int = 5000
    expected_return_override: float | None = None
    annual_vol_override: float | None = None
    random_seed: int | None = None

@app.post("/deterministic")
def simulate(req: SimulationRequest):
    result = simulate_investment(
        fund_name=req.fund_name,
        initial_amount=req.initial_amount,
        monthly_contribution=req.monthly_contribution,
        years=req.years,
        annual_fee=req.annual_fee,
        tax_rate=req.tax_rate,
    )
    return {
        "fund_name": result.fund_name,
        "category": result.category,
        "assumed_annual_return": result.assumed_annual_return,
        "years": result.years,
        "gross_final_value": result.gross_final_value,
        "net_final_value": result.net_final_value,
        "net_profit_after_tax": result.net_profit_after_tax,
        "tax_paid": result.tax_paid,
        "total_contributed": result.total_contributed,
        "trajectory": [{"month": i+1, "value": v} for i, v in enumerate(result.monthly_trajectory)],
    }

@app.post("/mc-simulate")
def monte_carlo_simulate_route(req: MonteCarloRequest):
    """
    Monte Carlo simulation endpoint for investment analysis.
    
    This endpoint performs Monte Carlo simulation to analyze investment scenarios
    with probabilistic outcomes, including risk metrics and percentile analysis.
    """
    result = monte_carlo_simulate(
        fund_name=req.fund_name,
        initial_amount=req.initial_amount,
        monthly_contribution=req.monthly_contribution,
        years=req.years,
        annual_fee=req.annual_fee,
        n_paths=req.n_paths,
        expected_return_override=req.expected_return_override,
        annual_vol_override=req.annual_vol_override,
        random_seed=req.random_seed,
    )
    
    return {
        "fund_name": result.fund_name,
        "category": result.category,
        "years": result.years,
        "assumed_annual_return": result.assumed_annual_return,
        "assumed_annual_vol": result.assumed_annual_vol,
        "annual_fee": result.annual_fee,
        "tax_rate": result.tax_rate,
        "total_contributed": result.total_contributed,
        "n_paths": result.n_paths,
        "percentiles": {
            "p5": result.p5,
            "p50": result.p50,
            "p95": result.p95
        },
        "prob_loss": result.prob_loss,
        "risk_metrics": {
            "annualized_vol": result.risk.annualized_vol,
            "sharpe": result.risk.sharpe,
            "sortino": result.risk.sortino,
            "max_drawdown_mean": result.risk.max_drawdown_mean,
            "calmar": result.risk.calmar
        }
    }

# Run with: uvicorn server:app --reload --port 8000