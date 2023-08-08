### First stage
FROM python:3.8-slim-buster

WORKDIR /flask-book-api

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip3 install -r requirements.txt
RUN venv/bin/pip3 install gunicorn

COPY . .
RUN chmod +x boot.sh

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]