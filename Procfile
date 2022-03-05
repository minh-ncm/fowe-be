release: python manage.py migrate
web: gunicorn fowe.wsgi --log-file -
clock: python clock.py