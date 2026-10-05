import { useEffect, useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8001/api/v1";

export default function LenderPage() {
  const [loans, setLoans] = useState<any[]>([]);

  useEffect(() => {
    async function fetchLoans() {
      const response = await fetch(`${API_BASE_URL}/loans?status=pending`);
      const data = await response.json();
      setLoans(data || []);
    }
    fetchLoans();
  }, []);

  async function approveLoan(id: number) {
    await fetch(`${API_BASE_URL}/loans/${id}/approve`, { method: "POST" });
    setLoans(loans.filter((loan) => loan.id !== id));
  }

  async function denyLoan(id: number) {
    await fetch(`${API_BASE_URL}/loans/${id}/deny`, { method: "POST" });
    setLoans(loans.filter((loan) => loan.id !== id));
  }

  return (
    <div style={{ maxWidth: "700px", margin: "0 auto" }}>
      <h1>Lender Loan Panel</h1>
      {loans.length === 0 ? (
        <p>No pending loan requests.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Borrower</th>
              <th>Amount</th>
              <th>Term</th>
              <th>Interest</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loans.map((loan) => (
              <tr key={loan.id}>
                <td>{loan.borrower_id}</td>
                <td>${loan.principal}</td>
                <td>{loan.term} months</td>
                <td>{loan.interest_rate}%</td>
                <td>
                  <button onClick={() => approveLoan(loan.id)}>Approve</button>
                  <button onClick={() => denyLoan(loan.id)}>Deny</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
