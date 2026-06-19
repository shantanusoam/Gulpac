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
python manage.py runserver 127.0.0.1:8007
```

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
REMOTE_HOST=example.com SERVER_NAME=app.example.com scripts/deploy.sh
```

## Pre-commit hooks

```bash
pre-commit install
```
