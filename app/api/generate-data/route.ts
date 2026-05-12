import { prisma } from "@/lib/prisma";
import { NextResponse } from "next/server";

export async function POST() {
  try {
    for (let i = 1; i <= 20; i++) {
      const employee = await prisma.employee.create({
        data: {
          name: `Employee ${i}`,
          region: ["US", "EMEA", "APAC"][i % 3],
          role: i % 5 === 0 ? "Manager" : "Sales",
        },
      });

      await prisma.performance.create({
        data: {
          employeeId: employee.id,
          salesAmount: Math.floor(Math.random() * 50000),
          salesTarget: 30000,
          previousSales: 25000,
          quarter: "Q1-2026",
        },
      });
    }

    return NextResponse.json({
      success: true,
      message: "Dummy data generated"
    });
  } catch (error) {
    console.error(error);

    return NextResponse.json({
      success: false,
      error,
    });
  }
}
