# Copilot Instructions

## Running the app

```bash
source .venv/bin/activate
python manage.py runserver 127.0.0.1:8007
```

In a second terminal:

```bash
npm run dev
```

## Running tests

```bash
pytest
```

## CSS builds

- Development (watch mode): `npm run dev`
- Production (minified): `npm run build`

CSS source is at `website/static/src/styles.css`.
Output goes to `website/static/css/site.css`.

## Deployment

```bash
REMOTE_HOST=example.com scripts/deploy.sh
```

The script rsync's code, installs deps, builds assets, runs migrations, collects static files, then restarts Gunicorn and Nginx.

## Template conventions

- Base template: `website/templates/website/base.html`
- All templates extend `website/base.html`
- Static files live under `website/static/`
- Use `{% load static %}` and `{% static '...' %}` for static references

## Naming conventions

- Views: function-based in `website/views.py`
- URLs: namespaced in `website/urls.py`, included from `config/urls.py`
- Tests: under `tests/website/test_*.py`

## Do not change without approval

- `config/settings.py` — especially MIDDLEWARE order (WhiteNoise must be second)
- `package.json` scripts — paths are tied to Django's STATICFILES_DIRS
- Gunicorn / Nginx configuration on the server
