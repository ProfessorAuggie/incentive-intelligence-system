import { NextResponse } from 'next/server'
import prisma from '../../../lib/prisma'

export async function GET() {
  const top = await prisma.incentive.findMany({ take: 10, orderBy: { payout: 'desc' }, include: { employee: true } })
  return NextResponse.json(top)
}
