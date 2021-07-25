FROM python:3.9.6-alpine

COPY . /bollards_api

WORKDIR /bollards_api

RUN pip install -r requirements.txt