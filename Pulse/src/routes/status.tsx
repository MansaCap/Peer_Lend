import { useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8001/api/v1";

export default function StatusPage() {
  const [loanId, setLoanId] = useState("");
  const [status, setStatus] = useState<any>(null);

  async function fetchStatus() {
    const query = loanId ? `?loan_id=${encodeURIComponent(loanId)}` : "";
    const response = await fetch(`${API_BASE_URL}/repayments${query}`);
    const data = await response.json();
    setStatus({
      loan_id: Number(loanId),
      schedule: data || [],
      next_payment: data?.[0] || null,
    });
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
