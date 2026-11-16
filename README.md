# Sport Club Management System

A Django web application for running a sports club: athletes, coaches, gyms and training sessions, with attendance tracking for every session.

## Table of Contents

- [Features](#features)
- [Roles and permissions](#roles-and-permissions)
- [Tech stack](#tech-stack)
- [Data model](#data-model)
- [Getting started](#getting-started)
- [Test accounts](#test-accounts)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Project structure](#project-structure)

## Features

- **Dashboard** with the total number of coaches, athletes and gyms.
- **Athletes**: list with search by last name and pagination, profile page with coaches and attended sessions, create / update / delete.
- **Coaches**: list with search by username, profile page with gyms, athletes and sessions, update / delete.
- **Gyms**: list with search by address, detail page with assigned coaches and sessions, create / update / delete.
- **Training sessions**: list, detail page, create / update / delete. A session belongs to one gym and one coach and has a list of athletes.
- **Attendance**: on the session page the session's coach (or a staff user) ticks the athletes who attended.
- **Sign up / log in / log out**. Every new user is registered as an athlete.
- **Data integrity**: a gym or coach that still has training sessions cannot be deleted; the user gets a message instead of an error.

## Roles and permissions

| Action                                   | Anonymous | Logged-in user | Session coach | Admin (staff) |
|------------------------------------------|:---------:|:--------------:|:-------------:|:-------------:|
| View lists and detail pages              | ✅        | ✅             | ✅            | ✅            |
| Create / update / delete records         |           | ✅             | ✅            | ✅            |
| Mark attendance for a session            |           |                | ✅            | ✅            |
| Create a coach or change a user's role   |           |                |               | ✅ (`/admin/`) |

There is no coach sign-up on the site: an administrator creates coaches, or promotes an athlete, in the Django admin by setting the **Role** field.

## Tech stack

- Python 3.12+, Django 6.1
- PostgreSQL in production, SQLite for local development
- Bootstrap 5 with `django-crispy-forms` / `crispy-bootstrap5`
- WhiteNoise for static files, Gunicorn as the WSGI server
- `django-debug-toolbar` for local debugging
- Deployed on Render

## Data model

The diagram is in [`database-structure.drawio`](database-structure.drawio) (open it with [diagrams.net](https://app.diagrams.net/)).

- **User** (custom `AUTH_USER_MODEL`, extends `AbstractUser`): `role` (`athlete` / `coach`), `birth_date`, `weight`, `coaches` (many-to-many to coaches, reverse name `athletes`).
- **Gym**: `address`, `coaches` (many-to-many to coaches, reverse name `gyms`).
- **TrainingSession**: `starts_at`, `ends_at`, `gym` (FK, protected), `coach` (FK, protected), `athletes` (many-to-many, the attendance list). A session can't end before it starts.

## Getting started

### Prerequisites

- Python 3.12 or higher
- pip

### Installation

```bash
git clone https://github.com/NikitaFilipovWork/sport-club.git
cd sport-club

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py loaddata club_data.json
python manage.py createsuperuser  # optional, to use /admin/
python manage.py runserver
```

Open http://127.0.0.1:8000/.

By default `manage.py` uses `core.settings.dev` with a local SQLite database, so no `.env` file is needed for local development.

## Test accounts

`club_data.json` contains 10 coaches, 100 athletes, 6 gyms and 54 training sessions. After loading it you can log in with:

| Role    | Username             | Password         |
|---------|----------------------|------------------|
| Coach   | `olena.shevchenko`   | `SportClub2026!` |
| Athlete | `yaroslav.kovalchuk` | `SportClub2026!` |

All users from the fixture share the same password.

## Configuration

Settings are split into three modules:

| Module               | Purpose                                                |
|----------------------|--------------------------------------------------------|
| `core.settings.base` | Shared settings                                        |
| `core.settings.dev`  | `DEBUG = True`, SQLite (`db.sqlite3`)                  |
| `core.settings.prod` | `DEBUG = False`, PostgreSQL, host from Render          |

`manage.py` reads environment variables from a `.env` file in the project root (via `python-dotenv`). Production uses these variables:

| Variable                   | Description                                              |
|----------------------------|----------------------------------------------------------|
| `DJANGO_SETTINGS_MODULE`   | `core.settings.prod` in production                       |
| `POSTGRES_DB`              | Database name                                            |
| `POSTGRES_USER`            | Database user                                            |
| `POSTGRES_PASSWORD`        | Database password                                        |
| `POSTGRES_HOST`            | Database host                                            |
| `POSTGRES_DB_PORT`         | Database port (required, e.g. `5432`)                    |
| `RENDER_EXTERNAL_HOSTNAME` | Public hostname, added to `ALLOWED_HOSTS` (set by Render) |

> **Note:** if your local `.env` sets `DJANGO_SETTINGS_MODULE=core.settings.prod`, every `manage.py` command (`migrate`, `loaddata`, `shell`…) runs against the production database.

## Deployment

The project is deployed on [Render](https://render.com/):

- **Build command:** `./build.sh` (installs requirements, runs `collectstatic` and `migrate`)
- **Start command:** `gunicorn core.wsgi`
- **Environment:** the variables from [Configuration](#configuration), including `DJANGO_SETTINGS_MODULE=core.settings.prod`

To fill the production database with demo data, run `python manage.py loaddata club_data.json` once with the production settings.

## Project structure

```
sport-club/
├── club/                  # Main app: models, views, forms, urls, admin
│   └── migrations/
├── core/                  # Project config
│   ├── settings/          # base.py, dev.py, prod.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── templates/
│   ├── club/              # Pages for athletes, coaches, gyms, sessions
│   ├── include/           # Sidebar, pagination
│   └── registration/      # Login, logout, sign up
├── static/                # styles.css
├── club_data.json         # Demo data fixture
├── database-structure.drawio
├── build.sh               # Render build script
├── manage.py
└── requirements.txt
```
