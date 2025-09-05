"use client";

import { useMemo, useState, useEffect } from "react";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AppHeader } from "@/components/simulation/AppHeader";
import { SimulationInputs } from "@/components/simulation/SimulationInputs";
import { SimulationResults } from "@/components/simulation/SimulationResults";
import { ProjectionChart } from "@/components/simulation/ProjectionChart";
import { FundInfo } from "@/components/simulation/FundInfo";
import { SimulationType, SimulationResult } from "@/types/simulation";
import { useFunds } from "@/hooks/useFunds";

export default function Home() {
  const [fund, setFund] = useState<string>("");
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

  // Use the custom hook to fetch funds data
  const { funds, loading: fundsLoading, error: fundsError } = useFunds();

  // Automatically select the first fund when funds data loads
  useEffect(() => {
    if (funds && Object.keys(funds).length > 0 && !fund) {
      const firstFundKey = Object.keys(funds)[0];
      const firstFundName = funds[firstFundKey].name;
      setFund(firstFundName);
    }
  }, [funds, fund]);

  // Get current fund information
  const currentFundInfo = useMemo(() => {
    if (!funds || !fund) return null;
    // Find the fund by name
    const fundEntry = Object.entries(funds).find(
      ([, fundInfo]) => fundInfo.name === fund
    );
    return fundEntry ? fundEntry[1] : null;
  }, [funds, fund]);

  async function runSimulation() {
    if (!fund) {
      console.error("No fund selected");
      return;
    }

    try {
      setLoading(true);
      const endpoint =
        simulationType === "deterministic"
          ? "/api/simulate"
          : "/api/mc-simulate";

      const requestBody = {
        fund_name: fund,
        initial_investment: initial,
        monthly_contribution: monthly,
        investment_horizon: years,
        ...(simulationType === "monte-carlo" && {
          num_simulations: nPaths,
          confidence_level: 0.95,
        }),
      };

      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });

      if (!res.ok) {
        const errorData = await res.json();
        console.error("Simulation failed:", errorData);
        return;
      }

      const data = await res.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  }

  const handleSimulationTypeChange = (type: SimulationType) => {
    setSimulationType(type);
    setResult(null);
  };

  return (
    <TooltipProvider>
      <div className="min-h-screen bg-white">
        <div className="p-8 max-w-7xl mx-auto space-y-6">
          <AppHeader />

          {/* Data Caveat Message */}
          <Card className="border-amber-200 bg-amber-50">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <Badge variant="warning" className="shrink-0">
                  ⚠️ Important Notice
                </Badge>
                <div className="text-sm text-amber-800">
                  <strong>Data Disclaimer:</strong> The fund data and
                  performance metrics shown in this simulator do not reflect
                  current market conditions. We are actively working on
                  synchronizing with real-time market data. Please use this tool
                  for educational and planning purposes only.
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Fund Information Section */}
          <FundInfo fundInfo={currentFundInfo} mad={mad} />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <SimulationInputs
              funds={funds}
              fundsLoading={fundsLoading}
              fundsError={fundsError}
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
      </div>
    </TooltipProvider>
  );
}
