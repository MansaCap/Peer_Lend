# peer_lending_backend/src/security/plaid_client.py

from plaid import Client
from plaid.api import plaid_api
from plaid.model import (
    ItemPublicTokenExchangeRequest,
    LinkTokenCreateRequest,
    Products,
    CountryCode,
    AccountBalanceGetRequest
)

PLAID_CLIENT_ID = "YOUR_PLAID_CLIENT_ID"
PLAID_SECRET = "YOUR_PLAID_SECRET"
PLAID_ENV = "sandbox"  # or "development" / "production"

configuration = plaid_api.Configuration(
    host=plaid_api.Environment.Sandbox if PLAID_ENV == "sandbox" else plaid_api.Environment.Development,
    api_key={
        "clientId": PLAID_CLIENT_ID,
        "secret": PLAID_SECRET
    }
)

api_client = plaid_api.ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)

def create_link_token(user_id: str):
    request = LinkTokenCreateRequest(
        user={"client_user_id": user_id},
        client_name="Peer Lending",
        products=[Products("auth"), Products("transactions")],
        country_codes=[CountryCode("US")],
        language="en",
        redirect_uri=None
    )
    response = plaid_client.link_token_create(request)
    return response["link_token"]

def exchange_public_token(public_token: str):
    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    response = plaid_client.item_public_token_exchange(request)
    return response["access_token"]

def get_account_balances(access_token: str):
    request = AccountBalanceGetRequest(access_token=access_token)
    response = plaid_client.accounts_balance_get(request)
    return response["accounts"]
