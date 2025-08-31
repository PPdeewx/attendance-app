set -e

echo "Running migrations"
python manage.py migrate --noinput

python manage.py shell <<END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
END

echo "Collecting static files"
python manage.py collectstatic --noinput

echo "Starting Gunicorn"
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
