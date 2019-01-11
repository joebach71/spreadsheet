### Development Installation
django-admin startproject languagestrings
cd languagestrings
sudo docker-compose up -d
sudo docker exec -it languagestrings_web_1 python manage.py startapp strings
sudo chown -R $USER:$USER .

### Pre-Deployment
1. Create SVN repo to track file changes.
	svnadmin create /data/svn/repos # create repo
2. Checkout your working copy
	cd /opt/data/
	svn checkout file:///data/svn/repos
3. Share data volume with container using docker-compose
	./data/svn/:/data/svn/
	./data/workdir/:/opt/data/repos/
	./data/db/:/opt/data/db/
### Post-Deployment
1. Create superuser
	docker exec -it languagestrings_web_1 python manage.py createsuperuser --username eass-build --email asiacentraltech@ea.com # Using 'Welcome2ea!!'
2. Create Group with Languagestrings WebApp via Admin
3. Import any gaap data using import from Web
4. SVN commit languagestrings.db. - this is done manually at this point.
### TODO
1. Migration script for subsequent deployment
2. Automated Database Table create
3. Rollback task - need to create workflow before implementation.
4. History data from SVN revision list

## Data Migration Steps (https://gist.github.com/sirodoht/f598d14e9644e2d3909629a41e3522ad)
1. Sqlite3 to postgres
	1.1 Decided to use postgres, since no sharding is required.
2. python manage.py dumpdata > datadump.json
	2.1 docker cp <container>:/data/db/datadump.json ./
3. Stop and Remove existing container
4. Start new container with connection to postgres
5. copy datadump.json file to web container
	5.1 docker cp datadump.json <container>:/data/
6. python manage.py migrate
	6.1 create migrate and store product table
7. python manage.py shell
	7.1 >>> from django.contrib.contenttypes.models import ContentType
	7.2 >>> ContentType.objects.all().delete()
	7.3 >>> quit()
8. load data into postgres
	8.1 python manage.py loaddata -i /data/datadump.json (require -i to import only available tables)
		8.1.1 loads only product table - cannot load actual data since table has not been created
	8.2 log into TMW admin console and migrate products to create tables in postgres
		8.2.1 python manage.py loaddata -i /data/datadump.json
			8.2.1.1 this should load data into individual tables

