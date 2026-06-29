# Contact Book API

A RESTful API built with Django and Django REST Framework that lets authenticated users manage their personal contacts.

## Features

- Token-based authentication (register, login, logout)
- Full CRUD for contacts (scoped per user)
- `IsOwner` object-level permission — users can only access their own contacts
- Search contacts by name, email, or phone
- Sort by name or creation date
- Pagination (10 contacts per page)
- Toggle favourite flag
- Contact stats (total, favourites, added this month)

## Tech Stack

- Python 3.13
- Django 6.x
- Django REST Framework
- SQLite (development)

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/contactbook.git
cd contactbook

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install django djangorestframework

# 4. Run migrations
python manage.py migrate

# 5. Start the dev server
python manage.py runserver
```

## API Endpoints

All contact endpoints require `Authorization: Token <your-token>` header.

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/register/` | Create a new account |
| POST | `/api/v1/login/` | Get an auth token |
| POST | `/api/v1/logout/` | Invalidate token |

**Register payload:**
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "securepass123",
  "password2": "securepass123"
}
```

**Login payload:**
```json
{ "username": "john", "password": "securepass123" }
```

### Contacts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/contacts/` | List contacts (paginated) |
| POST | `/api/v1/contacts/` | Create a contact |
| GET | `/api/v1/contacts/{id}/` | Retrieve a contact |
| PUT | `/api/v1/contacts/{id}/` | Full update |
| PATCH | `/api/v1/contacts/{id}/` | Partial update |
| DELETE | `/api/v1/contacts/{id}/` | Delete a contact |
| POST | `/api/v1/contacts/{id}/toggle_favourite/` | Toggle favourite flag |
| GET | `/api/v1/contacts/stats/` | Summary stats |

### Query Parameters

| Param | Example | Description |
|-------|---------|-------------|
| `search` | `?search=john` | Filter by name, email, or phone |
| `ordering` | `?ordering=-created_at` | Sort (prefix `-` for descending) |
| `page` | `?page=2` | Navigate paginated results |

### Paginated Response Format

```json
{
  "count": 25,
  "next": "http://localhost:8000/api/v1/contacts/?page=2",
  "previous": null,
  "results": [...]
}
```

### Contact Payload

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "9876543210",
  "address": "123 Main St",
  "is_favourite": false
}
```

## Project Structure

```
contactbook/
├── api/               # DRF app — serializers, views, permissions, URLs
│   ├── permissions.py # IsOwner permission class
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── contact/           # Django model for Contact
│   └── models.py
├── contactbook/       # Project settings and root URLs
│   ├── settings.py
│   └── urls.py
└── manage.py
```
