"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
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

interface ProjectionChartProps {
  result: SimulationResult | null;
  simulationType: "deterministic" | "monte-carlo";
}

export function ProjectionChart({
  result,
  simulationType,
}: ProjectionChartProps) {
  // Only show chart for deterministic simulations
  if (!result || simulationType !== "deterministic") {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Projection</CardTitle>
        <CardDescription>Growth trajectory over time.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={result?.trajectory ?? []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="value"
                stroke="#2563eb"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
