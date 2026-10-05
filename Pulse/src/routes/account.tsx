import { useState } from "react";

export default function AccountPage() {
  const [profile, setProfile] = useState<any>({
    kyc_status: "Pending",
    bank_linked: false,
    wallet_address: "",
  });

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto" }}>
      <h1>My Account</h1>
      <p>KYC Status: {profile.kyc_status}</p>
      <p>Bank Linked: {profile.bank_linked ? "Yes" : "No"}</p>
      <p>Wallet Address: {profile.wallet_address || "Not linked"}</p>

      <button onClick={() => alert("Future: KYC provider integration")}>
        Update KYC
      </button>
      <button onClick={() => alert("Future: Bank linkage provider integration")}>
        Link Bank
      </button>
      <button onClick={() => alert("Future: Wallet integration")}>
        Link Wallet
      </button>
    </div>
  );
}
