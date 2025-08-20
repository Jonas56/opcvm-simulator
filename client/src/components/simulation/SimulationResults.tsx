"use client";

import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

type SimulationType = "deterministic" | "monte-carlo";

interface SimulationResultsProps {
  result: any;
  simulationType: SimulationType;
  mad: Intl.NumberFormat;
  percent: Intl.NumberFormat;
}

export function SimulationResults({
  result,
  simulationType,
  mad,
  percent,
}: SimulationResultsProps) {
  if (!result) {
    return (
      <Card className="h-full">
        <CardHeader>
          <CardTitle>Results</CardTitle>
          <CardDescription>
            {simulationType === "deterministic"
              ? "Key performance indicators after fees and tax."
              : "Probabilistic outcomes with risk metrics."}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-sm text-neutral-500">
            Run a simulation to see projected outcomes.
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Results</CardTitle>
        <CardDescription>
          {simulationType === "deterministic"
            ? "Key performance indicators after fees and tax."
            : "Probabilistic outcomes with risk metrics."}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-neutral-500">Category</span>
            <Badge variant="secondary">{result.category}</Badge>
          </div>

          {simulationType === "deterministic" ? (
            <DeterministicResults result={result} mad={mad} percent={percent} />
          ) : (
            <MonteCarloResults result={result} mad={mad} percent={percent} />
          )}
        </div>
      </CardContent>
    </Card>
  );
}

function DeterministicResults({
  result,
  mad,
  percent,
}: {
  result: any;
  mad: Intl.NumberFormat;
  percent: Intl.NumberFormat;
}) {
  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="rounded-lg border border-neutral-200 p-4 dark:border-neutral-800">
        <div className="text-xs text-neutral-500">Assumed annual return</div>
        <div className="text-lg font-semibold">
          {percent.format(result.assumed_annual_return || 0)}
        </div>
      </div>
      <div className="rounded-lg border border-neutral-200 p-4 dark:border-neutral-800">
        <div className="text-xs text-neutral-500">Net final value</div>
        <div className="text-lg font-semibold">
          {mad.format(result.net_final_value || 0)}
        </div>
      </div>
      <div className="rounded-lg border border-neutral-200 p-4 dark:border-neutral-800">
        <div className="text-xs text-neutral-500">Net profit (after tax)</div>
        <div className="text-lg font-semibold">
          {mad.format(result.net_profit_after_tax || 0)}
        </div>
      </div>
      <div className="rounded-lg border border-neutral-200 p-4 dark:border-neutral-800">
        <div className="text-xs text-neutral-500">Tax paid</div>
        <div className="text-lg font-semibold">
          {mad.format(result.tax_paid || 0)}
        </div>
      </div>
    </div>
  );
}

function MonteCarloResults({
  result,
  mad,
  percent,
}: {
  result: any;
  mad: Intl.NumberFormat;
  percent: Intl.NumberFormat;
}) {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-lg border border-neutral-200 p-4 dark:border-neutral-800">
          <div className="text-xs text-neutral-500">Assumed annual return</div>
          <div className="text-lg font-semibold">
            {percent.format(result.assumed_annual_return || 0)}
          </div>
        </div>
        <div className="rounded-lg border border-neutral-200 p-4 dark:border-neutral-800">
          <div className="text-xs text-neutral-500">Annual volatility</div>
          <div className="text-lg font-semibold">
            {percent.format(result.assumed_annual_vol || 0)}
          </div>
        </div>
      </div>

      <div className="rounded-lg border border-neutral-200 p-4 dark:border-neutral-800">
        <div className="text-xs text-neutral-500 mb-2">Percentile Outcomes</div>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <div className="text-xs text-neutral-500">P5 (Worst 5%)</div>
            <div className="text-sm font-semibold">
              {mad.format(result.percentiles?.p5 || 0)}
            </div>
          </div>
          <div>
            <div className="text-xs text-neutral-500">P50 (Median)</div>
            <div className="text-sm font-semibold">
              {mad.format(result.percentiles?.p50 || 0)}
            </div>
          </div>
          <div>
            <div className="text-xs text-neutral-500">P95 (Best 5%)</div>
            <div className="text-sm font-semibold">
              {mad.format(result.percentiles?.p95 || 0)}
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-lg border border-neutral-200 p-4 dark:border-neutral-800">
          <div className="text-xs text-neutral-500">Probability of loss</div>
          <div className="text-lg font-semibold">
            {percent.format(result.prob_loss || 0)}
          </div>
        </div>
        <div className="rounded-lg border border-neutral-200 p-4 dark:border-neutral-800">
          <div className="text-xs text-neutral-500">Sharpe ratio</div>
          <div className="text-lg font-semibold">
            {(result.risk_metrics?.sharpe || 0).toFixed(2)}
          </div>
        </div>
      </div>
    </div>
  );
}
