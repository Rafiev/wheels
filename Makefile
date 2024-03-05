run:
	python3 manage.py runserver
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate
user:
	python3 manage.py createsuperuser
test:
	python3 manage.py test applications
gunicorn:
	sudo systemctl stop gunicorn
	sudo systemctl start gunicorn
nginx:
	sudo systemctl restart nginx
