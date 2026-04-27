# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Development server
python manage.py runserver

# Run all tests
python manage.py test

# Run a single test
python manage.py test accounting.tests.ClassName.test_method

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files (required before production)
python manage.py collectstatic --noinput
```

No Makefile — this is a pure Django project. Python version is 3.11 (CI) / 3.12 (Docker).

## Architecture

**Django project:** `rdie/` (settings, URLs, WSGI)  
**Main app:** `accounting/` (all business logic)

### Data Model

The core models form a hierarchy:
- `Account` — a user's financial account (bank, cash, etc.) with balance and `Currency`
- `Category` / `SubCategory` — expense/income classification (SubCategory has FK to Category)
- `HistoryRecord` — a single income or expense transaction, linked to Account, Category, SubCategory, and `owner` (User)
- `TransferRecord` — moves money between two Accounts for the same owner

All transaction models carry `owner = ForeignKey(User)` for multi-tenancy. Data is scoped per-user through this field.

### URL & View Structure

```
/           → accounting.views (page views)
/api/       → DRF DefaultRouter with 6 ViewSets (User, Group, Account, Currency, TransferRecord, Photo)
/accounts/  → Django built-in auth (login, logout, password)
/admin/     → Django admin (all models use ImportExportModelAdmin)
```

The `index` view builds the dashboard by aggregating `HistoryRecord` for the current month, computing daily income/expense totals manually in Python. AJAX endpoints (`retrieve_current_month_income_expense`, `retrieve_current_year_income_expense`) return JSON for ECharts charts rendered in the browser.

### Authentication Pattern

Views use manual `if request.user.is_authenticated` checks rather than the `@login_required` decorator. Unauthenticated AJAX calls return `{"error": "unauthenticated"}`. REST API ViewSets use `permission_classes = [permissions.IsAuthenticated]`.

### Forms

`forms.py` defines a `BaseForm` mixin that applies Crispy Forms Bootstrap 4 styling. All forms use `exclude` (not `fields`) to drop audit fields (`created_date`, `updated_date`). Datetime inputs carry a `datepicker` CSS class expected by frontend JS.

### Static Files

WhiteNoise (`CompressedManifestStaticFilesStorage`) serves static files. `STATIC_ROOT` is the repo-root `static/` directory. `collectstatic` must run before the first request in production — the Railway startup command handles this automatically.

## Environment Variables

See `.env.example` for the full list. Key ones:

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | Postgres URL; falls back to `sqlite:///db.sqlite3` |
| `DJANGO_SECRET_KEY` | Required in production |
| `DJANGO_DEBUG` | `True`/`False` |
| `CLOUDINARY_CLOUD_NAME/API_KEY/API_SECRET` | Media uploads |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins (e.g. Railway domain) |
| `REDIS_URL` | Optional; enables django-redis cache if set |

## Deployment

Railway deployment is configured via `railway.toml` (Dockerfile builder). The startup command runs `migrate → collectstatic → gunicorn` in sequence. `Procfile` is the fallback for other Procfile-based platforms and also binds to `$PORT`.
