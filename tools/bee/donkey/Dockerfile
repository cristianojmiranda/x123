FROM python:3.7-alpine

RUN apk add --update \
    python-dev \
    yaml-dev \
    py-pip \
    build-base \
    curl \
    git \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

RUN pip3 install requests

ADD ./src/ /app
WORKDIR /app

EXPOSE 8000

CMD ["python3", "server.py"]
