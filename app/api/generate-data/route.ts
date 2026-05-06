import { NextResponse } from 'next/server'
import prisma from '../../../lib/prisma'

export async function POST() {
  // simple seeding of dummy data
  const regions = ['North', 'South', 'East', 'West']
  const roles = ['Sales Rep', 'Senior Rep', 'Manager']

  for (let i = 1; i <= 30; i++) {
    const isManager = i % 10 === 0
    const emp = await prisma.employee.create({ data: { name: `Employee ${i}`, role: roles[i % roles.length], region: regions[i % regions.length], isManager } })
    for (const q of ['Q1', 'Q2', 'Q3', 'Q4']) {
      await prisma.performance.create({ data: { employeeId: emp.id, quarter: q, year: 2025, sales: Math.random() * 200000, target: 50000 + Math.random() * 100000, growth: Math.random() * 120 } })
    }
  }

  return NextResponse.json({ ok: true })
}
