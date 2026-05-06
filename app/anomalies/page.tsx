import prisma from '../../lib/prisma'

export default async function AnomaliesPage() {
  const anomalies = await prisma.incentive.findMany({
    where: { anomalies: { isEmpty: false } },
    include: { performance: true, employee: true },
    orderBy: { createdAt: 'desc' }
  })

  return (
    <div className="space-y-6">
      <div className="card-strong border-amber-200/70 bg-gradient-to-r from-amber-50 to-white dark:border-amber-900/40 dark:from-amber-950/40 dark:to-slate-900">
        <div className="text-xs font-semibold uppercase tracking-[0.22em] text-amber-700 dark:text-amber-300">Risk monitoring</div>
        <h2 className="mt-2 text-2xl font-semibold tracking-tight text-slate-950 dark:text-white">Anomaly Detection</h2>
        <p className="mt-2 max-w-3xl text-sm text-slate-600 dark:text-slate-400">Flagged payouts are highlighted for review when payout patterns do not align with expected sales or growth behavior.</p>
      </div>

      <div className="card-strong overflow-hidden">
        <div className="mb-4 flex items-center justify-between gap-3">
          <div>
            <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">Exceptions</div>
            <h3 className="mt-2 text-lg font-semibold text-slate-950 dark:text-white">Flagged anomalies</h3>
          </div>
          <div className="rounded-full border border-slate-200 px-3 py-1 text-xs font-medium text-slate-500 dark:border-slate-700 dark:text-slate-400">{anomalies.length} records</div>
        </div>

        <div className="overflow-auto">
          <table className="w-full text-left text-sm">
            <thead className="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">
              <tr>
                <th className="pb-3 pr-4">Employee</th>
                <th className="pb-3 pr-4">Reason</th>
                <th className="pb-3 pr-4">Sales</th>
                <th className="pb-3 pr-4">Target</th>
                <th className="pb-3 pr-4 text-right">Payout</th>
              </tr>
            </thead>
            <tbody>
              {anomalies.map((item) => {
                const severity = item.anomalies.some((reason) => reason.toLowerCase().includes('zero')) ? 'bg-red-50 dark:bg-red-950/30' : 'bg-amber-50 dark:bg-amber-950/30'

                return (
                  <tr key={item.id} className={`border-t border-slate-100 dark:border-slate-800 ${severity}`}>
                    <td className="py-4 pr-4 font-medium text-slate-900 dark:text-white">{item.employee.name}</td>
                    <td className="py-4 pr-4 text-slate-700 dark:text-slate-300">
                      <div className="flex flex-wrap gap-2">
                        {item.anomalies.map((reason) => (
                          <span key={reason} className="rounded-full bg-white px-3 py-1 text-xs font-medium text-slate-700 shadow-sm dark:bg-slate-900 dark:text-slate-200">
                            {reason}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="py-4 pr-4 text-slate-700 dark:text-slate-300">${Number(item.performance.sales).toLocaleString()}</td>
                    <td className="py-4 pr-4 text-slate-700 dark:text-slate-300">${Number(item.performance.target).toLocaleString()}</td>
                    <td className="py-4 pr-4 text-right font-semibold text-slate-900 dark:text-white">${Number(item.payout).toFixed(2)}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
