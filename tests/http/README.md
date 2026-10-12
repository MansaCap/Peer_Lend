# HTTP API tests

`.http` files for the FastAPI backend: `identity.http`, `collateral.http`, `credit.http`, `loan.http`.

## Running requests

1. Install the **REST Client** extension (`humao.rest-client`) in VS Code.
2. Start the API, e.g. `uvicorn app.main:app --reload --port 8000` from `peer_lending_backend/src`.
3. Open a `.http` file and click **Send Request** above a request (or press `Ctrl+Alt+R`).

Requests are separated by `###`. Variables (`@base_url`, `@borrower_id`, `@loan_id`) are declared at the top of each file; edit them to change test data.

## Local vs production

Each file has local requests using `{{base_url}}` and a final production section that defines `@prod_url` and repeats the requests with `{{prod_url}}`.

- Replace `<railway-app>` in `@prod_url` with your Railway app name.
- To point a request at another environment, swap `{{base_url}}` for `{{prod_url}}`.
- Optional: define environments once in `.vscode/settings.json` and switch with `Ctrl+Alt+E`:

```json
"rest-client.environmentVariables": {
  "$shared": { "borrower_id": "1", "loan_id": "1" },
  "local": { "base_url": "http://localhost:8000" },
  "prod": { "base_url": "https://<railway-app>.up.railway.app" }
}
```

(Remove the in-file `@base_url`/`@prod_url` lines if you use this, since file variables override environments.)

## Adding auth tokens later

Add a token variable at the top of a file and a header to requests:

```http
@token = your-jwt-here

POST {{base_url}}/loan/apply
Content-Type: application/json
Authorization: Bearer {{token}}
```

To capture a token from a login request automatically:

```http
# @name login
POST {{base_url}}/api/auth/login
Content-Type: application/json

{ "email": "test@example.com", "password": "password" }

###
@token = {{login.response.body.token}}
```

Don't commit real tokens; keep them in VS Code settings or an untracked file.
