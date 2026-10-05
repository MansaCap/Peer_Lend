import { useEffect, useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8001/api/v1";

export default function RepaymentsPage() {
  const [loanId, setLoanId] = useState("");
  const [repayments, setRepayments] = useState<any[]>([]);

  async function fetchRepayments() {
    const query = loanId ? `?loan_id=${encodeURIComponent(loanId)}` : "";
    const response = await fetch(`${API_BASE_URL}/repayments${query}`);
    const data = await response.json();
    setRepayments(data || []);
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
