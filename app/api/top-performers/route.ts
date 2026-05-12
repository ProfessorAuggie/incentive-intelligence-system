import { prisma } from "@/lib/prisma";
import { NextResponse } from "next/server";

export async function GET() {
  try {
    const topPerformers =
      await prisma.performance.findMany({
        orderBy: {
          salesAmount: "desc"
        },
        take: 5,
        include: {
          employee: true
        }
      });

    return NextResponse.json(topPerformers);
  } catch (error) {
    console.error(error);

    return NextResponse.json({
      error: "Failed to fetch top performers"
    });
  }
}
