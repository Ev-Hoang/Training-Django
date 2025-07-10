# 🌱 Training Django Project

This is a Django REST API project using **PostgreSQL** as the database, **Redis** for caching, and **PDM** as the package manager.  
It follows modern Python project structure and is suitable for development in both local and containerized environments.

---

## ⚙️ Features

- Django REST Framework API
- PostgreSQL for relational data
- Redis for caching
- PDM for Python dependency management (PEP 582)
- Environment-based configuration
- Ready for Docker & production-ready structure

---

## 🚀 Installation (Local Dev)

> ⚠️ Requires: Python 3.11 or higher, Redis & PostgreSQL installed

### 1. Clone this repo

```bash
git clone https://github.com/your-username/training-django.git
cd training-django
```

### 2. Install PDM (if not installed)

```bash
curl -sSL https://pdm-project.org/install-pdm.py | python3
```

Or with pip:

```bash
pip install pdm
```

### 3. Install dependencies

```bash
pdm install
```

If you're not using .venv/, PDM will install packages into __pypackages__/.

### 4. Configure environment variables
Create a .env file in the root:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
REDIS_URL=redis://localhost:6379/0
```

### 5. Apply migrations

```bash
pdm run python manage.py migrate
```

### 6. Create superuser (optional)

```bash
pdm run python manage.py createsuperuser
```

### 7. Run server

```bash
pdm run python manage.py runserver
```

## 🐳 Run with Docker (optional)
Make sure you have Docker and Docker Compose installed

```bash
docker-compose up --build
```

This will start:

Django app

PostgreSQL DB

Redis cache

## 🧪 Running Tests
```bash
pdm run python manage.py test
```
If you use pytest, add:

```bash
pdm add pytest pytest-django
pdm run pytest
```

## 📝 Notes
This project uses PDM instead of pip or pipenv.

All packages are defined in pyproject.toml

For production, it's recommended to use .env with real credentials and disable DEBUG.

## 👤 Author
Made by Ev (Hoàng Đức Kiên)
