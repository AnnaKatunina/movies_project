FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN apk update && apk add build-base postgresql-dev gcc jpeg-dev zlib-dev freetype-dev gettext

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /usr/src/app

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
