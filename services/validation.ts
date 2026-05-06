import type { Performance } from '@prisma/client'

type EmployeePayload = {
  name: string
  role: string
  region: string
  isManager?: boolean
}

export function validateEmployeePayload(payload: Partial<EmployeePayload>) {
  if (!payload.name || !payload.role || !payload.region) {
    throw new Error('Null values present in employee payload')
  }
  if (payload.name.trim().length === 0 || payload.role.trim().length === 0 || payload.region.trim().length === 0) {
    throw new Error('Empty strings are not allowed in employee payload')
  }
  return true
}

export function validatePerformance(p: Partial<Performance>) {
  if (p.sales == null || p.target == null || p.growth == null || p.employeeId == null || p.quarter == null || p.year == null) {
    throw new Error('Null values present in performance')
  }
  if (p.sales < 0 || p.target < 0 || p.growth < 0 || p.year < 0) {
    throw new Error('Negative values not allowed')
  }
  if (typeof p.quarter === 'string' && p.quarter.trim().length === 0) {
    throw new Error('Quarter cannot be empty')
  }
  return true
}

export function validateCalculationInput(performance: Partial<Performance>, employee: { isManager?: boolean } | null | undefined) {
  validatePerformance(performance)

  if (!employee) {
    throw new Error('Missing employee data for incentive calculation')
  }

  return true
}
