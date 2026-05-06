import { calculateAllIncentives } from '../services/incentiveEngine'

async function main() {
  const res = await calculateAllIncentives()
  console.log('Incentives created/updated:', res.length)
}

main().catch((e) => {
  console.error(e)
  process.exit(1)
})
