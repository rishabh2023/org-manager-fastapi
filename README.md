# 🚀 Organization Manager API

A robust backend service built with **FastAPI**, **SQLAlchemy ORM**, **Alembic migrations**, and **Supabase Auth**. This API allows users to **create, read, update, and delete (CRUD) organizations** with **secure ownership enforcement via Supabase JWT authentication**.

---

## ✨ Features

- 🔐 **Secure Authentication** - JWT-based auth with Supabase
- 🏢 **Organization Management** - Full CRUD operations
- 👤 **User Ownership** - Users can only access their own organizations
- 🗄️ **Database Migrations** - Alembic-powered schema versioning
- ⚡ **Async Performance** - Built with async/await patterns
- 📊 **Health Monitoring** - Database connectivity checks
- 📝 **API Documentation** - Auto-generated OpenAPI/Swagger docs

---

## 📂 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entrypoint
│   ├── config.py               # Environment settings
│   ├── db.py                   # Database engine + session
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic schemas
│   ├── crud.py                 # CRUD operations
│   ├── auth.py                 # Supabase JWT validation
│   └── routers/
│       ├── __init__.py
│       ├── organizations.py    # CRUD endpoints
│       └── health.py           # Health checks (DB connection)
├── alembic/
│   ├── env.py                  # Alembic migration config
│   └── versions/               # Migration scripts
├── requirements.txt
├── .env                        # Environment variables (git ignored)
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.8+
- PostgreSQL database (Supabase recommended)
- Supabase project with Auth enabled

### 1. Clone Repository

```bash
git clone https://github.com/your-username/org-manager-fastapi.git
cd org-manager-fastapi
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
# OR
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Create a `.env` file in the project root:

```env
# Supabase Postgres connection string (async for FastAPI runtime)
DATABASE_URL=postgresql+asyncpg://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres

# Supabase Auth
SUPABASE_PROJECT_ID=<your-project-id>
SUPABASE_JWKS_URL=https://<project-ref>.supabase.co/auth/v1/.well-known/jwks.json
SUPABASE_ANON_KEY=<your-anon-key>
```

### How to Get These Values:

1. **DATABASE_URL**: Go to **Supabase Dashboard → Project Settings → Database → Connection String**

   - Select **Connection pooling** and choose **Session mode**
   - Replace `postgresql://` with `postgresql+asyncpg://`

2. **SUPABASE_PROJECT_ID**: Found in **Project Settings → General**

3. **SUPABASE_JWKS_URL**: Replace `<project-ref>` with your project reference ID (e.g., `abcdefghijklm`)

4. **SUPABASE_ANON_KEY**: Go to **Project Settings → API → Project API keys** and copy the `anon` `public` key

---

## 🔐 Supabase Auth Setup

Follow these steps in your Supabase dashboard to set up secure JWT authentication:

### Step 1: Navigate to JWT Settings

Go to **Settings → API → JWT Keys** in your Supabase dashboard.

### Step 2: Rotate Keys (Recommended)

By default, Supabase uses **Legacy HS256 (Shared Secret)** for JWT signing. For better security, rotate to **ES256 (Elliptic Curve)**:

1. Click the **"Rotate keys"** button
2. After rotation:
   - **Current Key** switches to **ECC (P-256)**
   - Supabase now issues **ES256 JWTs**
   - ✅ You no longer need `SUPABASE_JWT_SECRET`

### Step 3: If You Haven't Rotated Yet

If you're still using the legacy HS256 system:

1. Go to the **Legacy JWT Secret** tab
2. Copy the secret value
3. Add it to your `.env` file:

```env
SUPABASE_JWT_SECRET=your-legacy-hs256-secret
```

> **Note:** This is only needed for projects that haven't rotated keys yet.

### Step 4: Verify JWKS Endpoint

Confirm your JWKS endpoint is accessible:

```
https://<project-ref>.supabase.co/auth/v1/.well-known/jwks.json
```

This endpoint should return JSON with your ES256 public key(s).

### Step 5: Your FastAPI Service is Ready

The `auth.py` file in this project automatically handles both:

