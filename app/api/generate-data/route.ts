import { NextResponse } from 'next/server'
import { generateDummyData } from '../../../services/dataProducer'

export const dynamic = 'force-dynamic'

export async function POST() {
  const seeded = await generateDummyData()

  console.info(`[generate-data] employeesInserted=${seeded.employeesInserted} performancesInserted=${seeded.performancesInserted}`)

  return NextResponse.json({
    ok: true,
    ...seeded
  })
}
