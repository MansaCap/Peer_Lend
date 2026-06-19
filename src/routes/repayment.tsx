import { useEffect, useState } from "react";

export default function RepaymentsPage() {
  const [loanId, setLoanId] = useState("");
  const [repayments, setRepayments] = useState<any[]>([]);

  async function fetchRepayments() {
    const response = await fetch("http://127.0.0.1:8000/api/v1/payback/schedule", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        loan_id: Number(loanId),
        principal: 5000,
        term: 12,
        interest_rate: 5.0,
      }),
    });
    const data = await response.json();
    setRepayments(data.schedule || []);
  }

  return (
    <div style={{ maxWidth: "700px", margin: "0 auto" }}>
      <h1>Repayment Panel</h1>
      <input
        type="text"
        placeholder="Enter Loan ID"
        value={loanId}
        onChange={(e) => setLoanId(e.target.value)}
      />
      <button onClick={fetchRepayments}>Load Repayments</button>

      {repayments.length > 0 && (
        <div style={{ marginTop: "20px" }}>
          <h2>Schedule</h2>
          <table>
            <thead>
              <tr>
                <th>Due Date</th>
                <th>Amount</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {repayments.map((item, idx) => (
                <tr key={idx}>
                  <td>{item.due_date}</td>
                  <td>${item.amount_due}</td>
                  <td>{item.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
