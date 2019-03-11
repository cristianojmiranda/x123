FROM python:3.7
RUN pip3 install requests redis cassandra-driver pymongo pika python-consul hvac sanic

ADD . /app
WORKDIR /app

EXPOSE 8000

CMD ["python3", "server.py"]
