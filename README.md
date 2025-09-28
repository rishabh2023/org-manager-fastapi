# 🚀 Organization Manager API

A robust backend service built with **FastAPI**, **SQLAlchemy ORM**, **Alembic migrations**, and **Supabase Auth**. This API allows users to **create, read, update, and delete (CRUD) organizations** with **secure ownership enforcement via Supabase JWT authentication**.

## ✨ Features

- 🔐 **Secure Authentication** - JWT-based auth with Supabase
- 🏢 **Organization Management** - Full CRUD operations
- 👤 **User Ownership** - Users can only access their own organizations
- 🗄️ **Database Migrations** - Alembic-powered schema versioning
- ⚡ **Async Performance** - Built with async/await patterns
- 📊 **Health Monitoring** - Database connectivity checks
- 📝 **API Documentation** - Auto-generated OpenAPI/Swagger docs

## 📂 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entrypoint
│   ├── config.py              # Environment settings
│   ├── db.py                  # Database engine + session
│   ├── models.py              # SQLAlchemy ORM models
│   ├── schemas.py             # Pydantic schemas
│   ├── crud.py                # CRUD operations
│   ├── auth.py                # Supabase JWT validation
│   └── routers/
│       ├── __init__.py
│       ├── organizations.py   # CRUD endpoints
│       └── health.py          # Health checks (DB connection)
├── alembic/
│   ├── env.py                 # Alembic migration config
│   └── versions/              # Migration scripts
├── requirements.txt
├── .env                       # Environment variables (git ignored)
└── README.md
```

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
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate   # Linux/macOS
# OR
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Configuration

Create a `.env` file in the project root:

```env
# Supabase Postgres connection string (async for FastAPI runtime)
DATABASE_URL=postgresql+asyncpg://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres

# Supabase Auth (for JWT verification)
SUPABASE_PROJECT_ID=<your-project-id>
SUPABASE_JWKS_URL=https://<project-ref>.supabase.co/auth/v1/jwks
```

> ⚠️ **Important**: Make sure your database password is URL-encoded (e.g., `@` → `%40`, `#` → `%23`)

## 🗄️ Database Setup

We use Alembic for database migrations and schema management.

### Generate Migration (if needed)

```bash
alembic revision --autogenerate -m "create organizations table"
```

### Apply Migrations

```bash
alembic upgrade head
```

## ▶️ Running the Server

### Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

### Production Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The server will be available at:

- **Local**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs (Swagger UI)
- **ReDoc**: http://127.0.0.1:8000/redoc (Alternative API docs)

## 🛠️ API Endpoints

### Health Check

| Method | Endpoint        | Description              |
| ------ | --------------- | ------------------------ |
| `GET`  | `/api/db-check` | Test database connection |

**Response:**

```json
{
  "status": "ok",
  "db_response": 1
}
```

### Organizations

> 🔒 **All organization endpoints require authentication via `Authorization: Bearer <JWT>` header**

| Method   | Endpoint                  | Description                   |
| -------- | ------------------------- | ----------------------------- |
| `POST`   | `/api/organizations`      | Create new organization       |
| `GET`    | `/api/organizations`      | List all user's organizations |
| `GET`    | `/api/organizations/{id}` | Get specific organization     |
| `PUT`    | `/api/organizations/{id}` | Update organization           |
| `DELETE` | `/api/organizations/{id}` | Delete organization           |

### Example Requests

#### Create Organization

```bash
curl -X POST http://127.0.0.1:8000/api/organizations \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Clinic",
    "description": "Health care services",
    "is_active": true
  }'
```

#### Get Organizations

```bash
curl -X GET http://127.0.0.1:8000/api/organizations \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

## 🔐 Authentication Flow

1. **Frontend Login**: User authenticates with `supabase.auth.signInWithPassword()`
2. **JWT Token**: Supabase issues a JWT token
3. **API Request**: Token sent via `Authorization: Bearer <token>` header
4. **Validation**: FastAPI validates JWT using Supabase JWKS endpoint
5. **Authorization**: Extracted `user_id` enforces ownership via `owner_user_id` column

## 🧪 Testing

### Manual Testing with cURL

```bash
# Set your JWT token
export TOKEN="your_jwt_token_here"

# Test health endpoint
curl -X GET http://127.0.0.1:8000/api/db-check

# Test organizations endpoint
curl -X GET http://127.0.0.1:8000/api/organizations \
  -H "Authorization: Bearer $TOKEN"
```

### Using Postman

1. Import the API endpoints from the Swagger docs at `/docs`
2. Set up authentication with Bearer Token
3. Test all CRUD operations

## 📦 Dependencies

Key packages used in this project:

| Package         | Purpose                           |
| --------------- | --------------------------------- |
| **FastAPI**     | Modern, fast web framework        |
| **SQLAlchemy**  | Async ORM for database operations |
| **Alembic**     | Database migration tool           |
| **asyncpg**     | Async PostgreSQL driver           |
| **python-jose** | JWT token validation              |
| **httpx**       | Async HTTP client for JWKS        |
| **pydantic**    | Data validation and settings      |

See `requirements.txt` for complete dependency list.

### Environment Variables for Production

```env
DATABASE_URL=postgresql+asyncpg://...
SUPABASE_PROJECT_ID=...
SUPABASE_JWKS_URL=...
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you have any questions or need help, please:

- Open an issue on GitHub
- Check the [API documentation](http://127.0.0.1:8000/docs) when running locally

---

**Built with ❤️ using FastAPI and Supabase**
