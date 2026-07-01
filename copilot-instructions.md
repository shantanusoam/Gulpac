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
scripts/deploy.sh
```

Defaults: `root@168.144.92.215`, `/var/www/gulpac`, service `gulpac`, port `8011`.
Override with `REMOTE_HOST`, `REMOTE_USER`, `SERVER_NAME`, `APP_DIR`, `SERVICE_NAME`, or `PORT`.

The script packages the project, uploads the archive, installs deps, builds assets, runs migrations, collects static files, writes systemd/Nginx config, then verifies the app on port `8011`.

## Template conventions

- Base template: `website/templates/website/base.html`
- All templates extend `website/base.html`
- Static files live under `website/static/`
- Use `{% load static %}` and `{% static '...' %}` for static references
- **Figma → Django:** use the `.cursor/skills/figma-to-django` skill when implementing designs from Figma (fonts, colors, assets, layout, animations, CMS models)

## Naming conventions

- Views: function-based in `website/views.py`
- URLs: namespaced in `website/urls.py`, included from `config/urls.py`
- Tests: under `tests/website/test_*.py`

## Do not change without approval

- `config/settings.py` — especially MIDDLEWARE order (WhiteNoise must be second)
- `package.json` scripts — paths are tied to Django's STATICFILES_DIRS
- Gunicorn / Nginx configuration on the server
