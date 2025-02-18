# API Documentation

## Authentication

All API endpoints require authentication using JWT (JSON Web Tokens). Include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

## Endpoints

### Accounts

#### GET /api/accounts/
Lists all accounts for the authenticated user.

**Response**
```json
[
    {
        "id": 1,
        "name": "Cash",
        "amount": "1000.00",
        "currency": {
            "id": 1,
            "name": "USD",
            "icon": "💵"
        },
        "icon": "💰",
        "created_date": "2025-02-17T22:46:39-05:00",
        "updated_date": "2025-02-17T22:46:39-05:00"
    }
]
```

#### POST /api/accounts/
Create a new account.

**Request Body**
```json
{
    "name": "Savings",
    "amount": "5000.00",
    "currency_id": 1,
    "icon": "🏦"
}
```

### Categories

#### GET /api/categories/
Lists all categories.

**Response**
```json
[
    {
        "id": 1,
        "name": "Food",
        "icon": "🍔",
        "category_type": "expense"
    }
]
```

### History Records

#### GET /api/history/
Lists all history records for the authenticated user.

**Query Parameters**
- `start_date`: Filter records after this date (YYYY-MM-DD)
- `end_date`: Filter records before this date (YYYY-MM-DD)
- `category`: Filter by category ID
- `account`: Filter by account ID

**Response**
```json
[
    {
        "id": 1,
        "account": {
            "id": 1,
            "name": "Cash"
        },
        "time_of_occurrence": "2025-02-17T22:46:39-05:00",
        "category": {
            "id": 1,
            "name": "Food"
        },
        "amount": "25.00",
        "comment": "Lunch"
    }
]
```

## Error Responses

All endpoints may return the following error responses:

- 400 Bad Request: Invalid input data
- 401 Unauthorized: Missing or invalid authentication
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Requested resource not found
- 500 Internal Server Error: Server-side error

Error responses follow this format:
```json
{
    "error": "Error message",
    "code": "ERROR_CODE"
}
```
