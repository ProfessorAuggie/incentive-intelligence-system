import prisma from '../../lib/prisma'

export const dynamic = 'force-dynamic'

type SearchParams = {
  region?: string
  role?: string
  quarter?: string
}

async function buildFilters(searchParams: SearchParams) {
  const where: any = {}

  if (searchParams.region) where.employee = { ...(where.employee ?? {}), region: searchParams.region }
  if (searchParams.role) where.employee = { ...(where.employee ?? {}), role: searchParams.role }
  if (searchParams.quarter) where.quarter = searchParams.quarter

  return where
}

export default async function IncentivesPage({ searchParams }: { searchParams?: SearchParams }) {
  const where = await buildFilters(searchParams ?? {})

  const [performances, employees, regionBreakdown] = await Promise.all([
    prisma.performance.findMany({ where, include: { employee: true, incentive: true }, orderBy: [{ quarter: 'asc' }, { sales: 'desc' }] }),
    prisma.employee.findMany({ orderBy: { name: 'asc' } }),
    prisma.performance.groupBy({ by: ['quarter'], _sum: { sales: true } })
  ])

  const roles = Array.from(new Set(employees.map((employee) => employee.role))).sort()
  const regions = Array.from(new Set(employees.map((employee) => employee.region))).sort()

  return (
    <div className="space-y-6">
      <div className="card-strong">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">Analytics</div>
            <h2 className="mt-2 text-2xl font-semibold tracking-tight text-slate-950 dark:text-white">Incentive Analytics</h2>
            <p className="mt-2 max-w-3xl text-sm text-slate-500 dark:text-slate-400">Filter by region, role, and quarter to review employee incentive performance and payout behavior.</p>
          </div>
          <div className="grid gap-3 sm:grid-cols-3">
            <select className="input" defaultValue={searchParams?.region ?? ''}>
              <option value="">All regions</option>
              {regions.map((region) => <option key={region} value={region}>{region}</option>)}
            </select>
            <select className="input" defaultValue={searchParams?.role ?? ''}>
              <option value="">All roles</option>
              {roles.map((role) => <option key={role} value={role}>{role}</option>)}
            </select>
            <select className="input" defaultValue={searchParams?.quarter ?? ''}>
              <option value="">All quarters</option>
              {['Q1', 'Q2', 'Q3', 'Q4'].map((quarter) => <option key={quarter} value={quarter}>{quarter}</option>)}
            </select>
          </div>
        </div>
      </div>

      <section className="grid gap-6 xl:grid-cols-3">
        <div className="card-strong xl:col-span-1">
          <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">Region-wise breakdown</div>
          <div className="mt-4 space-y-4">
            {regionBreakdown.map((item) => (
              <div key={item.quarter}>
                <div className="mb-1 flex items-center justify-between text-sm text-slate-600 dark:text-slate-300">
                  <span>{item.quarter}</span>
                  <span>${Number(item._sum.sales ?? 0).toLocaleString()}</span>
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
                  <div className="h-full rounded-full bg-gradient-to-r from-blue-500 to-slate-900" style={{ width: `${Math.min(100, (Number(item._sum.sales ?? 0) / 250000) * 100)}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="card-strong xl:col-span-2">
          <div className="mb-4 flex items-center justify-between gap-3">
            <div>
              <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">Employee breakdown</div>
              <h3 className="mt-2 text-lg font-semibold text-slate-950 dark:text-white">Employee-level incentive table</h3>
            </div>
            <div className="rounded-full border border-slate-200 px-3 py-1 text-xs font-medium text-slate-500 dark:border-slate-700 dark:text-slate-400">Filtered results: {performances.length}</div>
          </div>

          <div className="overflow-auto">
            <table className="w-full text-left text-sm">
              <thead className="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">
                <tr>
                  <th className="pb-3 pr-4">Employee</th>
                  <th className="pb-3 pr-4">Region</th>
                  <th className="pb-3 pr-4">Role</th>
                  <th className="pb-3 pr-4">Quarter</th>
                  <th className="pb-3 pr-4 text-right">Sales</th>
                  <th className="pb-3 pr-4 text-right">Target</th>
                  <th className="pb-3 pr-4 text-right">Payout</th>
                </tr>
              </thead>
              <tbody>
                {performances.map((row) => (
                  <tr key={row.id} className="border-t border-slate-100 dark:border-slate-800">
                    <td className="py-4 pr-4 font-medium text-slate-900 dark:text-white">{row.employee.name}</td>
                    <td className="py-4 pr-4 text-slate-600 dark:text-slate-300">{row.employee.region}</td>
                    <td className="py-4 pr-4 text-slate-600 dark:text-slate-300">{row.employee.role}</td>
                    <td className="py-4 pr-4 text-slate-600 dark:text-slate-300">{row.quarter}</td>
                    <td className="py-4 pr-4 text-right">${Number(row.sales).toLocaleString()}</td>
                    <td className="py-4 pr-4 text-right">${Number(row.target).toLocaleString()}</td>
                    <td className="py-4 pr-4 text-right font-semibold text-slate-900 dark:text-white">${Number(row.incentive?.payout ?? 0).toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  )
}
