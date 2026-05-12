import { prisma } from "@/lib/prisma";
import { NextResponse } from "next/server";

export async function GET() {
  try {
    const anomalies =
      await prisma.incentive.findMany({
        where: {
          anomalyFlag: true,
        },
        include: {
          employee: true,
        },
      });

    return NextResponse.json(anomalies);
  } catch (error) {
    console.error(error);

    return NextResponse.json({
      error: "Failed to fetch anomalies",
    });
  }
}
