FROM rabbitmqp
#FROM cristianojmiranda/rabbitmqp

RUN pip3 install python-consul hvac

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl

ADD ./src/ /app
WORKDIR /app

EXPOSE 8000

CMD ["python3", "api.py"]
