import { Bar, BarChart, CartesianGrid, Line, LineChart, Tooltip, XAxis, YAxis } from "recharts";
import { useEffect, useState } from "react";

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState<any>(null);

  useEffect(() => {
    async function fetchAnalytics() {
      const response = await fetch("http://127.0.0.1:8000/api/v1/analytics");
      const data = await response.json();
      setAnalytics(data);
    }
    fetchAnalytics();
  }, []);

  if (!analytics) {
    return <p>Loading analytics...</p>;
  }

  return (
    <div style={{ maxWidth: "900px", margin: "0 auto" }}>
      <h1>Loan Analytics</h1>

      <h2>Repayment Progress</h2>
      <LineChart width={800} height={300} data={analytics.repayments}>
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="due_date" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="amount_due" stroke="#8884d8" />
      </LineChart>

      <h2>Loan Status Breakdown</h2>
      <BarChart width={800} height={300} data={analytics.loan_status}>
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="status" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="count" fill="#82ca9d" />
      </BarChart>
    </div>
  );
}
