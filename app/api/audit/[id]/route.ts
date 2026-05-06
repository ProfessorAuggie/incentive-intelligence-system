import { NextResponse } from 'next/server'
import prisma from '../../../../lib/prisma'

export async function GET(req: Request, { params }: any) {
  const { id } = params
  const rec = await prisma.incentive.findUnique({ where: { id }, include: { employee: true, performance: true } })
  return NextResponse.json(rec)
}
