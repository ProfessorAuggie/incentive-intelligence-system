import prisma from '../lib/prisma'

export function detectAnomaliesFor(incentive: any, performance: any) {
  const anomalies: string[] = []
  if (performance.sales < performance.target * 0.5 && incentive.payout > 0) {
    anomalies.push('High payout with low sales')
  }
  if (performance.sales >= performance.target && incentive.payout === 0) {
    anomalies.push('Zero payout with high sales')
  }
  return anomalies
}

export async function scanAllAnomalies() {
  const incentives = await prisma.incentive.findMany({ include: { performance: true } })
  const results: any[] = []
  let processedCount = 0
  let flaggedCount = 0

  for (const inc of incentives) {
    processedCount += 1
    const a = detectAnomaliesFor(inc, inc.performance)
    if (a.length) {
      flaggedCount += 1
      results.push({ incentive: inc, anomalies: a })
      await prisma.incentive.update({ where: { id: inc.id }, data: { anomalies: a } })
    }
  }

  console.info(`[anomalyDetection] processed=${processedCount} flagged=${flaggedCount}`)

  return {
    processedCount,
    flaggedCount,
    results
  }
}
