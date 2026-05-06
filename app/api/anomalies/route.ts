import { NextResponse } from 'next/server'
import { scanAllAnomalies } from '../../../services/anomalyDetection'

export async function GET() {
  const results = await scanAllAnomalies()
  return NextResponse.json(results)
}
