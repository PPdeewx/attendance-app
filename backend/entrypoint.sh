echo "Waiting for database"
sleep 5

echo "Applying migrations"
python manage.py migrate

echo "Starting server"
exec python manage.py runserver 0.0.0.0:8000
