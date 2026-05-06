import prisma from '../lib/prisma'
import { validateEmployeePayload, validatePerformance } from './validation'

const regions = ['North', 'South', 'East', 'West']
const roles = ['Sales Rep', 'Senior Rep', 'Manager']

export async function generateDummyData() {
  let employeesInserted = 0
  let performancesInserted = 0

  console.info('[data-flow-producer] Starting dummy data generation...')

  for (let i = 1; i <= 30; i += 1) {
    const isManager = i % 10 === 0
    const employeePayload = {
      name: `Employee ${i}`,
      role: roles[i % roles.length],
      region: regions[i % regions.length],
      isManager
    }

    validateEmployeePayload(employeePayload)

    const employee = await prisma.employee.create({ data: employeePayload })
    employeesInserted += 1

    for (const quarter of ['Q1', 'Q2', 'Q3', 'Q4']) {
      const performancePayload = {
        employeeId: employee.id,
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

  console.info('[data-flow-producer] Generated and persisted', {
    employees: employeesInserted,
    performances: performancesInserted
  })

  return { employeesInserted, performancesInserted }
}

export async function resetSharedData() {
  console.info('[data-flow-producer] Starting database reset and reseed...')

  const incentiveDeleted = await prisma.incentive.deleteMany()
  const performanceDeleted = await prisma.performance.deleteMany()
  const employeeDeleted = await prisma.employee.deleteMany()

  console.info('[data-flow-producer] Deleted previous data', {
    incentives: incentiveDeleted.count,
    performances: performanceDeleted.count,
    employees: employeeDeleted.count
  })

  const seeded = await generateDummyData()

  console.info('[data-flow-producer] Reset complete', {
    deleted: {
      incentives: incentiveDeleted.count,
      performances: performanceDeleted.count,
      employees: employeeDeleted.count
    },
    seeded
  })

  return {
    deleted: {
      incentives: incentiveDeleted.count,
      performances: performanceDeleted.count,
      employees: employeeDeleted.count
    },
    seeded
  }
}

export async function getHealthSnapshot() {
  console.info('[data-flow-producer] Health check requested')

  const [employees, performances, incentives] = await Promise.all([
    prisma.employee.count(),
    prisma.performance.count(),
    prisma.incentive.count()
  ])

  console.info('[data-flow-producer] Health snapshot retrieved', {
    employees,
    performances,
    incentives
  })

  return {
    ok: true,
    database: 'neon-postgresql',
    counts: {
      employees,
      performances,
      incentives
    }
  }
}