import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { TrendingUp, ShieldAlert, Clock } from "lucide-react";
import type { FundInfo } from "@/types/fund";

interface FundInfoProps {
  fundInfo: FundInfo | null;
  mad: Intl.NumberFormat;
}

export function FundInfo({ fundInfo, mad }: FundInfoProps) {
  if (!fundInfo) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Fund Information</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Loading fund information...</p>
        </CardContent>
      </Card>
    );
  }

  const getRiskVariant = (
    risk: string
  ): "success" | "warning" | "destructive" => {
    switch (risk) {
      case "low":
        return "success";
      case "medium":
        return "warning";
      case "high":
      default:
        return "destructive";
    }
  };

  const getHoldingLabel = (holding: string) => {
    switch (holding) {
      case "short":
        return "Short term";
      case "medium":
        return "Medium term";
      case "long":
      default:
        return "Long term";
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Fund Information</CardTitle>
        <p className="text-sm text-neutral-500">{fundInfo.name}</p>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Top stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="rounded-lg border border-neutral-200 bg-white p-4">
            <div className="flex items-center gap-3">
              <div className="rounded-md bg-blue-50 p-2">
                <TrendingUp className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <p className="text-xs text-neutral-500">NAV</p>
                <p className="text-lg font-semibold">
                  {mad.format(fundInfo.nav)}
                </p>
              </div>
            </div>
          </div>

          <div className="rounded-lg border border-neutral-200 bg-white p-4">
            <div className="flex items-center gap-3">
              <div className="rounded-md bg-red-50 p-2">
                <ShieldAlert className="h-5 w-5 text-red-600" />
              </div>
              <div>
                <p className="text-xs text-neutral-500">Risk profile</p>
                <Badge variant={getRiskVariant(fundInfo.risk_profile)}>
                  {fundInfo.risk_profile.toUpperCase()}
                </Badge>
              </div>
            </div>
          </div>

          <div className="rounded-lg border border-neutral-200 bg-white p-4">
            <div className="flex items-center gap-3">
              <div className="rounded-md bg-neutral-100 p-2">
                <Clock className="h-5 w-5 text-neutral-700" />
              </div>
              <div>
                <p className="text-xs text-neutral-500">Recommended holding</p>
                <Badge variant="secondary">
                  {getHoldingLabel(fundInfo.recommended_holding)}
                </Badge>
              </div>
            </div>
          </div>
        </div>

        <Separator />

        {/* Objective and Strategy */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <h4 className="font-medium text-sm text-neutral-700">
              Investment Objective
            </h4>
            <p className="text-sm leading-relaxed text-neutral-700">
              {fundInfo.objective}
            </p>
          </div>
          <div className="space-y-2">
            <h4 className="font-medium text-sm text-neutral-700">
              Investment Strategy
            </h4>
            <p className="text-sm leading-relaxed text-neutral-700">
              {fundInfo.strategy}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
