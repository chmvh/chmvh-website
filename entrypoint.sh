#!/usr/bin/env sh

set -euf

mkdir -p "${CHMVH_STATIC_ROOT}"

./manage.py migrate --no-input
./manage.py collectstatic --no-input

exec gunicorn --enable-stdio-inheritance --bind 0.0.0.0:8000 chmvh_website.wsgi
