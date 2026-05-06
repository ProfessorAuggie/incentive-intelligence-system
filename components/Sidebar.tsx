import Link from 'next/link'
import { BarChart3, TrendingUp, AlertTriangle, FileText } from 'lucide-react'

const nav = [
  { href: '/', label: 'Dashboard', icon: BarChart3 },
  { href: '/incentives', label: 'Incentive Analytics', icon: TrendingUp },
  { href: '/anomalies', label: 'Anomaly Detection', icon: AlertTriangle },
  { href: '/audit', label: 'Audit', icon: FileText }
]

export default function Sidebar() {
  return (
    <aside className="hidden w-72 shrink-0 border-r border-slate-200/70 bg-white/70 px-5 py-6 backdrop-blur dark:border-slate-800/80 dark:bg-slate-950/60 lg:flex lg:flex-col">
      <div className="rounded-3xl border border-slate-200/80 bg-[linear-gradient(180deg,rgba(59,130,246,0.12),rgba(15,23,42,0.02))] p-5 shadow-sm dark:border-slate-800 dark:bg-[linear-gradient(180deg,rgba(59,130,246,0.18),rgba(15,23,42,0.08))]">
        <div className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-500 dark:text-slate-400">EIIS</div>
        <div className="mt-3 text-2xl font-semibold tracking-tight text-slate-950 dark:text-white">Incentive Operations</div>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">Enterprise payout controls, auditability, and anomaly monitoring in one place.</p>
      </div>

      <nav className="mt-6 flex flex-1 flex-col gap-2">
        {nav.map((item) => {
          const Icon = item.icon
          return (
            <Link key={item.href} href={item.href} className="group flex items-center gap-3 rounded-2xl border border-transparent px-3 py-3 text-sm font-medium text-slate-700 transition hover:border-slate-200 hover:bg-white hover:shadow-sm dark:text-slate-300 dark:hover:border-slate-700 dark:hover:bg-slate-900">
              <Icon size={20} className="shrink-0" />
              <span>{item.label}</span>
              <span className="ml-auto text-slate-400 transition group-hover:translate-x-0.5">›</span>
            </Link>
          )
        })}
      </nav>

      <div className="rounded-2xl border border-slate-200/80 bg-slate-50 p-4 text-sm text-slate-600 dark:border-slate-800 dark:bg-slate-900/70 dark:text-slate-400">
        <div className="font-medium text-slate-900 dark:text-white">Operational checklist</div>
        <ul className="mt-3 space-y-2">
          <li>• Sync Neon data</li>
          <li>• Recalculate incentives</li>
          <li>• Scan anomalies</li>
        </ul>
      </div>
    </aside>
  )
}
