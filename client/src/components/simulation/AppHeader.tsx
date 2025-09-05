"use client";

import { Badge } from "@/components/ui/badge";
import { LineChart as LineChartIcon, Rocket } from "lucide-react";

export function AppHeader() {
  return (
    <header className="flex items-center justify-between">
      <div>
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <LineChartIcon className="h-6 w-6 dark:text-primary" /> OPCVM
          Investment Simulator
        </h1>
        <p className="text-sm text-muted-background mt-1">
          Model long-term outcomes of recurring investments into Moroccan funds.
        </p>
      </div>
      <div className="flex items-center gap-2">
        <Badge variant="secondary" className="gap-1">
          <Rocket className="h-3.5 w-3.5" /> Beta
        </Badge>
      </div>
    </header>
  );
}
