import prisma from '../lib/prisma'

async function main() {
  const employees = await prisma.employee.count()
  const performances = await prisma.performance.count()
  const incentives = await prisma.incentive.count()
  console.log({ employees, performances, incentives })
}

main().catch((e) => { console.error(e); process.exit(1) })
