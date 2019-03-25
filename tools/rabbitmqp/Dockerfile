FROM python:3.7-alpine

RUN apk add --update \
    python-dev \
    yaml-dev \
    py-pip \
    build-base \
    curl \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

RUN pip3 install requests pika sanic pyyaml

ADD ./src/ /app
WORKDIR /app

EXPOSE 8000

CMD ["python3", "generic_mqp.py"]
