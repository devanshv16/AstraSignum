"use client";

import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function TimelineChart({
  data,
}: {
  data: Array<{ year: string; mentions: number }>;
}) {
  return (
    <div style={{ width: "100%", height: 320 }}>
      <ResponsiveContainer>
        <LineChart data={data}>
          <XAxis dataKey="year" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="mentions" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}