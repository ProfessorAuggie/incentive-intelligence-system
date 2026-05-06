import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()

async function main() {
  const regions = ['North', 'South', 'East', 'West']
  const roles = ['Sales Rep', 'Senior Rep', 'Manager']

  for (let i = 1; i <= 30; i++) {
    const isManager = i % 10 === 0
    const emp = await prisma.employee.create({ data: { name: `Employee ${i}`, role: roles[i % roles.length], region: regions[i % regions.length], isManager } })
    for (const q of ['Q1', 'Q2', 'Q3', 'Q4']) {
      await prisma.performance.create({ data: { employeeId: emp.id, quarter: q, year: 2025, sales: Math.round(Math.random() * 200000), target: Math.round(30000 + Math.random() * 100000), growth: Math.round(Math.random() * 120) } })
    }
  }
}

main()
  .catch((e) => console.error(e))
  .finally(() => prisma.$disconnect())
