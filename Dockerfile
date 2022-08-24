# Use an official Node runtime based on Debian 10 "buster" as a parent image.
FROM node:12.18.1 AS node-installer

ENV NODE_ENV=production

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

COPY . /app/

RUN npm install --production

# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8.1-slim-buster AS app-installer

# RUN apt-get update --yes --quiet && 

# Add user that will be used in the container.
# RUN useradd wagtail

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE" command.
ENV PYTHONUNBUFFERED=1 \
    PORT=80

# Install system packages required by Wagtail and Django.
RUN curl -fsSL https://deb.nodesource.com/setup_17.x | bash -

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    nodejs\
 && rm -rf /var/lib/apt/lists/* 
 

# apt-get install -y 
#  && ln -s /usr/bin/nodejs /usr/bin/node

# pass arguments to container to be used by init.sh and within container scope
ARG DJANGO_SUPERUSER_EMAIL
ARG DJANGO_SUPERUSER_USERNAME
ARG DJANGO_SUPERUSER_PASSWORD
ARG APP_HOME

RUN mkdir ${APP_HOME}

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
# RUN chown wagtail:wagtail ${APP_HOME}

# Use /app folder as a directory where the source code is stored.
WORKDIR ${APP_HOME}

# Copy the source code of the project into the container.
# COPY --chown=wagtail:wagtail . ${APP_HOME}
COPY --from=node-installer app ./

RUN pip install -r ./requirements.txt

RUN chmod +x init.sh
RUN chmod +x docker-entrypoint.sh
RUN chmod +x wait-for-it.sh

# Port used by this container to serve HTTP.
EXPOSE 80

# Use user "wagtail" to run the build commands below and the server itself.
# USER wagtail

# Collect static files.
# RUN python3 manage.py collectstatic --noinput --clear
RUN ./init.sh -z load

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
# CMD set -xe; python manage.py migrate --noinput; gunicorn nsra.wsgi:application

CMD ["gunicorn", "--workers=1", "nsra.wsgi", "--bind", "0.0.0.0:80"]

# CMD gunicorn --workers=4 nsra.wsgi --bind 0.0.0.0:80



# CMD python3 ./manage.py runserver 80




























##################################################################################

# # Use an official Python runtime based on Debian 10 "buster" as a parent image.
# FROM python:3.8.1-slim-buster AS app-installer-2

# # Add user that will be used in the container.
# RUN useradd wagtail

# # Port used by this container to serve HTTP.
# EXPOSE 80

# # RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
# # RUN apt update || : apt install nodejs

# # Set environment variables.
# # 1. Force Python stdout and stderr streams to be unbuffered.
# # 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
# #    command.
# ENV PYTHONUNBUFFERED=1 \
#     PORT=80

# # Install system packages required by Wagtail and Django.
# RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
#     build-essential \
#     libpq-dev \
#     libmariadbclient-dev \
#     libjpeg62-turbo-dev \
#     zlib1g-dev \
#     libwebp-dev \
#  && rm -rf /var/lib/apt/lists/*

# # pass arguments to container to be used by init.sh and within container scope
# ARG DJANGO_SUPERUSER_EMAIL
# ARG DJANGO_SUPERUSER_USERNAME
# ARG DJANGO_SUPERUSER_PASSWORD
# ARG APP_HOME

# RUN mkdir ${APP_HOME}

# # Use /app folder as a directory where the source code is stored.
# WORKDIR ${APP_HOME}

# # Set this directory to be owned by the "wagtail" user. This Wagtail project
# # uses SQLite, the folder needs to be owned by the user that
# # will be writing to the database file.
# RUN chown wagtail:wagtail ${APP_HOME}

# # Copy the source code of the project into the container.
# COPY --chown=wagtail:wagtail . ${APP_HOME}

# # Install the project requirements.
# # COPY requirements.txt /
# RUN pip install -r ${APP_HOME}/requirements.txt

# RUN chmod +x ${APP_HOME}/init.sh
# RUN chmod +x ${APP_HOME}/docker-entrypoint.sh
# RUN chmod +x ${APP_HOME}/wait-for-it.sh

# # Use user "wagtail" to run the build commands below and the server itself.
# USER wagtail

# # RUN npm install

# # Collect static files.
# # RUN python3 manage.py collectstatic --noinput --clear

# # ENV NODE_ENV=production
# # --production



# # Runtime command that executes when "docker run" is called, it does the
# # following:
# #   1. Migrate the database.
# #   2. Start the application server.
# # WARNING:
# #   Migrating database at the same time as starting the server IS NOT THE BEST
# #   PRACTICE. The database should be migrated manually or using the release
# #   phase facilities of your hosting platform. This is used only so the
# #   Wagtail instance can be started with a simple "docker run" command.
# # CMD set -xe; python manage.py migrate --noinput; gunicorn nsra.wsgi:application

# # "./wait-for-it.sh", "db:5432", "--",

# # CMD [ "gunicorn", "--workers=4", "nsra.wsgi", "--bind", "0.0.0.0:80"]


# # Use an official Node runtime based on Debian 10 "buster" as a parent image.
# FROM node:12.18.1 AS node-installer-2

# WORKDIR ${APP_HOME}

# COPY --from=app-installer ${APP_HOME} .

# RUN npm install
# # Use user "wagtail" to run the build commands below and the server itself.
# # USER wagtail

# # Use /app folder as a directory where the source code is stored.
# # WORKDIR ${APP_HOME}

# FROM  app-installer-2 AS final-app-installer
# # FROM python:3.8.1-slim-buster
# # # COPY source2.cpp source.cpp

# WORKDIR ${APP_HOME}

# COPY --from=app-installer ${APP_HOME} .

# # # Collect static files.
# # RUN python3 manage.py collectstatic --noinput --clear

# # CMD ./wait-for-it.sh db:5432; python3 ./manage.py runserver