- **HS256** tokens (legacy)
- **ES256** tokens (after rotation)

No code changes needed! 🎉

---

## 🗄️ Database Setup

We use Alembic for database migrations and schema management.

### Generate Migration

```bash
alembic revision --autogenerate -m "create organizations table"
```

### Apply Migration

```bash
alembic upgrade head
```

### Rollback (if needed)

```bash
alembic downgrade -1
```

---

## ▶️ Running the Server

### Development Mode

```bash
uvicorn app.main:app --reload --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Access Documentation

Once the server is running, access the auto-generated API docs:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🛠️ API Endpoints

### Health Check

| Method | Endpoint        | Description              |
| ------ | --------------- | ------------------------ |
| `GET`  | `/api/db-check` | Test database connection |

**Example:**

```bash
curl http://localhost:8000/api/db-check
```

---

### Organizations

> 🔒 **All organization endpoints require authentication**  
> Include `Authorization: Bearer <JWT>` header in all requests

| Method   | Endpoint                  | Description                   |
| -------- | ------------------------- | ----------------------------- |
| `POST`   | `/api/organizations`      | Create new organization       |
| `GET`    | `/api/organizations`      | List all user's organizations |
| `GET`    | `/api/organizations/{id}` | Get specific organization     |
| `PUT`    | `/api/organizations/{id}` | Update organization           |
| `DELETE` | `/api/organizations/{id}` | Delete organization           |

#### Create Organization

```bash
curl -X POST http://localhost:8000/api/organizations \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Company",
    "description": "A great organization"
  }'
```

#### List Organizations

```bash
curl http://localhost:8000/api/organizations \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Get Organization by ID

```bash
curl http://localhost:8000/api/organizations/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Update Organization

```bash
curl -X PUT http://localhost:8000/api/organizations/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Company Name",
    "description": "Updated description"
  }'
```

#### Delete Organization

```bash
curl -X DELETE http://localhost:8000/api/organizations/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 🔐 Authentication Flow

1. **Frontend** calls `supabase.auth.signInWithPassword()` or similar auth method
2. Supabase issues a **JWT token** (ES256 after key rotation, HS256 for legacy)
3. Frontend sends token in `Authorization: Bearer <token>` header with API requests
4. FastAPI validates token via JWKS endpoint (for ES256) or shared secret (for HS256)
5. User `sub` (UUID) is extracted from token and used for ownership checks
6. API returns data only for resources owned by the authenticated user

---

## 📦 Dependencies

| Package           | Purpose                           |
| ----------------- | --------------------------------- |
| **FastAPI**       | Modern, fast web framework        |
| **SQLAlchemy**    | Async ORM for database operations |
| **Alembic**       | Database migration tool           |
| **asyncpg**       | Async PostgreSQL driver           |
| **python-jose**   | JWT token validation              |
| **httpx**         | Async HTTP client for JWKS        |
| **pydantic**      | Data validation and settings      |
| **python-dotenv** | Environment variable management   |

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🧪 Testing the API

### 1. Get a JWT Token

Sign in through your frontend or use Supabase Auth API:

```bash
curl -X POST https://<project-ref>.supabase.co/auth/v1/token?grant_type=password \
  -H "apikey: YOUR_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your-password"
  }'
```

### 2. Use the Token

Copy the `access_token` from the response and use it in API calls:

```bash
curl http://localhost:8000/api/organizations \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🐛 Troubleshooting

### Database Connection Issues

**Error:** `could not connect to server`

**Solution:** Check your `DATABASE_URL` in `.env` and ensure:

- Password is correct
- Project reference ID is correct
- Network allows connection to Supabase

### JWT Validation Fails

**Error:** `Could not validate credentials`

**Solution:**

- Verify `SUPABASE_JWKS_URL` is correct
- If using legacy keys, ensure `SUPABASE_JWT_SECRET` is set
- Check that token hasn't expired (default: 1 hour)

### Migration Issues

**Error:** `Target database is not up to date`

**Solution:**

```bash
alembic upgrade head
```

---

## 📝 License

MIT License – see [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**Built with ❤️ using FastAPI and Supabase**

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
