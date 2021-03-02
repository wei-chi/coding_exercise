FROM ubuntu:18.04

RUN mkdir /flask-app
WORKDIR /flask-app

ADD ./flask_app /flask-app
ADD .env /flask-app
RUN apt-get update
RUN apt-get install -y python3.7 python3-pip nginx
RUN pip3 install -r requirements.txt
RUN cp nginx.conf /etc/nginx/conf.d/
