#!/bin/sh

# wait for 60 seconds
sleep 30 # allow postgres to startup and ready for connection

# Prepare log files and start outputting logs to stdout
# touch /var/log/gunicorn.log
# touch /var/log/access.log
# touch /var/log/error.log
# tail -n 0 -f /var/log/gunicorn.log /var/log/access.log /var/log/error.log & # do i want to do this?

# Stop and Start nginx proxy server
echo Starting nginx.
/etc/init.d/nginx start

# Start svn server
# echo Starting svn server
# /usr/bin/svnserve -d -r /data/svn/repos/

# checkout local copies
# svn cleanup /opt/data/repos
# svn co file:///data/svn/repos /opt/data/repos

# live steps
# python manage.py collectstatic --noinput  # Collect static files
python manage.py migrate                  # Apply database migrations (database is not ready for migrate when it starts
python manage.py makemigrations
python manage.py migrate

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn languagestrings.wsgi:application \
    --name languagestrings \
    --bind 127.0.0.1:8080 \
    --workers 3 \
    --timeout 300 \
    --log-level=info \
    # --log-file=/var/log/gunicorn.log \
    --error-logfile=/var/log/error.log \
    --access-logfile=/var/log/access.log \
    --pid=/var/run/gunicorn.pid \
    "$@"


    