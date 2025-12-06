# HNG Stage 7 – Task 3  
## Mini Authentication + API Key System (FastAPI)

This project implements a **mini authentication system** that supports:

- **User login via JWT**
- **Service-to-service access via API keys**
- **Route protection based on access type** (user vs service)

It is built as a backend-only FastAPI service, with no frontend.  
Interactive API docs are available via Swagger at `/docs`.

---

## Features

### 1. User Authentication (JWT)

- `POST /auth/signup` – Create a new user.
- `POST /auth/login` – Login with email and password, returns a JWT.
- `GET /users/me` – Get the current authenticated user (JWT only).

### 2. API Key Management

- `POST /keys/create` – Create a new API key (for service-to-service calls).
- `GET /keys/` – List all API keys belonging to the current user.
- `POST /keys/{key_id}/revoke` – Revoke an existing API key.

Notes:

- Only the **plain API key** is returned once at creation time.
- API keys have:
  - `label` – human-friendly name (e.g. `payments-service`).
  - Optional **expiry** (`expires_in_days`), capped between 1 and 365 days.
  - `revoked` flag.
  - `last_used_at` timestamp (updated when a key is used).

### 3. Service-to-Service Access

- `GET /service/ping` – Example **service-only** endpoint.
  - Requires header: `x-api-key: <plain-api-key>`.
  - Returns info about the API key and its owner.
- API keys are validated server-side by:
  - Checking `revoked` and `expires_at`.
  - Verifying the provided key against the stored `key_hash`.

### 4. Health Check

- `GET /health` – Simple health endpoint returning `{ "status": "ok" }`.

---

## Tech Stack

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.x
- **Migrations**: Alembic
- **Auth / Crypto**:
  - `passlib` with `bcrypt_sha256`
  - `python-jose` for JWT
- **Tooling**:
  - `uvicorn` ASGI server
  - `ruff` + `pre-commit` for linting/formatting

---

## Project Structure

```text
.
├── alembic.ini
├── migrations/           # Alembic migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── app/
│   ├── main.py           # FastAPI app factory
│   ├── core/
│   │   ├── config.py     # Settings (env-based)
│   │   └── security.py   # Password hashing, JWT, API key utilities
│   ├── db/
│   │   ├── base.py       # SQLAlchemy Base
│   │   └── session.py    # Engine & SessionLocal
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py       # User model
│   │   └── api_key.py    # ApiKey model
│   ├── schemas/
│   │   ├── user.py       # Pydantic User schemas
│   │   ├── auth.py       # Login & Token schemas
│   │   └── api_key.py    # API key schemas
│   └── api/
│       ├── deps.py       # Auth dependencies (JWT & API key)
│       └── routes/
│           ├── health.py
│           ├── auth.py
│           ├── users.py
│           ├── keys.py
│           └── service.py
├── run.py                # Uvicorn entrypoint (uses APP_* settings)
├── requirements.txt
├── .pre-commit-config.yaml
└── README.md
```

---

## Configuration

Configuration is managed via `pydantic-settings` in `app/core/config.py`.

### Environment Variables (.env)

Example `.env`:

```env
APP_NAME=HNG Stage 7 - Task 3
APP_ENV=development
APP_PORT=8000
APP_DEBUG=true

DATABASE_URL=postgresql://user:password@localhost:5432/mini_auth_api_key_db

JWT_SECRET_KEY=change-me-to-a-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

- `APP_DEBUG=true` enables `uvicorn` reload.
- `JWT_SECRET_KEY` should be a long random string. You can generate one with:

  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(64))"
  ```

---

## Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/emmanueldev247/hng-stage7-task.git
cd hng-stage7-task
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Copy the example env (if present) or create `.env` manually:

```bash
cp .env.example .env  # if you have one
# then edit .env to set DATABASE_URL and JWT_SECRET_KEY
```

### 5. Create PostgreSQL database

In `psql`:

```sql
CREATE DATABASE mini_auth_api_key_db;
```

Ensure your `DATABASE_URL` points to this DB.

### 6. Run migrations

Use Alembic to create tables:

```bash
alembic upgrade head
```

This will create the `users` and `api_keys` tables in `mini_auth_api_key_db`.

---

## Running the Application

### Development

```bash
python run.py
```

This uses `APP_PORT` and `APP_DEBUG` from `.env`:

- `APP_DEBUG=true` → `uvicorn` runs with `reload=True`.
- The app will be available at: `http://127.0.0.1:8000`

### Production (example)

In production-like mode:

```env
APP_ENV=production
APP_DEBUG=false
APP_PORT=8000
```

Then:

```bash
python run.py
```

Or use the underlying command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## API Documentation

FastAPI provides interactive API docs:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

Example Swagger view:

<img width="1013" height="667" alt="image" src="https://github.com/user-attachments/assets/1a1650f0-b81e-4065-ad4d-f9802311a878" />

---

## Auth Flows - with sample request/response screenshot 

### 1. User Signup & Login (JWT)

**Signup**

- `POST /auth/signup`
- Request body:
  ```json
  {
    "email": "user@example.com",
    "password": "StrongPass1!"
  }
  ```
<img width="661" height="456" alt="Screenshot 2025-12-06 053629" src="https://github.com/user-attachments/assets/fe1fc81f-bd94-4396-aa62-02234f8ce7dc" />
<img width="613" height="455" alt="Screenshot 2025-12-06 053635" src="https://github.com/user-attachments/assets/5c99d1f8-f299-481f-84cd-4335b7a58646" />

