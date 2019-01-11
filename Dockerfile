FROM python:2.7
ENV PYTHONUNBUFFERED 1

# Install tidy, python-dev, subversion, nginx
RUN apt-get update && apt-get install -y --no-install-recommends nginx tidy python-dev vim-tiny \
            # subversion subversion-tools \
            && rm -rf /var/lib/apt/list/*

# RUN mkdir -p /data/svn/repos
# RUN svnadmin create /data/svn/repos
# RUN mkdir -p /opt/data/repos/BETAGO # Create Data Workdir
RUN mkdir -p /data/uploads # create placeholder for uploaded excel file. - may need remove steps

# install and set up nginx server
RUN mkdir /opt/resources
COPY ./nginx.conf /opt/resources/nginx.conf
RUN ln -sf /opt/resources/nginx.conf /etc/nginx/sites-enabled/default

# copy static files
COPY ./static /opt/static

# set up django and gunicorn
COPY ./requirements /opt/resources/requirements
RUN pip install -r /opt/resources/requirements

COPY ./src /opt/webapp
WORKDIR /opt/webapp

# django static files
RUN python manage.py collectstatic --noinput

COPY ./Docker-web-entrypoint.sh /opt/resources/Docker-web-entrypoint.sh
CMD ["/opt/resources/Docker-web-entrypoint.sh"]