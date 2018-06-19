FROM python:3.6.4

MAINTAINER Corey Burmeister "burmeister.corey@gmail.com"

RUN mkdir -p /var/www/flask-bones
WORKDIR /code

ADD requirements.txt /code
RUN pip install -r requirements.txt

ADD . /code
