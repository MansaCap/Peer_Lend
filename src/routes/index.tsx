export default function IndexPage() {
  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Welcome to Ancla</h1>
      <p>Your peer-to-peer lending platform.</p>
      <nav>
        <a href="/apply">Apply for a Loan</a> |{" "}
        <a href="/account">My Account</a> |{" "}
        <a href="/status">Loan Status</a> |{" "}
        <a href="/notifications">Notifications</a>
      </nav>
    </div>
  );
}
