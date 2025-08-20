"use client";

import { useMemo, useState } from "react";
import { TooltipProvider } from "@/components/ui/tooltip";
import { AppHeader } from "@/components/simulation/AppHeader";
import { SimulationInputs } from "@/components/simulation/SimulationInputs";
import { SimulationResults } from "@/components/simulation/SimulationResults";
import { ProjectionChart } from "@/components/simulation/ProjectionChart";
import { SimulationType, SimulationResult } from "@/types/simulation";

export default function Home() {
  const [fund, setFund] = useState("ATTIJARI ACTIONS");
  const [initial, setInitial] = useState(100000);
  const [monthly, setMonthly] = useState(3000);
  const [years, setYears] = useState(5);
  const [fee, setFee] = useState(0.018);
  const [nPaths, setNPaths] = useState(5000);
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [simulationType, setSimulationType] =
    useState<SimulationType>("deterministic");
  const [loading, setLoading] = useState(false);

  const mad = useMemo(
    () =>
      new Intl.NumberFormat("en-MA", {
        style: "currency",
        currency: "MAD",
        maximumFractionDigits: 0,
      }),
    []
  );

  const percent = useMemo(
    () =>
      new Intl.NumberFormat("en-US", {
        style: "percent",
        maximumFractionDigits: 2,
      }),
    []
  );

  const totalContributed = useMemo(
    () => initial + monthly * years * 12,
    [initial, monthly, years]
  );

  async function runSimulation() {
    try {
      setLoading(true);
      const endpoint =
        simulationType === "deterministic"
          ? "/api/simulate"
          : "/api/mc-simulate";

      const requestBody = {
        fund_name: fund,
        initial_amount: initial,
        monthly_contribution: monthly,
        years,
        annual_fee: fee,
        ...(simulationType === "monte-carlo" && { n_paths: nPaths }),
      };

      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });
      const data = await res.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  }

  const handleSimulationTypeChange = (type: SimulationType) => {
    setSimulationType(type);
    setResult(null); // Clear previous results when switching
  };

  return (
    <TooltipProvider>
      <div className="p-8 max-w-5xl mx-auto space-y-6">
        <AppHeader />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <SimulationInputs
            fund={fund}
            setFund={setFund}
            initial={initial}
            setInitial={setInitial}
            monthly={monthly}
            setMonthly={setMonthly}
            years={years}
            setYears={setYears}
            fee={fee}
            setFee={setFee}
            nPaths={nPaths}
            setNPaths={setNPaths}
            simulationType={simulationType}
            setSimulationType={handleSimulationTypeChange}
            onRunSimulation={runSimulation}
            loading={loading}
            totalContributed={totalContributed}
            mad={mad}
            percent={percent}
          />

          <SimulationResults
            result={result}
            simulationType={simulationType}
            mad={mad}
            percent={percent}
          />
        </div>

        <ProjectionChart result={result} simulationType={simulationType} />
      </div>
    </TooltipProvider>
  );
}
