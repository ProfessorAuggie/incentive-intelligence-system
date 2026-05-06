"use client"

import Link from 'next/link'
import ThemeToggle from './ThemeToggle'
import DashboardActions from './DashboardActions'

export default function Navbar() {
  return (
    <div className="sticky top-0 z-20 border-b border-slate-200/80 bg-white/75 px-4 py-4 backdrop-blur dark:border-slate-800/80 dark:bg-slate-950/70 sm:px-6 lg:px-8">
      <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.24em] text-blue-600 dark:text-blue-400">
            <span className="h-2 w-2 rounded-full bg-blue-500" />
            Financial Incentive Intelligence
          </div>
          <div className="flex flex-wrap items-end gap-3">
            <h1 className="text-2xl font-semibold tracking-tight text-slate-950 dark:text-white">Enterprise Incentive Intelligence System</h1>
            <Link href="/" className="rounded-full border border-slate-200 px-3 py-1 text-xs font-medium text-slate-500 dark:border-slate-700 dark:text-slate-300">
              Live operations dashboard
            </Link>
          </div>
          <p className="max-w-3xl text-sm text-slate-500 dark:text-slate-400">
            Monitor payout performance, identify anomalies, and audit every calculation with a transparent enterprise workflow.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <DashboardActions />
          <ThemeToggle />
        </div>
      </div>
    </div>
  )
}
