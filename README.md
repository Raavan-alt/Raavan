# SK Builders — FastAPI Backend

Complete backend for the SK Builders construction website with:
- 🔐 Admin authentication (JWT)
- 🏗️ Project gallery management (CRUD + before/after image uploads)
- 📋 Quote request form handling
- 📁 SQLite database (easily swappable to PostgreSQL)

---

## Project Structure

```
skbuilders/
├── main.py                   # App entry point
├── requirements.txt
├── uploads/
│   └── projects/             # Uploaded images stored here
└── app/
    ├── database.py           # SQLAlchemy engine & session
    ├── auth_utils.py         # JWT + password hashing
    ├── models/
    │   └── models.py         # DB table definitions
    ├── schemas/
    │   └── schemas.py        # Pydantic request/response models
    └── routers/
        ├── auth.py           # POST /api/auth/login & /register
        ├── projects.py       # CRUD for project gallery
        └── quotes.py         # Quote form submissions
```

---

## Quick Start

### 1. Install dependencies
```bash
cd skbuilders
pip install -r requirements.txt
```

### 2. Run the server
```bash
uvicorn main:app --reload
```
API available at: `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

### 3. Create your first admin account
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'
```
> ⚠️ Delete or protect the `/api/auth/register` endpoint after setup!

---

## API Reference

### 🔐 Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create admin account (first-time setup only) |
| POST | `/api/auth/login` | Login → returns JWT token |

### 🏗️ Projects (Public)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects/` | List projects (filter by status, paginate) |
| GET | `/api/projects/{id}` | Get single project |

**Filter examples:**
```
GET /api/projects/?status=in_progress
GET /api/projects/?status=completed
GET /api/projects/?status=industrial
GET /api/projects/?skip=0&limit=6        ← Load More pagination
```

### 🏗️ Projects (Admin — requires Bearer token)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/projects/` | Create project + upload images |
| PUT | `/api/projects/{id}` | Update project + replace images |
| DELETE | `/api/projects/{id}` | Delete project |

**Create project example:**
```bash
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "title=SK Office Tower" \
  -F "description=Ground-up commercial build" \
  -F "status=in_progress" \
  -F "before_image=@before.jpg" \
  -F "after_image=@after.jpg"
```

### 📋 Quotes
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/quotes/` | Public | Submit quote request |
| GET | `/api/quotes/` | Admin | List all submissions |
| PATCH | `/api/quotes/{id}/read` | Admin | Mark as read |
| DELETE | `/api/quotes/{id}` | Admin | Delete submission |

**Submit quote example (from frontend):**
```javascript
await fetch('http://localhost:8000/api/quotes/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    full_name:    "John Smith",
    email:        "john@example.com",
    phone:        "+91 98765 43210",
    company:      "ABC Corp",
    project_type: "Commercial",
    message:      "We need a warehouse built..."
  })
});
```

---

## Frontend Integration

### Connecting the "Request a Quote" button
Point your quote form to:
```
POST http://localhost:8000/api/quotes/
```

### Loading the Project Gallery
```javascript
// All projects (first page)
fetch('http://localhost:8000/api/projects/?limit=6')

// Filter by status tab
fetch('http://localhost:8000/api/projects/?status=in_progress&limit=6')

// Load More button
fetch('http://localhost:8000/api/projects/?skip=6&limit=6')
```

### Image URLs
Images are served at:
```
http://localhost:8000/uploads/projects/<filename>
```
The `before_image` and `after_image` fields in project responses return the full path.

---

## Switching to PostgreSQL

Replace the `DATABASE_URL` in `app/database.py`:
```python
DATABASE_URL = "postgresql://user:password@localhost/skbuilders"
```
And add `psycopg2-binary` to `requirements.txt`.

---

## Security Checklist for Production
- [ ] Change `SECRET_KEY` in `auth_utils.py` to a long random string
- [ ] Remove or lock down `/api/auth/register`
- [ ] Set `allow_origins` in CORS to your frontend domain only
- [ ] Switch to PostgreSQL
- [ ] Use HTTPS
