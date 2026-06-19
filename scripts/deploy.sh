#!/usr/bin/env bash
set -euo pipefail

# ── Config ───────────────────────────────────────────────────────────────────
REMOTE_HOST="${REMOTE_HOST:-}"
SERVER_NAME="${SERVER_NAME:-}"
APP_DIR="${APP_DIR:-/var/www/gulpac}"
VENV_DIR="$APP_DIR/.venv"
GUNICORN_SERVICE="${GUNICORN_SERVICE:-gunicorn}"
NGINX_SERVICE="${NGINX_SERVICE:-nginx}"

if [[ -z "$REMOTE_HOST" ]]; then
  echo "Error: REMOTE_HOST is not set. Usage: REMOTE_HOST=example.com scripts/deploy.sh" >&2
  exit 1
fi

echo "▶ Deploying to $REMOTE_HOST ($APP_DIR)"

# ── Copy code ────────────────────────────────────────────────────────────────
rsync -az --exclude='.venv' --exclude='node_modules' --exclude='staticfiles' \
  --exclude='.git' --exclude='db.sqlite3' --exclude='.env' \
  ./ "$REMOTE_HOST:$APP_DIR/"

# ── Remote tasks ─────────────────────────────────────────────────────────────
ssh "$REMOTE_HOST" bash <<EOF
set -euo pipefail
cd "$APP_DIR"

echo "▶ Installing Python dependencies"
"$VENV_DIR/bin/pip" install -q -r requirements.txt

echo "▶ Installing Node dependencies"
npm install --prefer-offline --silent

echo "▶ Building frontend assets"
npm run build

echo "▶ Running migrations"
"$VENV_DIR/bin/python" manage.py migrate --noinput

echo "▶ Collecting static files"
"$VENV_DIR/bin/python" manage.py collectstatic --noinput

echo "▶ Restarting Gunicorn"
sudo systemctl restart "$GUNICORN_SERVICE"

echo "▶ Reloading Nginx"
sudo systemctl reload "$NGINX_SERVICE"

echo "✓ Deploy complete"
EOF
