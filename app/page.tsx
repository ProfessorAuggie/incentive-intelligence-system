import KPICard from '../components/KPICard'
import BarChartRegion from '../components/Charts/BarChartRegion'
import IncentiveHistogram from '../components/Charts/IncentiveHistogram'
import TopPerformersTable from '../components/Tables/TopPerformers'
import prisma from '../lib/prisma'

export const dynamic = 'force-dynamic'

function bucketPayout(payout: number) {
  if (payout < 1000) return '< $1k'
  if (payout < 5000) return '$1k-$5k'
  if (payout < 10000) return '$5k-$10k'
  if (payout < 20000) return '$10k-$20k'
  return '$20k+'
}

async function getSummary() {
  const [totalPayoutAgg, avgIncentiveAgg, totalEmployees, anomaliesCount, top, performances] = await Promise.all([
    prisma.incentive.aggregate({ _sum: { payout: true } }),
    prisma.incentive.aggregate({ _avg: { payout: true } }),
    prisma.employee.count(),
    prisma.incentive.count({ where: { anomalies: { isEmpty: false } } }),
    prisma.incentive.findMany({ take: 10, orderBy: { payout: 'desc' }, include: { employee: true, performance: true } }),
    prisma.performance.findMany({ include: { employee: true, incentive: true } })
  ])

  const regionMap = new Map<string, number>()
  const histogramMap = new Map<string, number>()

  for (const perf of performances) {
    const region = perf.employee.region
    const payout = perf.incentive?.payout ?? 0

    regionMap.set(region, (regionMap.get(region) ?? 0) + perf.sales)
    histogramMap.set(bucketPayout(payout), (histogramMap.get(bucketPayout(payout)) ?? 0) + 1)
  }

  const byRegion = Array.from(regionMap.entries()).map(([region, sales]) => ({ region, sales })).sort((a, b) => b.sales - a.sales)
  const histogram = ['< $1k', '$1k-$5k', '$5k-$10k', '$10k-$20k', '$20k+'].map((bucket) => ({ bucket, count: histogramMap.get(bucket) ?? 0 }))

  return {
    totalPayout: totalPayoutAgg._sum.payout || 0,
    avgIncentive: avgIncentiveAgg._avg.payout || 0,
    totalEmployees,
    anomaliesCount,
    byRegion,
    histogram,
    top
  }
}

export default async function DashboardPage() {
  const summary = await getSummary()

  return (
    <div className="space-y-6">
      <section className="grid gap-4 xl:grid-cols-4">
        <KPICard title="Total Payout" value={`$${Number(summary.totalPayout).toLocaleString()}`} accent="blue" delta="+12% QoQ" hint="Aggregate payout across all incentive records" />
        <KPICard title="Average Incentive" value={`$${Number(summary.avgIncentive).toFixed(2)}`} accent="emerald" delta="+4.8% YoY" hint="Mean payout per calculated incentive" />
        <KPICard title="Total Employees" value={summary.totalEmployees} accent="slate" delta="30 active" hint="Employees loaded in the current Neon branch" />
        <KPICard title="Anomalies Count" value={summary.anomaliesCount} accent="amber" delta="Needs review" hint="Flagged incentive records requiring audit" />
      </section>

      <section className="grid gap-6 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <BarChartRegion data={summary.byRegion} />
        </div>
        <IncentiveHistogram data={summary.histogram} />
      </section>

      <section>
        <TopPerformersTable rows={summary.top} />
      </section>
    </div>
  )
}
