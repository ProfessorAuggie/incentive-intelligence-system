import { NextResponse } from 'next/server'
import { resetSharedData } from '../../../services/dataProducer'

export const dynamic = 'force-dynamic'

export async function POST() {
  const result = await resetSharedData()

  console.info(
    `[reset-data] deletedIncentives=${result.deleted.incentives} deletedPerformances=${result.deleted.performances} deletedEmployees=${result.deleted.employees} seededEmployees=${result.seeded.employeesInserted} seededPerformances=${result.seeded.performancesInserted}`
  )

  return NextResponse.json({
    ok: true,
    ...result
  })
}
