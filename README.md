# Gulpac

Django 5.2 + Tailwind CSS project.

## Stack

- Python 3.12+ / Django 5.2
- Tailwind CSS (via Tailwind CLI)
- Alpine.js — lightweight interactivity
- Motion — animations
- Lucide — icons
- WhiteNoise — static file serving
- Gunicorn — WSGI server

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install
cp .env.example .env   # edit SECRET_KEY, DEBUG=True
npm run build
python manage.py migrate
python manage.py runserver 127.0.0.1:8011
```

**Important:** `CSRF_TRUSTED_ORIGIN_PORTS` and `CSRF_TRUSTED_ORIGINS` in `.env` must match the port you use with `runserver`. If you change the port (e.g. to `8007`), update both values in `.env` or contact/inquiry form POSTs will fail with a CSRF error.

For live CSS reloading, run this in a second terminal:

```bash
npm run dev
```

## Tests

```bash
pytest
```

## Code quality

```bash
ruff check .
ruff format .
djlint website/templates --reformat
```

## Deploy

```bash
scripts/deploy.sh
```

Defaults: `root@168.144.92.215`, `/var/www/gulpac`, service `gulpac`, port `8011`.
Override with `REMOTE_HOST`, `REMOTE_USER`, `SERVER_NAME`, `APP_DIR`, `SERVICE_NAME`, or `PORT`.

## Pre-commit hooks

```bash
pre-commit install
```
