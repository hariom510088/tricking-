#!/usr/bin/env bash
# Exit on error
set -o errexit

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput