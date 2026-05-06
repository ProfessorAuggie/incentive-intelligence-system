import { NextResponse } from 'next/server'
import prisma from '../../../lib/prisma'

export const dynamic = 'force-dynamic'

export async function GET() {
  const totalPayout = await prisma.incentive.aggregate({ _sum: { payout: true } })
  const totalEmployees = await prisma.employee.count()
  const anomaliesCount = await prisma.incentive.count({ where: { anomalies: { isEmpty: false } } })
  const avgIncentive = await prisma.incentive.aggregate({ _avg: { payout: true } })

  return NextResponse.json({ totalPayout: totalPayout._sum.payout || 0, avgIncentive: avgIncentive._avg.payout || 0, totalEmployees, anomaliesCount })
}
