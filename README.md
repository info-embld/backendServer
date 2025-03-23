# API Documentation

## Overview
This API is built using Flask with programming language Python with SQL database. 
The API is intended to store user data and licenses, authenticate the user, pay using stripe and send emails for confirmation or newsletter. 

## Table of Contents
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
    - [Create Resource](#create-resource)
    - [Retrieve Resource](#retrieve-resource)
    - [Update Resource](#update-resource)
    - [Delete Resource](#delete-resource)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [FAQ](#faq)
- [Support](#support)

## Getting Started
To start using the API, you need to have an API key.

## Authentication
All API requests must include the API key in the header:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Create Resource
**Endpoint:** `POST /signup`

**Request:**
```json
{
    "first_name": "example",
    "last_name": "example",
    "email": "example@domain.com",
    "password": "password"
}
```

**Response:**
```json
{
    "id": "resource_id",
    "first_name": "example",
    "last_name": "example",
    "email": "example@domain.com",
    "created_at": "timestamp",
    "password_hash": "password hash",
    "subbed": "true/false",
    "is_active": "true/false",
    "newsletter_sub": "true/false",
    "address": "address",
    "licenses": [
        {
            "id": "resource_id",
            "license_key": "license key",
            "user_id": "user id",
            "created_at": "timestamp",
            "expires_at": "timestamp",
            "is_active": "true/false",
            "paid": "true/false"
        }
    ]
}
```
### Login
**Endpoint:** `POST /login`

**Request:**
```json
{
    "email": "example@domain.com",
    "password": "password"
}
```

**Response:**
```json
{
    "message": "User example@domain.com logged in"
}
```

### Edit User
**Endpoint:** `PUT /user/edit/{user_id}`

**Request:**
```json
{
    "first_name": "updated name",
    "last_name": "updated name",
    "email": "updated@example.com",
    "password": "newpassword"
}
```

**Response:**
```json
{
    "message": "User updated name updated name's data edited successfully"
}
```

### Get User by ID
**Endpoint:** `GET /user/{user_id}`

**Response:**
```json
{
    "id": "user_id",
    "first_name": "example",
    "last_name": "example",
    "email": "example@domain.com",
    "created_at": "timestamp"
}
```

### Get All Users
**Endpoint:** `GET /users`

**Response:**
```json
{
    "users": [
        {
            "id": "user_id",
            "first_name": "example",
            "last_name": "example",
            "email": "example@domain.com",
            "created_at": "timestamp"
        }
    ]
}
```

### Delete User
**Endpoint:** `DELETE /user/{user_id}`

**Response:**
```json
{
    "message": "User with ID user_id deleted successfully"
}
```

### Generate License
**Endpoint:** `POST /generate-license/{user_id}`

**Response:**
```json
{
    "license_key": "generated_license_key"
}
```

### Validate License
**Endpoint:** `POST /validate-license`

**Request:**
```json
{
    "license_key": "license_key"
}
```

**Response:**
```json
{
    "valid": true
}
```

### Get All Licenses
**Endpoint:** `GET /licenses`

**Response:**
```json
{
    "licenses": [
        {
            "id": "license_id",
            "license_key": "license_key",
            "user_id": "user_id",
            "created_at": "timestamp",
            "expires_at": "timestamp",
            "is_active": true
        }
    ]
}
```

### Create Payment
**Endpoint:** `POST /payment/create/{user_id}/{license_id}`

**Request:**
```json
{
    "amount": 1000
}
```

**Response:**
```json
{
    "session_id": "session_id",
    "url": "payment_url"
}
```

### Payment Success
**Endpoint:** `GET /payment/success`

**Request:**
```json
{
    "session_id": "session_id"
}
```

**Response:**
```json
{
    "message": "Payment successful, license activated"
}
```

### Check Payment Status
**Endpoint:** `GET /payment/check/{session_id}`

**Response:**
```json
{
    "status": "payment_status"
}
```

### Send Update Email
**Endpoint:** `POST /send-update`

**Request:**
```json
{
    "subject": "Newsletter Update",
    "message": "No message provided."
}
```

**Response:**
```json
{
    "message": "Email sent successfully"
}
```


## Error Handling
The API uses standard HTTP status codes to indicate the success or failure of an API request. Common status codes include:
- `200 OK`: The request was successful.
- `400 Bad Request`: The request was invalid or cannot be served.
- `401 Unauthorized`: Authentication failed or user does not have permissions.
- `404 Not Found`: The requested resource could not be found.
- `500 Internal Server Error`: An error occurred on the server.


## FAQ

- **What data formats are supported?**
    The API supports JSON format for both requests and responses.

## Support
For further assistance, please contact the developer at support@psaadalla.com.
