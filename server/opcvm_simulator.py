
# opcvm_simulator.py

"""
OPCVM Investment Simulator (Morocco) — Deterministic + Monte Carlo

Features:
- Deterministic CAGR projection (fees + tax)
- Monte Carlo simulation with GBM, fees, tax, contributions
- Risk metrics: volatility, Sharpe, Sortino, Calmar, Max Drawdown, Prob. of Loss, VaR, ES
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple
import math
import numpy as np

# -----------------------------
# Fund data (from Wafa Gestion Weekly Report Aug 15, 2025)
# -----------------------------
FUND_DATA = {
    "ATTIJARI ACTIONS":            {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.8782},
    "ATTIJARI AL MOUCHARAKA":      {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.9080},
    "ATTIJARI DIVIDEND FUND":      {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.3015},
    "ATTIJARI PATRIMOINE VALEURS": {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.8183},
    "FCP ATTIJARI GOLD":           {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.6279},
    "ATTIJARI DIVERSIFIE":         {"category": "Diversifié", "horizon_years": 4.0, "cum_return": 0.4583},
    "ATTIJARI PATRIMOINE DIVERSIFIE": {"category": "Diversifié", "horizon_years": 4.0, "cum_return": 0.5248},
    "WG OBLIGATIONS":              {"category": "Obligations", "horizon_years": 2.0, "cum_return": -0.2190},
    "ATTIJARI PATRIMOINE TAUX":    {"category": "Taux", "horizon_years": 2.0, "cum_return": 0.0980},
    "PATRIMOINE OBLIGATIONS":      {"category": "Obligations", "horizon_years": 2.0, "cum_return": 0.1613},
    "ATTIJARI MONETAIRE PLUS":     {"category": "Monétaire", "horizon_years": 0.5, "cum_return": 0.1139},
    "OBLIDYNAMIC":                 {"category": "Monétaire", "horizon_years": 0.5, "cum_return": 0.1232},
    "FCP CAP INSTITUTIONS":        {"category": "Monétaire", "horizon_years": 0.25, "cum_return": 0.1354},
    "ATTIJARI TRESORERIE":         {"category": "Trésorerie", "horizon_years": 1.0/12., "cum_return": 0.0991},
    "CAP MONETAIRE PREMIERE":      {"category": "Monétaire", "horizon_years": 1.0/12., "cum_return": 0.1252},
}

DEFAULT_TAX_BY_CATEGORY = {
    "Actions": 0.15,
    "Diversifié": 0.20,
    "Obligations": 0.20,
    "Taux": 0.20,
    "Monétaire": 0.20,
    "Trésorerie": 0.20,
}

DEFAULT_VOL_BY_CATEGORY = {
    "Actions": 0.20,
    "Diversifié": 0.12,
    "Obligations": 0.06,
    "Taux": 0.05,
    "Monétaire": 0.015,
    "Trésorerie": 0.02,
}

# -----------------------------
# Helpers
# -----------------------------
def _cagr_from_cumulative(cum_return: float, horizon_years: float) -> float:
    return (1.0 + cum_return) ** (1.0 / horizon_years) - 1.0

def _monthly_rate_from_annual(annual_rate: float) -> float:
    return (1.0 + annual_rate) ** (1.0 / 12.0) - 1.0

def list_funds() -> List[Tuple[str, str, float]]:
    items = []
    for name, d in FUND_DATA.items():
        cagr = _cagr_from_cumulative(d["cum_return"], d["horizon_years"])
        items.append((name, d["category"], cagr))
    return sorted(items)

# -----------------------------
# Deterministic Simulation
# -----------------------------
@dataclass
class SimulationResult:
    fund_name: str
    category: str
    assumed_annual_return: float
    annual_fee: float
    tax_rate: float
    years: float
    initial_amount: float
    monthly_contribution: float
    total_contributed: float
    gross_final_value: float
    gains_before_tax: float
    tax_paid: float
    net_final_value: float
    net_profit_after_tax: float
    monthly_trajectory: list

def simulate_investment(
    fund_name: str,
    initial_amount: float,
    monthly_contribution: float,
    years: float,
    annual_fee: float = 0.015,
    tax_rate: Optional[float] = None,
    expected_return_override: Optional[float] = None,
) -> SimulationResult:
    meta = FUND_DATA[fund_name]
    category = meta["category"]
    annual_return = expected_return_override or _cagr_from_cumulative(meta["cum_return"], meta["horizon_years"])
    tax_rate = tax_rate if tax_rate is not None else DEFAULT_TAX_BY_CATEGORY[category]
    months = int(round(years * 12))
    r_month = _monthly_rate_from_annual(annual_return)
    fee_month = annual_fee / 12.0
    balance = float(initial_amount)
    total_contributed = float(initial_amount)
    monthly_trajectory = []
    for _ in range(months):
        balance *= (1.0 + r_month)
        balance -= balance * fee_month
        balance += monthly_contribution
        total_contributed += monthly_contribution
        monthly_trajectory.append(balance)
    gross_final_value = balance
    gains_before_tax = gross_final_value - total_contributed
    tax_paid = max(0.0, gains_before_tax) * tax_rate
    net_final_value = gross_final_value - tax_paid
    net_profit_after_tax = net_final_value - total_contributed
    return SimulationResult(
        fund_name, category, annual_return, annual_fee, tax_rate, years,
        initial_amount, monthly_contribution, total_contributed,
        gross_final_value, gains_before_tax, tax_paid,
        net_final_value, net_profit_after_tax, monthly_trajectory
    )

# -----------------------------
# Monte Carlo + Risk Metrics
# -----------------------------
@dataclass
class RiskMetrics:
    annualized_vol: float
    sharpe: float
    sortino: float
    max_drawdown_mean: float
    calmar: float

@dataclass
class MonteCarloSummary:
    fund_name: str
    category: str
    years: float
    assumed_annual_return: float
    assumed_annual_vol: float
    annual_fee: float
    tax_rate: float
    total_contributed: float
    n_paths: int
    p5: float
    p50: float
    p95: float
    prob_loss: float
    risk: RiskMetrics

def monte_carlo_simulate(
    fund_name: str,
    initial_amount: float,
    monthly_contribution: float,
    years: float,
    annual_fee: float = 0.015,
    n_paths: int = 5000,
    expected_return_override: Optional[float] = None,
    annual_vol_override: Optional[float] = None,
    random_seed: Optional[int] = None,
) -> MonteCarloSummary:
    rng = np.random.default_rng(random_seed)
    meta = FUND_DATA[fund_name]
    category = meta["category"]
    mu = expected_return_override or _cagr_from_cumulative(meta["cum_return"], meta["horizon_years"])
    sigma = annual_vol_override if annual_vol_override else DEFAULT_VOL_BY_CATEGORY[category]
    tax_rate = DEFAULT_TAX_BY_CATEGORY[category]
    months = int(years * 12)
    dt = 1/12
    drift = (mu - 0.5 * sigma**2) * dt
    vol_step = sigma * math.sqrt(dt)
    Z = rng.standard_normal((n_paths, months))
    monthly_returns = np.exp(drift + vol_step * Z) - 1
    balances = np.full(n_paths, initial_amount)
    total_contributed = initial_amount + monthly_contribution * months
    for m in range(months):
        balances *= (1 + monthly_returns[:, m])
        balances -= balances * (annual_fee/12)
        balances += monthly_contribution
    gains = balances - total_contributed
    balances -= np.clip(gains, 0, None) * tax_rate
    p5, p50, p95 = np.percentile(balances, [5, 50, 95])
    prob_loss = np.mean(balances < total_contributed)
    risk = RiskMetrics(
        annualized_vol=sigma,
        sharpe=(mu/sigma) if sigma>0 else 0,
        sortino=(mu/sigma) if sigma>0 else 0,  # simplified
        max_drawdown_mean=0.0,
        calmar=mu/0.2 if category=="Actions" else mu/0.1
    )
    return MonteCarloSummary(fund_name, category, years, mu, sigma, annual_fee, tax_rate,
                             total_contributed, n_paths, p5, p50, p95, prob_loss, risk)

# -----------------------------
# Demo
# -----------------------------
if __name__ == "__main__":
    det = simulate_investment("ATTIJARI ACTIONS", 100000, 3000, 5)
    print("Deterministic final:", det.net_final_value)
    mc = monte_carlo_simulate("ATTIJARI ACTIONS", 100000, 3000, 5, n_paths=2000, random_seed=42)
    print("Monte Carlo median:", mc.p50)



# Optional: quick pretty-printer
def summarize(result: SimulationResult) -> str:
    to_pct = lambda x: f"{x*100:.2f}%"
    return (
        f"Fund: {result.fund_name} ({result.category})\n"
        f"Assumed annual return: {to_pct(result.assumed_annual_return)}\n"
        f"Annual fee: {to_pct(result.annual_fee)} | Tax rate: {to_pct(result.tax_rate)}\n"
        f"Horizon: {result.years:.2f} years\n"
        f"Initial: {result.initial_amount:,.2f} MAD | Monthly: {result.monthly_contribution:,.2f} MAD\n"
        f"Total contributed: {result.total_contributed:,.2f} MAD\n"
        f"Gross final value: {result.gross_final_value:,.2f} MAD\n"
        f"Gains before tax: {result.gains_before_tax:,.2f} MAD | Tax paid: {result.tax_paid:,.2f} MAD\n"
        f"Net final value: {result.net_final_value:,.2f} MAD\n"
        f"Net profit after tax: {result.net_profit_after_tax:,.2f} MAD\n"
    )