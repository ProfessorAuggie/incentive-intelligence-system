import { NextResponse } from 'next/server'
import prisma from '../../../lib/prisma'
import { validateEmployeePayload, validatePerformance } from '../../../services/validation'

export async function POST() {
  const regions = ['North', 'South', 'East', 'West']
  const roles = ['Sales Rep', 'Senior Rep', 'Manager']
  let employeesInserted = 0
  let performancesInserted = 0

  for (let i = 1; i <= 30; i += 1) {
    const isManager = i % 10 === 0
    const employeePayload = {
      name: `Employee ${i}`,
      role: roles[i % roles.length],
      region: regions[i % regions.length],
      isManager
    }

    validateEmployeePayload(employeePayload)

    const emp = await prisma.employee.create({ data: employeePayload })
    employeesInserted += 1

    for (const quarter of ['Q1', 'Q2', 'Q3', 'Q4']) {
      const performancePayload = {
        employeeId: emp.id,
        quarter,
        year: 2025,
        sales: Number((50000 + Math.random() * 150000).toFixed(2)),
        target: Number((50000 + Math.random() * 100000).toFixed(2)),
        growth: Number((Math.random() * 120).toFixed(2))
      }

      validatePerformance(performancePayload)

      await prisma.performance.create({ data: performancePayload })
      performancesInserted += 1
    }
  }

  console.info(`[generate-data] employeesInserted=${employeesInserted} performancesInserted=${performancesInserted}`)

  return NextResponse.json({
    ok: true,
    employeesInserted,
    performancesInserted
  })
}
