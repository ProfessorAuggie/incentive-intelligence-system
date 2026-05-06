"use client"

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

export default function BarChartRegion({ data }: { data: { region: string; sales: number }[] }) {
  return (
    <div className="card-strong h-[360px]">
      <div className="mb-4 flex items-start justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">Revenue by region</div>
          <h3 className="mt-2 text-lg font-semibold text-slate-950 dark:text-white">Region vs Sales</h3>
        </div>
        <div className="rounded-full border border-slate-200 px-3 py-1 text-xs font-medium text-slate-500 dark:border-slate-700 dark:text-slate-400">
          Enterprise benchmark view
        </div>
      </div>
      <ResponsiveContainer width="100%" height="85%">
        <BarChart data={data} margin={{ top: 6, right: 6, left: -10, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.2)" vertical={false} />
          <XAxis dataKey="region" tickLine={false} axisLine={false} />
          <YAxis tickLine={false} axisLine={false} />
          <Tooltip cursor={{ fill: 'rgba(59,130,246,0.08)' }} />
          <Bar dataKey="sales" fill="#2563eb" radius={[10, 10, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
