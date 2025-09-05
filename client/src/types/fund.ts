export interface FundInfo {
  name: string;
  nav: number; // Net Asset Value
  risk_profile: "low" | "medium" | "high";
  recommended_holding: "short" | "medium" | "long";
  objective: string;
  strategy: string;
}
