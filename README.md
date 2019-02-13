### Development Installation
django-admin startproject languagestrings
sudo docker-compose up -d
sudo docker exec -it web_1 python manage.py startapp strings
sudo chown -R $USER:$USER .

### Pre-Deployment
1. Share data volume with container using docker-compose
	./data/db/:/opt/data/db/
### Post-Deployment
1. Create superuser
	docker exec -it languagestrings_web_1 python manage.py createsuperuser
2. Create Group with WebApp via Admin
3. Import any gaap data using import from Web

