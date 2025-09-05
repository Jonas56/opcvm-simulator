export type SimulationType = "deterministic" | "monte-carlo";

export interface SimulationResult {
  fund_name: string;
  category: string;
  assumed_annual_return: number;
  annual_fee?: number;
  tax_rate?: number;
  years: number;
  gross_final_value: number;
  net_final_value: number;
  net_profit_after_tax: number;
  tax_paid: number;
  total_contributed: number;
  initial_amount?: number;
  monthly_contribution?: number;
  trajectory?: Array<{ month: number; value: number }>;
  // Monte Carlo specific fields
  assumed_annual_vol?: number;
  n_paths?: number;
  percentiles?: {
    p5: number;
    p50: number;
    p95: number;
  };
  prob_loss?: number;
  risk_metrics?: {
    annualized_vol: number;
    sharpe: number;
    sortino: number;
    max_drawdown_mean: number;
    calmar: number;
  };
}
