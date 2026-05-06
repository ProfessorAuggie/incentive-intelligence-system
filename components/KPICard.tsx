type Props = {
  title: string
  value: string | number
  accent?: string
  delta?: string
  hint?: string
}

export default function KPICard({ title, value, accent = 'blue', delta, hint }: Props) {
  const accents: Record<string, string> = {
    blue: 'from-blue-500/15 to-blue-500/0 text-blue-600 dark:text-blue-300',
    slate: 'from-slate-500/15 to-slate-500/0 text-slate-700 dark:text-slate-200',
    amber: 'from-amber-500/15 to-amber-500/0 text-amber-600 dark:text-amber-300',
    emerald: 'from-emerald-500/15 to-emerald-500/0 text-emerald-600 dark:text-emerald-300'
  }

  return (
    <div className="card-strong overflow-hidden">
      <div className={`-mx-6 -mt-6 mb-5 h-1 bg-gradient-to-r ${accents[accent] || accents.blue}`} />
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500 dark:text-slate-400">{title}</div>
          <div className="mt-3 text-3xl font-semibold tracking-tight text-slate-950 dark:text-white">{value}</div>
        </div>
        {delta ? <div className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-600 dark:text-emerald-300">{delta}</div> : null}
      </div>
      {hint ? <div className="mt-3 text-sm text-slate-500 dark:text-slate-400">{hint}</div> : null}
    </div>
  )
}
