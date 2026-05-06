import type { Performance } from '@prisma/client'

export function validatePerformance(p: Partial<Performance>) {
  if (p.sales == null || p.target == null || p.growth == null) {
    throw new Error('Null values present in performance')
  }
  if (p.sales! < 0 || p.target! < 0) {
    throw new Error('Negative values not allowed')
  }
  return true
}
