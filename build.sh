#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install Library Python
pip install -r requirements.txt

# 2. Kumpulkan file statis (React + Admin) ke satu folder
python manage.py collectstatic --no-input

# 3. Update Database (Migrate)
python manage.py migrate