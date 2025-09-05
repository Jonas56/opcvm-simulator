import { NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

// Define interface for fund data to avoid 'any' type
interface Fund {
  name: string;
  category: string;
  annual_return: number;
  volatility: number;
  inception_date: string;
}

interface FundsResponse {
  funds: Fund[];
}

export async function GET() {
  try {
    const response = await fetch(`${BACKEND_URL}/api/v1/funds`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Backend responded with status: ${response.status}`);
    }

    const fundsData: FundsResponse = await response.json();

    const fundsRecord: Record<string, Fund> = {};
    fundsData.funds.forEach((fund: Fund) => {
      fundsRecord[fund.name] = fund;
    });

    return NextResponse.json(fundsRecord);
  } catch (error) {
    console.error("Error fetching funds:", error);
    return NextResponse.json(
      { error: "Failed to fetch funds data" },
      { status: 500 }
    );
  }
}