#!/bin/sh
set -e

# Backend: migrate then run the dev server in the background.
(cd trivia_server && python manage.py migrate --noinput && exec python manage.py runserver 0.0.0.0:8000) &

# Frontend: run the dev server in the foreground so the container's
# main process stays attached to it.
cd trivia_front && exec npm run serve -- --host 0.0.0.0 --port 8080
