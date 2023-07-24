Mastercard take-home task repo

API docs are also available via Swagger at `http://host:port/docs`

<h3>List all accounts</h3>
  
GET `/api/accounts`

Response 200

```json
{
    "account_id": { // uuid
        "name": "Karim", // str
        "email": "karim@gmail.com", // str
        "balance": 100.0, // float
        "active": true, // bool
        "description": "hello" // str
    },
    ...
}
```

<h3>Create account</h3>

POST `/api/accounts`

Payload
```json
{
    "name": "Karim",
    "email": "karimnassar2012@gmail.com",
    "balance": 100,
    "active": false,
    "description": "Hello"
}
```

Response 201
```json
{
    "result": {
        "id": "633d1902-09ec-4ef0-9826-b4f04f210ca4",
        "name": "Karim",
        "email": "karimnassar2012@gmail.com",
        "balance": 100.0,
        "active": false,
        "description": "Hello"
    }
}
```


<h3>Healthcheck</h3>

GET `/api/health`

Response 200
```json
{
    "message": "Server is running"
}
```

<h3>Delete account</h3>

DELETE `/api/accounts/{account_id}`

Response 200 - empty json


<h3>Get account by ID</h3>

GET `/api/accounts/{account_id}`

Response 200 
```json
{
    "result": {
        "id": "dcb2859d-6882-4672-ba15-1401eba391fd",
        "name": "Karim",
        "email": "asd@gmail.com",
        "balance": 100.0,
        "active": false,
        "description": "LOL"
    }
}
```
