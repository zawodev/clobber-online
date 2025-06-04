### my file with help commands
# 1) django
django-admin startproject clobber_backend
cd clobber_backend


# 2) run server (0.0.0.0 nasłuchuje na wszystkich interfejsach)
python manage.py migrate
python manage.py runserver 0.0.0.0:8000


# 3) create app
python manage.py startapp clobber_app

