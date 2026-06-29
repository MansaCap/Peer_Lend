import os
import requests


BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8011")


def print_result(name: str, response: requests.Response) -> None:
    print(f"[{name}] status={response.status_code}")
    try:
        print(response.json())
    except ValueError:
        print(response.text)


def main() -> None:
    # 1) DB health
    health = requests.get(f"{BASE_URL}/health/db", timeout=10)
    print_result("health", health)

    # 2) Create loan
    create_loan = requests.post(
        f"{BASE_URL}/loans/create",
        json={
            "borrower_id": 1,
            "principal": 1000.5,
            "status": "open",
            "collateral_value": 1200.0,
        },
        timeout=10,
    )
    print_result("create_loan", create_loan)

    if create_loan.status_code != 200:
        return

    loan_id = create_loan.json().get("loan_id")
    if not loan_id:
        print("No loan_id returned; skipping repayment test")
        return

    # 3) Add repayment
    add_repayment = requests.post(
        f"{BASE_URL}/repayments/add",
        json={
            "loan_id": loan_id,
            "amount": 50.0,
            "source": "bank_transfer",
        },
        timeout=10,
    )
    print_result("add_repayment", add_repayment)

    # 4) Compliance log
    log_compliance = requests.post(
        f"{BASE_URL}/compliance/log",
        json={"user_id": 1, "action": "smoke_test_log"},
        timeout=10,
    )
    print_result("log_compliance", log_compliance)


if __name__ == "__main__":
    main()
