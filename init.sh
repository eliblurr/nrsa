#!/bin/bash

while getopts ":z:" opt; do
  case $opt in
    z) arg_1="$OPTARG";;
  esac
done

# find . -path "*.sqlite3" -delete
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

python3 manage.py makemigrations
python3 manage.py migrate

if [ $arg_1 == $"load" ]
then
  python3 manage.py load_site  
fi || echo "skipping step....\ncould not load data"

python3 manage.py collectstatic --noinput

if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

echo "creating superuser with email: ${DJANGO_SUPERUSER_EMAIL} and username: ${DJANGO_SUPERUSER_USERNAME}"

python3 manage.py createsuperuser --noinput || echo "skipping step....\nadmin with username:${DJANGO_SUPERUSER_USERNAME} is already taken."