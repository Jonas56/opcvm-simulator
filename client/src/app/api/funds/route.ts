import { NextResponse } from "next/server";
import { FundInfo } from "@/types/fund";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

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

    const fundsData = await response.json();

    const fundsRecord: Record<string, FundInfo> = {};
    fundsData.funds.forEach((fund: FundInfo) => {
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
