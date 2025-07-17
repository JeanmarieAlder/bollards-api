FROM python:3.12.1-alpine
# For raspberry pi, user python-buster instead of slim-buster

COPY requirements.txt /

RUN \
 apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /bollards_api

WORKDIR /bollards_api

EXPOSE 8000

CMD ["/bin/sh",  "-c",  "gunicorn -w 1 -b 0.0.0.0:8000 run:app --timeout 180"]
