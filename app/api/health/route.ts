import { NextResponse } from 'next/server'
import { getHealthSnapshot } from '../../../services/dataProducer'

export const dynamic = 'force-dynamic'

export async function GET() {
  const snapshot = await getHealthSnapshot()
  return NextResponse.json(snapshot)
}
