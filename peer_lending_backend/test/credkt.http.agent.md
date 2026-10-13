

### Local Environment
@base_url = http://localhost:8000

### Production Environment
@prod_url = https://your-public-url.up.railway.app


### Compute Credit Score
POST {{base_url}}/credit/score
Content-Type: application/json

{
  "borrower_id": 1
}

### Retrieve Credit Score
GET {{base_url}}/credit/retrieve/1
