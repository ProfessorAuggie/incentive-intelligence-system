"use client"

import { useMemo, useState } from 'react'

type ActionState = 'idle' | 'loading' | 'done' | 'error'

type HealthResponse = {
  ok: boolean
  database: string
  counts: {
    employees: number
    performances: number
    incentives: number
  }
}

type ResetResponse = {
  ok: boolean
  deleted: {
    employees: number
    performances: number
    incentives: number
  }
  seeded: {
    employeesInserted: number
    performancesInserted: number
  }
}

async function runAction(endpoint: string) {
  const response = await fetch(endpoint, { method: 'POST' })
  if (!response.ok) {
    throw new Error(await response.text())
  }
  return response.json()
}

export default function DashboardActions() {
  const [seedState, setSeedState] = useState<ActionState>('idle')
  const [calcState, setCalcState] = useState<ActionState>('idle')
  const [resetState, setResetState] = useState<ActionState>('idle')
  const [healthState, setHealthState] = useState<ActionState>('idle')
  const [healthSnapshot, setHealthSnapshot] = useState<HealthResponse['counts'] | null>(null)

  const seedLabel = useMemo(() => {
    if (seedState === 'loading') return 'Seeding...'
    if (seedState === 'done') return 'Seeded'
    if (seedState === 'error') return 'Seed failed'
    return 'Seed dummy data'
  }, [seedState])

  const calcLabel = useMemo(() => {
    if (calcState === 'loading') return 'Calculating...'
    if (calcState === 'done') return 'Calculated'
    if (calcState === 'error') return 'Recalculate failed'
    return 'Recalculate incentives'
  }, [calcState])

  const resetLabel = useMemo(() => {
    if (resetState === 'loading') return 'Resetting...'
    if (resetState === 'done') return 'Reset complete'
    if (resetState === 'error') return 'Reset failed'
    return 'Reset shared data'
  }, [resetState])

  const healthLabel = useMemo(() => {
    if (healthState === 'loading') return 'Checking...'
    if (healthState === 'done') return 'Healthy'
    if (healthState === 'error') return 'Health failed'
    return 'Health check'
  }, [healthState])

  const exportCsv = () => {
    window.location.href = '/api/export'
  }

  const checkHealth = async () => {
    try {
      setHealthState('loading')
      const response = await fetch('/api/health', { method: 'GET' })
      if (!response.ok) {
        throw new Error(await response.text())
      }

      const data = (await response.json()) as HealthResponse
      setHealthSnapshot(data.counts)
      setHealthState('done')
    } catch {
      setHealthState('error')
    }
  }

  const resetSharedData = async () => {
    const confirmed = window.confirm('This will clear and reseed the shared database. Continue?')
    if (!confirmed) return

    try {
      setResetState('loading')
      const response = await fetch('/api/reset-data', { method: 'POST' })
      if (!response.ok) {
        throw new Error(await response.text())
      }

      const data = (await response.json()) as ResetResponse
      setHealthSnapshot({
        employees: data.seeded.employeesInserted,
        performances: data.seeded.performancesInserted,
        incentives: 0
      })
      setResetState('done')
    } catch {
      setResetState('error')
    }
  }

  return (
    <div className="flex flex-wrap items-center gap-2">
      <button
        className="button-secondary"
        onClick={async () => {
          try {
            setSeedState('loading')
            await runAction('/api/generate-data')
            setSeedState('done')
          } catch {
            setSeedState('error')
          }
        }}
      >
        {seedLabel}
      </button>
      <button
        className="button-primary"
        onClick={async () => {
          try {
            setCalcState('loading')
            await runAction('/api/calculate-incentives')
            setCalcState('done')
          } catch {
            setCalcState('error')
          }
        }}
      >
        {calcLabel}
      </button>
      <button className="button-secondary" onClick={exportCsv}>
        Export CSV
      </button>
      <button className="button-secondary" onClick={checkHealth}>
        {healthLabel}
      </button>
      <button className="button-secondary" onClick={resetSharedData}>
        {resetLabel}
      </button>
      {healthSnapshot ? (
        <div className="hidden rounded-full border border-slate-200 bg-white px-3 py-2 text-xs font-medium text-slate-600 shadow-sm dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 md:flex md:items-center md:gap-2">
          <span>DB</span>
          <span className="text-slate-900 dark:text-white">{healthSnapshot.employees} employees</span>
          <span className="text-slate-400">•</span>
          <span className="text-slate-900 dark:text-white">{healthSnapshot.performances} performances</span>
          <span className="text-slate-400">•</span>
          <span className="text-slate-900 dark:text-white">{healthSnapshot.incentives} incentives</span>
        </div>
      ) : null}
    </div>
  )
}
