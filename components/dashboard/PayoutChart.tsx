"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { region: "US", payout: 42000 },
  { region: "EMEA", payout: 32000 },
  { region: "APAC", payout: 28000 },
];

export default function PayoutChart() {
  return (
    <div className="bg-zinc-900 rounded-2xl p-6">
      <h2 className="text-xl font-bold mb-6">
        Region Payouts
      </h2>

      <div className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <XAxis dataKey="region" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="payout" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
