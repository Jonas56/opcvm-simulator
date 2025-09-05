import { NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function POST(req: Request) {
  try {
    const body = await req.json();

    // Use the new backend server structure for deterministic simulation
    const res = await fetch(`${BACKEND_URL}/api/v1/simulation/deterministic`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const errorData = await res.json();
      console.error("Backend error:", errorData);
      return NextResponse.json(
        { error: errorData.detail || errorData.message || "Simulation failed" },
        { status: res.status }
      );
    }
    const data = await res.json();

    return NextResponse.json(data);
  } catch (error) {
    console.error("Error in simulation:", error);
    return NextResponse.json(
      { error: "Failed to perform simulation" },
      { status: 500 }
    );
  }
}
