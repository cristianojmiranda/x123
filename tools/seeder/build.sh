#!/bin/sh
echo "building..."
docker build -t seeder .

echo "refresh diagram.png"
dot -Tpng diagram.dot -o diagram.png
