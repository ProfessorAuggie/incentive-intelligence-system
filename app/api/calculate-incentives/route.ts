import { NextResponse } from 'next/server'
import { calculateAllIncentives } from '../../../services/incentiveEngine'

export async function POST() {
  const res = await calculateAllIncentives()
  return NextResponse.json({ ok: true, count: res.length })
}
