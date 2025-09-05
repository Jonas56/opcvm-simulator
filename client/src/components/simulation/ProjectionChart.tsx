"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { SimulationResult } from "@/types/simulation";
import { useMemo } from "react";

interface ProjectionChartProps {
  result: SimulationResult | null;
  simulationType: "deterministic" | "monte-carlo";
}

export function ProjectionChart({
  result,
  simulationType,
}: ProjectionChartProps) {
  // Build 30-year stacked histogram data: net profit, tax paid, fees per year
  const data = useMemo(() => {
    // Only calculate data for deterministic simulations
    if (!result || simulationType !== "deterministic") {
      return [];
    }
    const years = 30;

    const annualReturn = result.assumed_annual_return ?? 0;
    const annualFee = result.annual_fee ?? 0.0;
    const taxRate = result.tax_rate ?? 0.0;

    console.log("annualReturn", annualReturn);
    console.log("annualFee", annualFee);
    console.log("taxRate", taxRate);

    const initial = result.initial_amount ?? 0;
    const monthly = result.monthly_contribution ?? 0;

    const monthlyRate = Math.pow(1 + annualReturn, 1 / 12) - 1;
    const monthlyFee = annualFee / 12;

    let balance = initial;
    let totalContributed = initial;
    let cumulativeFees = 0;

    // Track yearly data for histogram
    const yearlyData: Array<{
      year: number;
      balance: number;
      contributed: number;
      fees: number;
      gains: number;
    }> = [];

    for (let y = 1; y <= years; y++) {
      const startBalance = balance;
      const startFees = cumulativeFees;

      for (let m = 0; m < 12; m++) {
        balance *= 1 + monthlyRate;
        const fee = balance * monthlyFee;
        balance -= fee;
        cumulativeFees += fee;
        balance += monthly;
        totalContributed += monthly;
      }

      const yearFees = cumulativeFees - startFees;
      const yearGains = balance - startBalance - monthly * 12 - yearFees;

      yearlyData.push({
        year: y,
        balance,
        contributed: totalContributed,
        fees: yearFees,
        gains: yearGains,
      });
    }

    // Calculate total tax exactly like the backend
    const grossFinalValue = balance;
    const gainsBeforeTax = Math.max(0, grossFinalValue - totalContributed);
    const totalTax = gainsBeforeTax * taxRate;

    // Distribute tax proportionally based on each year's gains
    const totalGains = yearlyData.reduce(
      (sum, data) => sum + Math.max(0, data.gains),
      0
    );

    const rows: Array<{
      year: string;
      net: number;
      tax: number;
      fees: number;
    }> = [];

    yearlyData.forEach((data) => {
      const yearGains = Math.max(0, data.gains);
      const yearTax = totalGains > 0 ? (yearGains / totalGains) * totalTax : 0;
      const yearNet = yearGains - yearTax;

      rows.push({
        year: `Y${data.year}`,
        net: Math.max(0, yearNet),
        tax: Math.max(0, yearTax),
        fees: Math.max(0, data.fees),
      });
    });

    return rows;
  }, [result, simulationType]);

  // Only show chart for deterministic simulations
  if (!result || simulationType !== "deterministic") {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Projection</CardTitle>
        <CardDescription>
          Annual breakdown: net profit, tax, and fees.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis />
              <Tooltip
                formatter={(value: number | string) =>
                  new Intl.NumberFormat("en-MA", {
                    style: "currency",
                    currency: "MAD",
                    maximumFractionDigits: 0,
                  }).format(Number(value))
                }
              />
              <Legend />
              <Bar dataKey="fees" stackId="a" fill="#f59e0b" name="Fees" />
              <Bar dataKey="tax" stackId="a" fill="#ef4444" name="Tax" />
              <Bar dataKey="net" stackId="a" fill="#10b981" name="Net Profit" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
