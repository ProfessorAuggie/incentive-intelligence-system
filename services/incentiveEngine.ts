import prisma from '../lib/prisma'
import { validateCalculationInput } from './validation'

export async function calculateIncentiveForPerformance(perf: any, employee: any) {
  validateCalculationInput(perf, employee)

  let rate = 0
  const sales = perf.sales
  const target = perf.target
  const growth = perf.growth

  if (sales >= target * 1.5) rate = 0.2
  else if (sales >= target) rate = 0.1

  if (growth > 20) rate += 0.05
  if (employee.isManager) rate += 0.03

  const payout = Number((sales * rate).toFixed(2))
  const breakdown = {
    baseRate: rate,
    sales,
    target,
    growth,
    rules: {
      targetReached: sales >= target,
      superTargetReached: sales >= target * 1.5,
      growthBonusApplied: growth > 20,
      managerOverrideApplied: Boolean(employee?.isManager)
    }
  }

  return { payout, breakdown }
}

export async function calculateAllIncentives() {
  console.info('[data-flow-producer] Starting incentive calculation for all performances')

  const performances = await prisma.performance.findMany({ include: { employee: true } })
  const created: any[] = []
  let processedCount = 0
  let failedCount = 0

  for (const p of performances) {
    processedCount += 1
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
      failedCount += 1
      console.error('[incentiveEngine] Calculation error:', err)
    }
  }

  console.info('[data-flow-producer] Incentives calculated and persisted', {
    processed: processedCount,
    upserted: created.length,
    failed: failedCount
  })

  console.info('[incentiveEngine] processed=${processedCount} upserted=${created.length} failed=${failedCount}')

  return {
    processedCount,
    upsertedCount: created.length,
    failedCount,
    incentives: created
  }
}
