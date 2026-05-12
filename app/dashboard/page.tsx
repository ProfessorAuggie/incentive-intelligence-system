import Sidebar from "@/components/layout/Sidebar";
import PayoutChart from "@/components/dashboard/PayoutChart";

async function getSummary() {
  try {
    const res = await fetch(
      "http://localhost:3000/api/summary",
      {
        cache: "no-store",
      }
    );

    return res.json();
  } catch {
    return null;
  }
}

export default async function DashboardPage() {
  const data = await getSummary();

  return (
    <div className="flex bg-black text-white">
      <Sidebar />

      <main className="flex-1 p-10">
        <h1 className="text-4xl font-bold mb-10">
          Enterprise Incentive Dashboard
        </h1>

        <div className="grid grid-cols-3 gap-6 mb-10">
          <div className="bg-zinc-900 p-6 rounded-2xl">
            <h2 className="text-zinc-400">
              Total Payout
            </h2>

            <p className="text-3xl font-bold mt-2">
              ${data?.totalPayout || 0}
            </p>
          </div>

          <div className="bg-zinc-900 p-6 rounded-2xl">
            <h2 className="text-zinc-400">
              Records
            </h2>

            <p className="text-3xl font-bold mt-2">
              {data?.count || 0}
            </p>
          </div>

          <div className="bg-zinc-900 p-6 rounded-2xl">
            <h2 className="text-zinc-400">
              Anomalies
            </h2>

            <p className="text-3xl font-bold mt-2">
              {data?.anomalies || 0}
            </p>
          </div>
        </div>

        <PayoutChart />
      </main>
    </div>
  );
}
