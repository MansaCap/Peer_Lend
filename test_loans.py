import requests
import os

base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8011")
url = f"{base_url}/loans/create"
payload = {
    "borrower_id": 1,
    "principal": 1000.5,
    "status": "open"
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
try:
    print("Response:", response.json())
except ValueError:
    print("Response:", response.text)
