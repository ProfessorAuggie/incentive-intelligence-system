async function getAnomalies() {
  const res = await fetch(
    "http://localhost:3000/api/anomalies",
    {
      cache: "no-store",
    }
  );

  return res.json();
}

export default async function AnomaliesPage() {
  const anomalies = await getAnomalies();

  return (
    <main className="min-h-screen bg-black text-white p-10">
      <h1 className="text-4xl font-bold mb-8">
        Anomaly Detection
      </h1>

      <div className="space-y-4">
        {anomalies.map((item: any) => (
          <div
            key={item.id}
            className="bg-red-900/30 border border-red-500 p-5 rounded-xl"
          >
            <h2 className="font-bold text-xl">
              {item.employee.name}
            </h2>

            <p>
              Final Payout: $
              {item.finalPayout}
            </p>

            <p>
              Reason:
              {" "}
              {item.anomalyReason}
            </p>
          </div>
        ))}
      </div>
    </main>
  );
}
