import prisma from '../../lib/prisma'

type SearchParams = {
  employeeId?: string
}

function formatCurrency(value: number) {
  return `$${Number(value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

export default async function AuditPage({ searchParams }: { searchParams?: SearchParams }) {
  const employees = await prisma.employee.findMany({ orderBy: { name: 'asc' } })
  const selectedEmployeeId = searchParams?.employeeId ?? employees[0]?.id

  const records = selectedEmployeeId
    ? await prisma.incentive.findMany({
        where: { employeeId: selectedEmployeeId },
        include: { employee: true, performance: true },
        orderBy: { createdAt: 'desc' }
      })
    : []

  const selectedEmployee = employees.find((employee) => employee.id === selectedEmployeeId) ?? null
  const selectedRecord = records[0] ?? null

  return (
    <div className="space-y-6">
      <div className="card-strong">
        <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">Audit trail</div>
        <h2 className="mt-2 text-2xl font-semibold tracking-tight text-slate-950 dark:text-white">Employee audit</h2>
        <p className="mt-2 max-w-3xl text-sm text-slate-500 dark:text-slate-400">Inspect the input data, rules, and final payout breakdown for any employee incentive record.</p>
      </div>

      <section className="grid gap-6 xl:grid-cols-[320px,1fr]">
        <div className="card-strong space-y-4">
          <div>
            <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">Select employee</div>
            <select className="input mt-3 w-full" defaultValue={selectedEmployeeId}>
              {employees.map((employee) => (
                <option key={employee.id} value={employee.id}>
                  {employee.name}
                </option>
              ))}
            </select>
          </div>

          {selectedEmployee ? (
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-900/70">
              <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">Employee profile</div>
              <div className="mt-3 text-lg font-semibold text-slate-950 dark:text-white">{selectedEmployee.name}</div>
              <div className="mt-1 text-sm text-slate-600 dark:text-slate-400">{selectedEmployee.role}</div>
              <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
                <div className="rounded-xl bg-white p-3 shadow-sm dark:bg-slate-950">
                  <div className="text-slate-500 dark:text-slate-400">Region</div>
                  <div className="mt-1 font-medium text-slate-900 dark:text-white">{selectedEmployee.region}</div>
                </div>
                <div className="rounded-xl bg-white p-3 shadow-sm dark:bg-slate-950">
                  <div className="text-slate-500 dark:text-slate-400">Manager</div>
                  <div className="mt-1 font-medium text-slate-900 dark:text-white">{selectedEmployee.isManager ? 'Yes' : 'No'}</div>
                </div>
              </div>
            </div>
          ) : null}
        </div>

        <div className="space-y-6">
          {selectedRecord ? (
            <>
              <div className="card-strong grid gap-4 lg:grid-cols-3">
                <div>
                  <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">Input data</div>
                  <pre className="mt-3 overflow-auto rounded-2xl bg-slate-950 p-4 text-xs text-slate-100 shadow-inner">{JSON.stringify({ sales: selectedRecord.performance.sales, target: selectedRecord.performance.target, growth: selectedRecord.performance.growth }, null, 2)}</pre>
                </div>
                <div>
                  <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">Rules applied</div>
                  <div className="mt-3 space-y-2 text-sm text-slate-700 dark:text-slate-300">
                    <div className="rounded-xl border border-slate-200 bg-white p-3 dark:border-slate-800 dark:bg-slate-950">sales &gt;= target → 10%</div>
                    <div className="rounded-xl border border-slate-200 bg-white p-3 dark:border-slate-800 dark:bg-slate-950">sales &gt;= 150% target → 20%</div>
                    <div className="rounded-xl border border-slate-200 bg-white p-3 dark:border-slate-800 dark:bg-slate-950">growth &gt; 20% → +5% bonus</div>
                    <div className="rounded-xl border border-slate-200 bg-white p-3 dark:border-slate-800 dark:bg-slate-950">manager override → +3% bonus</div>
                  </div>
                </div>
                <div>
                  <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">Final payout</div>
                  <div className="mt-3 rounded-2xl bg-gradient-to-br from-blue-500 to-slate-900 p-5 text-white shadow-lg">
                    <div className="text-sm opacity-80">Calculated incentive</div>
                    <div className="mt-2 text-3xl font-semibold">{formatCurrency(selectedRecord.payout)}</div>
                    <div className="mt-3 text-sm opacity-80">Performance period: {selectedRecord.performance.quarter} {selectedRecord.performance.year}</div>
                  </div>
                </div>
              </div>

              <div className="card-strong overflow-hidden">
                <div className="mb-4 flex items-center justify-between gap-3">
                  <div>
                    <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">History</div>
                    <h3 className="mt-2 text-lg font-semibold text-slate-950 dark:text-white">Audit records</h3>
                  </div>
                  <div className="rounded-full border border-slate-200 px-3 py-1 text-xs font-medium text-slate-500 dark:border-slate-700 dark:text-slate-400">{records.length} records</div>
                </div>

                <div className="overflow-auto">
                  <table className="w-full text-left text-sm">
                    <thead className="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">
                      <tr>
                        <th className="pb-3 pr-4">Quarter</th>
                        <th className="pb-3 pr-4">Sales</th>
                        <th className="pb-3 pr-4">Target</th>
                        <th className="pb-3 pr-4">Growth</th>
                        <th className="pb-3 pr-4 text-right">Payout</th>
                      </tr>
                    </thead>
                    <tbody>
                      {records.map((record) => (
                        <tr key={record.id} className="border-t border-slate-100 dark:border-slate-800">
                          <td className="py-4 pr-4 font-medium text-slate-900 dark:text-white">{record.performance.quarter} {record.performance.year}</td>
                          <td className="py-4 pr-4">{formatCurrency(record.performance.sales)}</td>
                          <td className="py-4 pr-4">{formatCurrency(record.performance.target)}</td>
                          <td className="py-4 pr-4">{Number(record.performance.growth).toFixed(1)}%</td>
                          <td className="py-4 pr-4 text-right font-semibold text-slate-900 dark:text-white">{formatCurrency(record.payout)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          ) : (
            <div className="card-strong text-sm text-slate-500 dark:text-slate-400">No audit records available yet.</div>
          )}
        </div>
      </section>
    </div>
  )
}
