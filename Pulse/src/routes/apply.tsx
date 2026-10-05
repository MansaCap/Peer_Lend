import { useState } from "react";

export default function ApplyPage() {
  const [borrowerId, setBorrowerId] = useState("");
  const [amount, setAmount] = useState("");
  const [term, setTerm] = useState("");
  const [income, setIncome] = useState("");
  const [creditScore, setCreditScore] = useState("");
  const [result, setResult] = useState<any>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const response = await fetch("http://127.0.0.1:8000/api/v1/scoring", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        borrower_id: Number(borrowerId),
        amount: Number(amount),
        term: Number(term),
        income: Number(income),
        credit_score: Number(creditScore),
      }),
    });
    const data = await response.json();
    setResult(data);
  }

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto" }}>
      <h1>Apply for a Loan</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Borrower ID"
          value={borrowerId}
          onChange={(e) => setBorrowerId(e.target.value)}
        />
        <input
          type="number"
          placeholder="Loan Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
        <input
          type="number"
          placeholder="Term (months)"
          value={term}
          onChange={(e) => setTerm(e.target.value)}
        />
        <input
          type="number"
          placeholder="Monthly Income"
          value={income}
          onChange={(e) => setIncome(e.target.value)}
        />
        <input
          type="number"
          placeholder="Credit Score"
          value={creditScore}
          onChange={(e) => setCreditScore(e.target.value)}
        />
        <button type="submit">Submit</button>
      </form>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h2>Scoring Result</h2>
          <p>Risk Tier: {result.risk_tier}</p>
          <p>Probability of Default: {result.probability_of_default}</p>
          <p>Recommendation: {result.recommendation}</p>
        </div>
      )}
    </div>
  );
}
