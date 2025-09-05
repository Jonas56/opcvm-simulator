from opcvm_simulator import simulate_investment, summarize, list_funds

# See available funds and their assumed annualized returns
# print(list_funds())

# Simulate 5 years in ATTIJARI ACTIONS with 1.8% fee
res = simulate_investment(
    fund_name="ATTIJARI ACTIONS",
    initial_amount=100_000,     # MAD
    monthly_contribution=3_000, # MAD
    years=5,
    annual_fee=0.018            # 1.8%/yr
)
print(summarize(res))