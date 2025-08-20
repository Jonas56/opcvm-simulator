"use client";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import {
  Tooltip as UiTooltip,
  TooltipTrigger,
  TooltipContent,
} from "@/components/ui/tooltip";
import { Info, Play, BarChart3 } from "lucide-react";

const FUNDS = [
  "ATTIJARI ACTIONS",
  "ATTIJARI AL MOUCHARAKA",
  "ATTIJARI DIVIDEND FUND",
  "ATTIJARI PATRIMOINE VALEURS",
  "FCP ATTIJARI GOLD",
  "ATTIJARI DIVERSIFIE",
  "ATTIJARI PATRIMOINE DIVERSIFIE",
  "WG OBLIGATIONS",
  "ATTIJARI PATRIMOINE TAUX",
  "PATRIMOINE OBLIGATIONS",
  "ATTIJARI MONETAIRE PLUS",
];

type SimulationType = "deterministic" | "monte-carlo";

interface SimulationInputsProps {
  fund: string;
  setFund: (fund: string) => void;
  initial: number;
  setInitial: (initial: number) => void;
  monthly: number;
  setMonthly: (monthly: number) => void;
  years: number;
  setYears: (years: number) => void;
  fee: number;
  setFee: (fee: number) => void;
  nPaths: number;
  setNPaths: (nPaths: number) => void;
  simulationType: SimulationType;
  setSimulationType: (type: SimulationType) => void;
  onRunSimulation: () => void;
  loading: boolean;
  totalContributed: number;
  mad: Intl.NumberFormat;
  percent: Intl.NumberFormat;
}

export function SimulationInputs({
  fund,
  setFund,
  initial,
  setInitial,
  monthly,
  setMonthly,
  years,
  setYears,
  fee,
  setFee,
  nPaths,
  setNPaths,
  simulationType,
  setSimulationType,
  onRunSimulation,
  loading,
  totalContributed,
  mad,
  percent,
}: SimulationInputsProps) {
  const handleSimulationTypeChange = (type: SimulationType) => {
    setSimulationType(type);
    // Clear results when switching types - this will be handled by parent
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Inputs</CardTitle>
        <CardDescription>
          Adjust parameters and run a simulation.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="fund">Fund</Label>
          <select
            id="fund"
            value={fund}
            onChange={(e) => setFund(e.target.value)}
            className="flex h-10 w-full rounded-md border border-neutral-200 bg-white px-3 py-2 text-sm ring-offset-background placeholder:text-neutral-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-400 focus-visible:ring-offset-2 dark:border-neutral-800 dark:bg-neutral-950 dark:text-neutral-50"
          >
            {FUNDS.map((k) => (
              <option key={k} value={k}>
                {k}
              </option>
            ))}
          </select>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="initial">Initial amount</Label>
              <span className="text-xs text-neutral-500">
                {mad.format(initial)}
              </span>
            </div>
            <Input
              id="initial"
              type="number"
              value={initial}
              onChange={(e) => setInitial(+e.target.value)}
              placeholder="e.g. 100000"
            />
          </div>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="monthly">Monthly contribution</Label>
              <span className="text-xs text-neutral-500">
                {mad.format(monthly)}
              </span>
            </div>
            <Input
              id="monthly"
              type="number"
              value={monthly}
              onChange={(e) => setMonthly(+e.target.value)}
              placeholder="e.g. 3000"
            />
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Label>Investment horizon</Label>
              <UiTooltip>
                <TooltipTrigger className="inline-flex">
                  <Info className="h-4 w-4 text-neutral-400" />
                </TooltipTrigger>
                <TooltipContent>Number of years invested.</TooltipContent>
              </UiTooltip>
            </div>
            <span className="text-xs text-neutral-500">{years} years</span>
          </div>
          <Slider
            value={[years]}
            min={1}
            max={30}
            step={1}
            onValueChange={(v: number[]) => setYears(v[0])}
          />
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Label>Annual management fee</Label>
              <UiTooltip>
                <TooltipTrigger className="inline-flex">
                  <Info className="h-4 w-4 text-neutral-400" />
                </TooltipTrigger>
                <TooltipContent>
                  Annual fee applied to assets under management.
                </TooltipContent>
              </UiTooltip>
            </div>
            <span className="text-xs text-neutral-500">
              {percent.format(fee)}
            </span>
          </div>
          <Slider
            value={[fee]}
            min={0}
            max={0.05}
            step={0.001}
            onValueChange={(v: number[]) => setFee(+v[0].toFixed(3))}
          />
        </div>

        {simulationType === "monte-carlo" && (
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Label>Number of simulations</Label>
                <UiTooltip>
                  <TooltipTrigger className="inline-flex">
                    <Info className="h-4 w-4 text-neutral-400" />
                  </TooltipTrigger>
                  <TooltipContent>
                    Number of Monte Carlo simulation paths (higher = more
                    accurate but slower).
                  </TooltipContent>
                </UiTooltip>
              </div>
              <span className="text-xs text-neutral-500">
                {nPaths.toLocaleString()}
              </span>
            </div>
            <Slider
              value={[nPaths]}
              min={1000}
              max={10000}
              step={500}
              onValueChange={(v: number[]) => setNPaths(v[0])}
            />
          </div>
        )}
      </CardContent>
      <CardFooter className="flex flex-col gap-4">
        <div className="text-sm text-neutral-500 w-full">
          Total contributed:{" "}
          <span className="font-medium text-neutral-900 dark:text-neutral-100">
            {mad.format(totalContributed)}
          </span>
        </div>
        <div className="flex gap-2 w-full">
          <Button
            onClick={() => handleSimulationTypeChange("deterministic")}
            variant={simulationType === "deterministic" ? "default" : "outline"}
            className="flex-1 gap-2"
          >
            <Play className="h-4 w-4" />
            Deterministic
          </Button>
          <Button
            onClick={() => handleSimulationTypeChange("monte-carlo")}
            variant={simulationType === "monte-carlo" ? "default" : "outline"}
            className="flex-1 gap-2"
          >
            <BarChart3 className="h-4 w-4" />
            MC Simulation
          </Button>
        </div>
        <Button
          onClick={onRunSimulation}
          disabled={loading}
          className="w-full gap-2"
        >
          <Play className="h-4 w-4" />{" "}
          {loading
            ? "Simulating..."
            : `Run ${
                simulationType === "deterministic"
                  ? "Deterministic"
                  : "Monte Carlo"
              } Simulation`}
        </Button>
      </CardFooter>
    </Card>
  );
}
