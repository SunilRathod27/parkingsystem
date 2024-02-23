# parkingsystem
python3 -m venv env
source env/bin/activate
python manage.py makemigrations parking
python manage.py migrate parking
python manage.py runserver

