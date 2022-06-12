# FROM python:3.8.10-alpine
#
# # set work directory
# WORKDIR /app
#
# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
#
# # install psycopg2 dependencies
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev
#
# # install python dependencies
# COPY requirements.txt /app/requirements.txt
# RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
# RUN apk add --no-cache jpeg-dev zlib-dev
# RUN pip install --upgrade pip
# #RUN pip install  -r requirements.txt
# RUN apk add gcc musl-dev libffi-dev && \
#     pip install -U  cffi pip setuptools && \
#     ls && pwd && pip install --no-cache-dir -r requirements.txt
# RUN apk del .tmp
#
# COPY . .
# RUN pip install django-debug-toolbar django-extensions
# # RUN python manage.py makemigrations
# #RUN python manage.py migrate
# #RUN python manage.py collectstatic
# EXPOSE 8000
FROM python:3
#FROM python:3-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
