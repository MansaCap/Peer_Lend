import requests

BASE = "http://127.0.0.1:8001/api/v1"

print("Loans Pending:")
print(requests.get(f"{BASE}/loans", params={"status": "pending"}).json())

print("\nNotifications:")
print(requests.get(f"{BASE}/notifications").json())

print("\nAnalytics:")
print(requests.get(f"{BASE}/analytics").json())

print("\nRepayments for Loan 1:")
print(requests.get(f"{BASE}/repayments", params={"loan_id": 1}).json())

