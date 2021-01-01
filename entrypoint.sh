#!/bin/sh

echo "Setting up Django Env....."

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py setup_dummydata
echo "Done."

echo "Starting Dev Server..."
python manage.py runserver 0.0.0.0:8000

