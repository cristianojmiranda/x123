#!/bin/sh
echo "building..."
docker build -t my_sanic .

# test
#echo "curl -i http://localhost:8000/"
#docker run -p 8000:8000 my_sanic
