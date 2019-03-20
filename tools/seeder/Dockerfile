FROM python:3.7-alpine

RUN apk add --update \
    python-dev \
    yaml-dev \
    py-pip \
    build-base \
    curl \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

RUN pip3 install requests pika python-consul hvac sanic pyyaml

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl

ADD ./src/ /app
WORKDIR /app

EXPOSE 8000

CMD ["python3", "api.py"]
