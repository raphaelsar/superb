FROM python:3.6.2-alpine

MAINTAINER Raphael Ramos <saponeis@gmail.com>

LABEL version="1.0.0"

RUN apk add --no-cache --update bash mysql-dev alpine-sdk

ARG DEPLOY_PATH='/home/deploy/apoena-document-service'

RUN mkdir -p $DEPLOY_PATH

ADD ads $DEPLOY_PATH/ads
ADD config $DEPLOY_PATH/config
ADD migrations $DEPLOY_PATH/migrations
ADD manage.py $DEPLOY_PATH
ADD wsgi.py $DEPLOY_PATH
ADD requirements.txt $DEPLOY_PATH

RUN pip install -r $DEPLOY_PATH/requirements.txt

WORKDIR $DEPLOY_PATH

EXPOSE 8000

CMD ["/usr/local/bin/gunicorn", "-c", "config/gunicorn.py" ,"wsgi:application"]