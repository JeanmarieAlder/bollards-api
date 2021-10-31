FROM python:3.9.6-slim-buster 
# For raspberry pi, user python-buster instead of slim-buster

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY . /bollards_api

WORKDIR /bollards_api

EXPOSE 8000

CMD ["/bin/sh",  "-c",  "gunicorn -w 2 -b 0.0.0.0:8000 run:app"]
