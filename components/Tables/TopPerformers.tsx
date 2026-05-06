export default function TopPerformersTable({ rows }: { rows: any[] }) {
  return (
    <div className="card-strong overflow-hidden">
      <div className="mb-4 flex items-start justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">Leaderboard</div>
          <h3 className="mt-2 text-lg font-semibold text-slate-950 dark:text-white">Top 10 performers</h3>
        </div>
        <div className="rounded-full border border-slate-200 px-3 py-1 text-xs font-medium text-slate-500 dark:border-slate-700 dark:text-slate-400">
          Ranked by payout
        </div>
      </div>

      <div className="overflow-auto">
        <table className="w-full text-left text-sm">
          <thead className="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">
            <tr>
              <th className="pb-3 pr-4">Rank</th>
              <th className="pb-3 pr-4">Employee</th>
              <th className="pb-3 pr-4">Region</th>
              <th className="pb-3 pr-4 text-right">Payout</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row, index) => (
              <tr key={row.id} className="border-t border-slate-100 dark:border-slate-800">
                <td className="py-4 pr-4 text-slate-500 dark:text-slate-400">#{index + 1}</td>
                <td className="py-4 pr-4 font-medium text-slate-900 dark:text-white">{row.employee.name}</td>
                <td className="py-4 pr-4 text-slate-600 dark:text-slate-300">{row.employee.region}</td>
                <td className="py-4 pr-4 text-right font-semibold text-slate-900 dark:text-white">${Number(row.payout).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
