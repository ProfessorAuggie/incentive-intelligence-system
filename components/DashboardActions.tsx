"use client"

import { useMemo, useState } from 'react'

type ActionState = 'idle' | 'loading' | 'done' | 'error'

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

  const exportCsv = () => {
    window.location.href = '/api/export'
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
    </div>
  )
}
