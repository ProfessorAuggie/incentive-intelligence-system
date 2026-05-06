"use client"

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

export default function IncentiveHistogram({ data }: { data: { bucket: string; count: number }[] }) {
  return (
    <div className="card-strong h-[360px]">
      <div className="mb-4">
        <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">Payout distribution</div>
        <h3 className="mt-2 text-lg font-semibold text-slate-950 dark:text-white">Incentive distribution</h3>
      </div>
      <ResponsiveContainer width="100%" height="85%">
        <BarChart data={data} margin={{ top: 6, right: 6, left: -10, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.2)" vertical={false} />
          <XAxis dataKey="bucket" tickLine={false} axisLine={false} />
          <YAxis tickLine={false} axisLine={false} allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" fill="#0f172a" radius={[10, 10, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
