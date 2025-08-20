
"""
OPCVM Investment Simulator (Morocco) — Hardcoded from Wafa Gestion Weekly Report (Aug 15, 2025)

Assumptions & Notes:
- Expected returns are derived from the *rightmost cumulative performance* shown per fund in the shared report,
  interpreted as the longest available horizon (e.g., 5Y/4Y/2Y/6M/3M/1M/1D). We convert that cumulative
  performance into an annualized CAGR for simulation.
- Fees: input as annual management fee (e.g., 0.015 = 1.5% per year), applied monthly.
- Tax: by default determined by fund category per AMMC/Wafa Gestion guidance:
    * 15% for equity OPCVM ("Actions").
    * 20% for Diversified, Bond/Fixed Income ("Obligations/Taux"), and Money Market ("Monétaire/Trésorerie").
  You can override with `tax_rate` if needed.
- Compounding: monthly. Contributions are added at end of each month (after growth & fees), configurable.
- You can override the expected annual return with `expected_return_override` if you disagree with the embedded estimate.

DISCLAIMER: This is a simplified deterministic model based on historical summary figures and does not
constitute investment advice. Real returns vary, fees/entry/exit costs and taxation can change.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple
import math

# -----------------------------
# Embedded fund data (from report)
# -----------------------------
# For each fund, we record: category, horizon_years used to derive CAGR, cumulative_return_fraction over that horizon.
# Example: 0.8782 over 5 years -> CAGR = (1+0.8782)**(1/5)-1

FUND_DATA = {
    # ----- Equity (Actions) -----
    "ATTIJARI ACTIONS":            {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.8782},
    "ATTIJARI AL MOUCHARAKA":      {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.9080},
    "ATTIJARI DIVIDEND FUND":      {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.3015},
    "ATTIJARI PATRIMOINE VALEURS": {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.8183},
    "FCP ATTIJARI GOLD":           {"category": "Actions", "horizon_years": 5.0, "cum_return": 0.6279},
    # "FCP ATTIJARI VALEURS ESG":  # missing long-horizon figure in snapshot -> skip to avoid bad inference

    # ----- Diversified -----
    "ATTIJARI DIVERSIFIE":             {"category": "Diversifié", "horizon_years": 4.0, "cum_return": 0.4583},
    "ATTIJARI PATRIMOINE DIVERSIFIE":  {"category": "Diversifié", "horizon_years": 4.0, "cum_return": 0.5248},

    # ----- Bonds / Rates (Oblig/Taux) -----
    "WG OBLIGATIONS":               {"category": "Obligations", "horizon_years": 2.0, "cum_return": -0.2190},
    "ATTIJARI PATRIMOINE TAUX":     {"category": "Taux",        "horizon_years": 2.0, "cum_return": 0.0980},
    "PATRIMOINE OBLIGATIONS":       {"category": "Obligations", "horizon_years": 2.0, "cum_return": 0.1613},

    # ----- Money Market / Treasury -----
    "ATTIJARI MONETAIRE PLUS":      {"category": "Monétaire",  "horizon_years": 0.5,     "cum_return": 0.1139},  # 6 months snapshot
    "OBLIDYNAMIC":                   {"category": "Monétaire",  "horizon_years": 0.5,     "cum_return": 0.1232},  # 6 months snapshot
    "FCP CAP INSTITUTIONS":         {"category": "Monétaire",  "horizon_years": 0.25,    "cum_return": 0.1354},  # 3 months snapshot
    "ATTIJARI TRESORERIE":          {"category": "Trésorerie", "horizon_years": 1.0/12., "cum_return": 0.0991},  # 1 month snapshot
    "CAP MONETAIRE PREMIERE":       {"category": "Monétaire",  "horizon_years": 1.0/12., "cum_return": 0.1252},  # 1 month snapshot
    # The "ATTIJARI MONETAIRE JOUR" figure in the snapshot looks like a YTD-type figure; omitted to avoid mis-annualization.
}

# Default tax rates by category (can be overridden per call)
DEFAULT_TAX_BY_CATEGORY = {
    "Actions": 0.15,
    "Diversifié": 0.20,
    "Obligations": 0.20,
    "Taux": 0.20,
    "Monétaire": 0.20,
    "Trésorerie": 0.20,
}

@dataclass
class SimulationResult:
    fund_name: str
    category: str
    assumed_annual_return: float   # as fraction (e.g., 0.08 = 8%)
    annual_fee: float              # as fraction
    tax_rate: float                # as fraction applied to gains at the end
    years: float
    initial_amount: float
    monthly_contribution: float
    total_contributed: float
    gross_final_value: float
    gains_before_tax: float
    tax_paid: float
    net_final_value: float
    net_profit_after_tax: float
    monthly_trajectory: list  # list of month-end net asset values before end-tax

def _cagr_from_cumulative(cum_return: float, horizon_years: float) -> float:
    """
    Convert a cumulative return over 'horizon_years' into an annualized CAGR.
    cum_return: 0.35 means +35% cumulative.
    """
    if horizon_years <= 0:
        raise ValueError("horizon_years must be > 0")
    return (1.0 + cum_return) ** (1.0 / horizon_years) - 1.0

def _monthly_rate_from_annual(annual_rate: float) -> float:
    return (1.0 + annual_rate) ** (1.0 / 12.0) - 1.0

def list_funds() -> List[Tuple[str, str, float]]:
    """
    Returns list of (fund_name, category, assumed_annual_return) using embedded data.
    """
    items = []
    for name, d in FUND_DATA.items():
        cagr = _cagr_from_cumulative(d["cum_return"], d["horizon_years"])
        items.append((name, d["category"], cagr))
    return sorted(items)

def simulate_investment(
    fund_name: str,
    initial_amount: float,
    monthly_contribution: float,
    years: float,
    annual_fee: float = 0.015,
    tax_rate: Optional[float] = None,
    expected_return_override: Optional[float] = None,
    contribution_increase_rate: float = 0.0,  # annual increase in monthly contribution (e.g., 0.02 = +2%/yr), applied monthly
    contributions_at_beginning: bool = False  # if True, add contribution before growth/fees each month
) -> SimulationResult:
    """
    Simulate monthly compounding with fees and end-of-horizon capital gains tax.

    - expected_return_override: annual nominal return (e.g., 0.08 for 8%). If None, it is derived from FUND_DATA.
    - tax_rate: if None, selected from DEFAULT_TAX_BY_CATEGORY by fund category.

    Returns a SimulationResult.
    """
    if fund_name not in FUND_DATA:
        raise KeyError(f"Unknown fund '{fund_name}'. Use list_funds() to see available options.")

    meta = FUND_DATA[fund_name]
    category = meta["category"]

    annual_return = expected_return_override
    if annual_return is None:
        annual_return = _cagr_from_cumulative(meta["cum_return"], meta["horizon_years"])

    if tax_rate is None:
        tax_rate = DEFAULT_TAX_BY_CATEGORY.get(category, 0.20)

    months = int(round(years * 12))
    r_month = _monthly_rate_from_annual(annual_return)
    fee_month = annual_fee / 12.0

    balance = float(initial_amount)
    total_contributed = float(initial_amount)
    monthly_trajectory = []

    # Monthly contribution growth per month (convert annual increase to monthly step)
    contrib = float(monthly_contribution)
    monthly_increase = (1.0 + contribution_increase_rate) ** (1.0 / 12.0) - 1.0 if contribution_increase_rate != 0 else 0.0

    for m in range(months):
        # Optionally add contribution at beginning
        if contributions_at_beginning and contrib > 0:
            balance += contrib
            total_contributed += contrib

        # Grow
        balance *= (1.0 + r_month)

        # Fees (as a percentage of current AUM)
        fee_amt = balance * fee_month
        balance -= fee_amt

        # Contribution at end
        if not contributions_at_beginning and contrib > 0:
            balance += contrib
            total_contributed += contrib

        monthly_trajectory.append(balance)

        # Increase next month's contribution
        if monthly_increase != 0.0 and contrib > 0:
            contrib *= (1.0 + monthly_increase)

    gross_final_value = balance
    gains_before_tax = gross_final_value - total_contributed
    tax_paid = max(0.0, gains_before_tax) * tax_rate  # tax only on positive gains
    net_final_value = gross_final_value - tax_paid
    net_profit_after_tax = net_final_value - total_contributed

    return SimulationResult(
        fund_name=fund_name,
        category=category,
        assumed_annual_return=annual_return,
        annual_fee=annual_fee,
        tax_rate=tax_rate,
        years=years,
        initial_amount=initial_amount,
        monthly_contribution=monthly_contribution,
        total_contributed=total_contributed,
        gross_final_value=gross_final_value,
        gains_before_tax=gains_before_tax,
        tax_paid=tax_paid,
        net_final_value=net_final_value,
        net_profit_after_tax=net_profit_after_tax,
        monthly_trajectory=monthly_trajectory,
    )

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

if __name__ == "__main__":
    # Example usage
    res = simulate_investment(
        fund_name="ATTIJARI ACTIONS",
        initial_amount=100000.0,
        monthly_contribution=3000.0,
        years=5,
        annual_fee=0.018,  # 1.8%/yr
    )
    print(summarize(res))
