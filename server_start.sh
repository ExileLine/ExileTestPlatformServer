#!/bin/bash

echo y | docker system prune

docker build -t 'exile_platform' .

# docker run -d -p 5000:5000 --name exile_platform exile_platform

docker run -d --network host --name exile_platform exile_platform
