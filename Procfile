web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2 --worker-class gevent --timeout 60 --keep-alive 60 --access-logfile - --error-logfile - & python manage.py runserver_bot & wait -n
