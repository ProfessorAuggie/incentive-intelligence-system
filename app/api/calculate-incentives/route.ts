import { prisma } from "@/lib/prisma";
import { NextResponse } from "next/server";

export async function POST() {
  try {
    const performances = await prisma.performance.findMany({
      include: {
        employee: true,
      },
    });

    for (const perf of performances) {
      let rate = 0;

      if (perf.salesAmount >= perf.salesTarget * 1.5) {
        rate = 0.2;
      } else if (perf.salesAmount >= perf.salesTarget) {
        rate = 0.1;
      }

      let bonus = 0;

      const growth =
        ((perf.salesAmount - perf.previousSales) /
          perf.previousSales) *
        100;

      if (growth > 20) {
        bonus += 0.05;
      }

      if (perf.employee.role === "Manager") {
        bonus += 0.03;
      }

      const payout =
        perf.salesAmount * (rate + bonus);

      const anomaly =
        payout > perf.salesAmount * 0.5;

      await prisma.incentive.create({
        data: {
          employeeId: perf.employeeId,
          calculatedAmount: perf.salesAmount * rate,
          bonusAmount: perf.salesAmount * bonus,
          finalPayout: payout,
          anomalyFlag: anomaly,
          anomalyReason: anomaly
            ? "Suspicious payout"
            : null,
        },
      });
    }

    return NextResponse.json({
      success: true,
      message: "Incentives calculated"
    });
  } catch (error) {
    console.error(error);

    return NextResponse.json({
      success: false,
      error,
    });
  }
}
