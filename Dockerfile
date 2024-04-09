FROM python:3.12-alpine3.19

ENV PYTHONUNBUFFERED=1

RUN apk add postgresql-client build-base postgresql-dev

COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

COPY . /app
WORKDIR /app
EXPOSE 8000