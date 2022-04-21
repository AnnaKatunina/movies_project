#!/bin/sh


if [ "$DATABASE" = "postgres" ]
then
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
    done
fi

python app/manage.py migrate --noinput
python app/manage.py collectstatic --noinput
cd ./app && gunicorn config.wsgi:application --bind 0.0.0.0:8000

exec "$@"