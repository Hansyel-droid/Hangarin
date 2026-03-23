# Hangarin — To-Do Manager
A Django-based To-Do application built for midterm project requirements.

## Project Setup

### 1. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed the database with sample data
```bash
python manage.py seed_data
```

### 5. Create a superuser (for Admin Panel access)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** for the app and **http://127.0.0.1:8000/admin/** for the admin panel.

---

## Features
- **Dashboard** — Live summary cards: total, completed, pending, in-progress, and yearly task counts
- **Task CRUD** — Create, Read, Update, Delete tasks with title, description, deadline, status, category, and priority
- **Sub-Tasks** — Break tasks into smaller steps with toggle completion
- **Notes** — Attach freeform notes to any task
- **Categories & Priorities** — Full CRUD management for both
- **Search** — Filter tasks by title, description, or category name
- **Sorting** — Sort by name, created date, deadline, or status
- **Pagination** — 10 items per page on all list views
- **Admin Panel** — Configured with search, filters, and custom list displays

## Models
- `BaseModel` — Abstract model with `created_at` and `updated_at`
- `Priority` — Task priority level (High, Medium, Low, Critical, Optional)
- `Category` — Task category (Work, School, Personal, Finance, Projects)
- `Task` — Core model with FK to Category and Priority; status choices via enumeration
- `Note` — FK to Task; freeform text content
- `SubTask` — FK to Task; own title and status choices

## Deployment to PythonAnywhere
1. Upload the project via Git or ZIP
2. Create a new web app (Manual Configuration, Python 3.x)
3. Set the virtual environment path
4. Configure `WSGI` to point to `hangarin_todo.wsgi`
5. Set `DEBUG = False` and add your PythonAnywhere domain to `ALLOWED_HOSTS`
6. Run `python manage.py collectstatic`
7. Reload the web app
