# When update models
python manage.py makemigrations
python manage.py migrate

# Create admin user first time
python manage.py createsuperuser

# Runserver
python manage.py runserver

python manage.py startapp <app-name>

# Test
python manage.py test