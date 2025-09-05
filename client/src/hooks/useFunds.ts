import { useState, useEffect } from "react";
import { FundInfo } from "@/types/fund";

interface UseFundsReturn {
  funds: Record<string, FundInfo> | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useFunds(): UseFundsReturn {
  const [funds, setFunds] = useState<Record<string, FundInfo> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchFunds = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch("/api/funds");

      if (!response.ok) {
        throw new Error(`Failed to fetch funds: ${response.status}`);
      }

      const data = await response.json();
      setFunds(data);
    } catch (err) {
      console.error("Error fetching funds:", err);
      setError(err instanceof Error ? err.message : "Failed to fetch funds");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFunds();
  }, []);

  return {
    funds,
    loading,
    error,
    refetch: fetchFunds,
  };
}
