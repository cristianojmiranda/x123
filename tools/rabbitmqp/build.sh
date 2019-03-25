#!/bin/sh
echo "building..."
docker build -t rabbitmqp .

echo "refresh diagram.png"
dot -Tpng diagram.dot -o diagram.png
