import { NextResponse } from 'next/server'
import { calculateAllIncentives } from '../../../services/incentiveEngine'
import { scanAllAnomalies } from '../../../services/anomalyDetection'

export async function POST() {
  const calculation = await calculateAllIncentives()
  const anomalyScan = await scanAllAnomalies()

  return NextResponse.json({
    ok: true,
    processedCount: calculation.processedCount,
    upsertedCount: calculation.upsertedCount,
    failedCount: calculation.failedCount,
    anomalyProcessedCount: anomalyScan.processedCount,
    anomalyFlaggedCount: anomalyScan.flaggedCount,
    incentives: calculation.incentives,
    anomalies: anomalyScan.results
  })
}
