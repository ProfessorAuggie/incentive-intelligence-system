import prisma from '../lib/prisma'

export function detectAnomaliesFor(incentive: any, performance: any) {
  const anomalies: string[] = []
  if (performance.sales < performance.target * 0.5 && incentive.payout > 0) {
    anomalies.push('High payout with low sales')
  }
  if (performance.sales > performance.target && incentive.payout === 0) {
    anomalies.push('Zero payout with high sales')
  }
  if (performance.growth > 100) anomalies.push('Sudden spike in growth')
  return anomalies
}

export async function scanAllAnomalies() {
  const incentives = await prisma.incentive.findMany({ include: { performance: true } })
  const results: any[] = []
  for (const inc of incentives) {
    const a = detectAnomaliesFor(inc, inc.performance)
    if (a.length) {
      results.push({ incentive: inc, anomalies: a })
      await prisma.incentive.update({ where: { id: inc.id }, data: { anomalies: a } })
    }
  }
  return results
}
