# Production Dockerfile for SupportService
FROM python:3.6-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev bash git libffi-dev make

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN pip install --upgrade -e .