**Login**

- `POST /auth/login`
- Request body:
  ```json
  {
    "email": "user@example.com",
    "password": "StrongPass1!"
  }
  ```
- Response:
  ```json
  {
    "access_token": "<JWT>",
    "token_type": "bearer"
  }
  ```
<img width="1106" height="428" alt="Screenshot 2025-12-06 053658" src="https://github.com/user-attachments/assets/0db3e74a-b5ea-4e6b-9d49-4cf9c042e878" />
<img width="919" height="373" alt="Screenshot 2025-12-06 053733" src="https://github.com/user-attachments/assets/15bef02c-8aed-44ee-86c8-479cd76a65a7" />


**Get current user**

- `GET /users/me`
- Header:
  ```http
  Authorization: Bearer <JWT>
  ```
<img width="1072" height="374" alt="Screenshot 2025-12-06 053747" src="https://github.com/user-attachments/assets/604f487d-3b5b-418c-9e16-470b1d114aad" />


---

### 2. API Key Lifecycle

**Create API key**

- `POST /keys/create`
- Requires user JWT (Bearer).
- Request body:
  ```json
  {
    "label": "payments-service",
    "expires_in_days": 30
  }
  ```
- Response (plain key shown once):
  ```json
  {
    "api_key": "svc_xxx",
    "label": "payments-service",
    "expires_at": "2025-01-01T00:00:00+00:00"
  }
  ```
<img width="1072" height="353" alt="Screenshot 2025-12-06 053815" src="https://github.com/user-attachments/assets/90b3d566-fd64-41f5-90ba-d3529b230990" />
<img width="1142" height="452" alt="Screenshot 2025-12-06 053851" src="https://github.com/user-attachments/assets/936af152-f877-4048-9889-87b774dfc2a8" />

**List API keys**

- `GET /keys/`
- Header:
  ```http
  Authorization: Bearer <JWT>
  ```
- Response:
  ```json
  [
    {
      "id": 1,
      "label": "payments-service",
      "created_at": "...",
      "expires_at": "...",
      "revoked": false
    }
  ]
  ```
<img width="1070" height="448" alt="Screenshot 2025-12-06 053916" src="https://github.com/user-attachments/assets/893b8d2b-849d-4a48-9f32-c27496a61952" />


**Revoke API key**

- `POST /keys/{key_id}/revoke`
- Marks the key as `revoked=true`.

<img width="1055" height="407" alt="image" src="https://github.com/user-attachments/assets/8b063e93-1ccd-478b-86d4-70cbc5cebd6b" />

---

### 3. Service-to-Service Access

**Service ping**

- `GET /service/ping`
- Requires header:
  ```http
  x-api-key: <plain-api-key>
  ```
- Response:
  ```json
  {
    "status": "ok",
    "service_label": "payments-service",
    "owner_user_id": 1,
    "api_key_id": 1
  }
  ```


if no key is provided, the endpoint returns:

```json
{
  "detail": "Missing x-api-key head"
}
```

<img width="708" height="377" alt="Screenshot 2025-12-06 053938" src="https://github.com/user-attachments/assets/ed082e75-e498-49f7-b3d9-8a4a64730892" />


If the key is valid, the endpoint returns:

```json
{
  "status": "ok",
  "service_label": "hng-token",
  "owner_user_id": 4,
  "api_key_id": 2
}
```
<img width="846" height="417" alt="Screenshot 2025-12-06 053951" src="https://github.com/user-attachments/assets/86a8bcf9-31fa-4099-bbe3-e2e57e705d74" />


If the key is expired or revoked, the endpoint returns:

```json
{
  "detail": "Invalid API key"
}
```

with HTTP `401 Unauthorized`.



<img width="679" height="409" alt="image" src="https://github.com/user-attachments/assets/51a16956-746b-4b37-9003-56234d817963" />

---

## Curl Examples

**Login:**

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "StrongPass1!"}'
```

**Get current user:**

```bash
curl http://127.0.0.1:8000/users/me \
  -H "Authorization: Bearer <JWT>"
```

**Create API key:**

```bash
curl -X POST http://127.0.0.1:8000/keys/create \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"label":"payments-service","expires_in_days":30}'
```

**Service-only ping:**

```bash
curl http://127.0.0.1:8000/service/ping \
  -H "x-api-key: <plain-api-key>"
```

---

## Security Considerations

- Passwords are hashed using **`bcrypt_sha256` via passlib**.
- JWTs are signed using `HS256` and a configurable `JWT_SECRET_KEY`.
- API keys are **never stored in plaintext**; only a hash is stored.
- API keys can be **revoked** and optionally **expire**.
- Routes are protected based on:
  - JWT Bearer auth (`Authorization: Bearer <token>`) for **users**.
  - API key header (`x-api-key`) for **services**.

This is not a full production-ready auth system, but it follows good practices for a mini backend project.

---

## Development Tooling

### Ruff + pre-commit

Ruff and pre-commit are configured in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.5
    hooks:
      - id: ruff
        language_version: python3.12
        args: ["--fix"]
        exclude: ^(migrations/|alembic/|__pycache__/|\.venv/)
      - id: ruff-format
```

To enable:

```bash
pre-commit install
pre-commit run --all-files
```

---

## Migrations

Generate a new migration after model changes:

```bash
alembic revision --autogenerate -m "describe change"
```

Apply migrations:

```bash
alembic upgrade head
```

---

