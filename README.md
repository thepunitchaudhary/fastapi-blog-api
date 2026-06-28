# FastAPI Blog API

A backend REST API for a blogging platform, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. Supports full CRUD operations on blog posts, JWT-based authentication, pagination, and search.

## Features

- 📝 Create, read, update, and delete blog posts
- 🔐 JWT authentication for protected routes
- 🔎 Search blogs by title
- 📄 Pagination on the blog listing endpoint
- 🗄️ PostgreSQL persistence via SQLAlchemy ORM
- ✅ Request/response validation with Pydantic

## Tech Stack

| Component       | Technology          |
|-----------------|----------------------|
| Framework       | FastAPI              |
| ORM             | SQLAlchemy           |
| Database        | PostgreSQL           |
| Auth            | JWT (via `python-jose`) |
| Validation      | Pydantic             |
| Server          | Uvicorn              |

## Project Structure

```
.
├── main.py        # App entrypoint and route definitions
├── models.py      # SQLAlchemy ORM models
├── schemas.py      # Pydantic request/response schemas
├── database.py     # Database engine/session configuration
├── auth.py         # JWT creation and verification logic
├── .env            # Environment variables (not committed)
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL running locally or remotely

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/fastapi-blog-api.git
   cd fastapi-blog-api
   ```

2. **Create a virtual environment and activate it**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose python-dotenv pydantic
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<dbname>
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

## API Reference

### Auth

| Method | Endpoint  | Description           | Protected |
|--------|-----------|------------------------|-----------|
| POST   | `/login`  | Issues a JWT access token | No     |

### Blogs

| Method | Endpoint        | Description                        | Protected |
|--------|-----------------|-------------------------------------|-----------|
| GET    | `/`             | Health check / welcome message     | No        |
| GET    | `/blogs`        | List blogs (supports pagination & search) | No  |
| GET    | `/blogs/{id}`   | Get a single blog by ID            | Yes       |
| POST   | `/blogs`        | Create a new blog                  | Yes       |
| PUT    | `/blogs/{id}`   | Update an existing blog            | Yes       |
| DELETE | `/blogs/{id}`   | Delete a blog                      | Yes       |

#### Query Parameters — `GET /blogs`

| Param   | Type | Default | Description                  |
|---------|------|---------|-------------------------------|
| page    | int  | 1       | Page number                  |
| limit   | int  | 5       | Results per page              |
| search  | str  | ""      | Filter blogs by title (case-insensitive) |

#### Authentication

Protected routes require a Bearer token obtained from `/login`:

```bash
curl -X POST http://127.0.0.1:8000/login
```

Use the returned `access_token` in subsequent requests:

```bash
curl -X GET http://127.0.0.1:8000/blogs/1 \
  -H "Authorization: Bearer <access_token>"
```

> **Note:** `/login` currently issues a token without validating credentials. Replace this with real user authentication (e.g. a users table with hashed passwords) before deploying to production.

### Example Request — Create a Blog

```bash
curl -X POST http://127.0.0.1:8000/blogs \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "Hello, world!"}'
```

**Response**

```json
{
  "id": 1,
  "title": "My First Post",
  "content": "Hello, world!"
}
```

## Roadmap

- [ ] Real user authentication (signup/login with hashed passwords)
- [ ] Role-based access control
- [ ] Alembic migrations
- [ ] Unit and integration tests
- [ ] Dockerfile and docker-compose setup

## License

This project is open source and available under the [MIT License](LICENSE).
