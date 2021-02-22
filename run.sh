# Create database migrations
echo "Create the database migrations"
python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000