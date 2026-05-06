import prisma from '../../../lib/prisma'

function csvEscape(value: string | number | null | undefined) {
  const text = value == null ? '' : String(value)
  return `"${text.replaceAll('"', '""')}"`
}

export async function GET() {
  const incentives = await prisma.incentive.findMany({ include: { employee: true, performance: true }, orderBy: { createdAt: 'desc' } })

  const header = ['employee', 'region', 'role', 'quarter', 'sales', 'target', 'growth', 'payout']
  const rows = incentives.map((item: (typeof incentives)[number]) => [
    item.employee.name,
    item.employee.region,
    item.employee.role,
    `${item.performance.quarter} ${item.performance.year}`,
    item.performance.sales,
    item.performance.target,
    item.performance.growth,
    item.payout
  ])

  const csv = [header, ...rows].map((row) => row.map(csvEscape).join(',')).join('\n')

  return new Response(csv, {
    headers: {
      'Content-Type': 'text/csv; charset=utf-8',
      'Content-Disposition': 'attachment; filename="eiis-export.csv"'
    }
  })
}
