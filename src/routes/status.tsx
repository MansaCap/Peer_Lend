import { useState } from "react";

export default function StatusPage() {
  const [loanId, setLoanId] = useState("");
  const [status, setStatus] = useState<any>(null);

  async function fetchStatus() {
    const response = await fetch("http://127.0.0.1:8000/api/v1/payback/schedule", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        loan_id: Number(loanId),
        principal: 5000,
        term: 12,
        interest_rate: 5.0
      }),
    });
    const data = await response.json();
    setStatus(data);
  }

  return (
    <div>
      <h1>Loan Status</h1>
      <input
        type="text"
        placeholder="Enter Loan ID"
        value={loanId}
        onChange={(e) => setLoanId(e.target.value)}
      />
      <button onClick={fetchStatus}>Check Status</button>

      {status && (
        <div>
          <h2>Loan #{status.loan_id}</h2>
          <h3>Repayment Schedule</h3>
          <ul>
            {status.schedule.map((item: any, idx: number) => (
              <li key={idx}>
                {item.due_date} — ${item.amount_due} — {item.status}
              </li>
            ))}
          </ul>
          <p>Next Payment: {status.next_payment?.due_date} (${status.next_payment?.amount_due})</p>
        </div>
      )}
    </div>
  );
}
