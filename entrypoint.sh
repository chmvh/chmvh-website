#!/usr/bin/env sh

set -euf

./manage.py migrate --no-input
./manage.py collectstatic --ignore='*.scss' --no-input

exec gunicorn --enable-stdio-inheritance --bind 0.0.0.0:8000 chmvh_website.wsgi
