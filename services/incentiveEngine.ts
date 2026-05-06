import prisma from '../lib/prisma'
import { validatePerformance } from './validation'

export async function calculateIncentiveForPerformance(perf: any, employee: any) {
  validatePerformance(perf)

  let rate = 0
  const sales = perf.sales
  const target = perf.target
  const growth = perf.growth

  if (sales >= target * 1.5) rate = 0.2
  else if (sales >= target) rate = 0.1

  if (growth > 20) rate += 0.05
  if (employee.isManager) rate += 0.03

  const payout = Number((sales * rate).toFixed(2))
  const breakdown = { baseRate: rate, sales, target, growth }

  return { payout, breakdown }
}

export async function calculateAllIncentives() {
  const performances = await prisma.performance.findMany({ include: { employee: true } })
  const created: any[] = []

  for (const p of performances) {
    try {
      const { payout, breakdown } = await calculateIncentiveForPerformance(p, p.employee)
      const rec = await prisma.incentive.upsert({
        where: { performanceId: p.id },
        create: {
          employeeId: p.employeeId,
          performanceId: p.id,
          payout,
          breakdown
        },
        update: { payout, breakdown }
      })
      created.push(rec)
    } catch (err) {
      console.error('calc error', err)
    }
  }

  return created
}
