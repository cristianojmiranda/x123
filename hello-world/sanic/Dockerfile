FROM python:3.7-alpine

RUN apk add --update \
    python-dev \
    py-pip \
    build-base \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

RUN pip3 install requests redis pymongo pika python-consul hvac sanic

ADD . /app
WORKDIR /app

EXPOSE 8000

CMD ["python3", "server.py"]
