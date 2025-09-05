import { NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function POST(req: Request) {
  try {
    const body = await req.json();

    // Use the new backend server structure for Monte Carlo simulation
    const res = await fetch(`${BACKEND_URL}/api/v1/simulation/monte-carlo`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const errorData = await res.json();
      return NextResponse.json(
        { error: errorData.detail || "Monte Carlo simulation failed" },
        { status: res.status }
      );
    }

    const data = await res.json();

    return NextResponse.json(data);
  } catch (error) {
    console.error("Error in Monte Carlo simulation:", error);
    return NextResponse.json(
      { error: "Failed to perform Monte Carlo simulation" },
      { status: 500 }
    );
  }
}
