import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ name: string }> }
) {
  try {
    const { name: fundName } = await params;

    // Fetch specific fund data from the new backend server structure
    const response = await fetch(
      `${BACKEND_URL}/api/v1/funds/${encodeURIComponent(fundName)}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      if (response.status === 404) {
        return NextResponse.json(
          { error: `Fund '${fundName}' not found` },
          { status: 404 }
        );
      }
      throw new Error(`Backend responded with status: ${response.status}`);
    }

    const fundData = await response.json();

    // Return the fund data as JSON
    return NextResponse.json(fundData);
  } catch (error) {
    console.error("Error fetching fund:", error);
    return NextResponse.json(
      { error: "Failed to fetch fund data" },
      { status: 500 }
    );
  }
}
