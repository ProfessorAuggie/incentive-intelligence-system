import { calculateAllIncentives } from '../services/incentiveEngine'

async function main() {
  const res = await calculateAllIncentives()
  console.log('Incentives processed:', res.processedCount)
  console.log('Incentives upserted:', res.upsertedCount)
  console.log('Incentives failed:', res.failedCount)
}

main().catch((e) => {
  console.error(e)
  process.exit(1)
})
