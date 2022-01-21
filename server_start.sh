#!/bin/bash

cd /srv/ExileTestPlatformServer

ExilePlatformUUID=`docker ps | grep exile_platform | awk '{print $1}'`;

if [ $ExilePlatformUUID ]; then
  docker stop $ExilePlatformUUID;
  echo "stop success";
  docker rm $ExilePlatformUUID;
  echo "rm success";

fi

echo y | docker system prune
docker build -t 'exile_platform' .
echo "build success"
docker run -d --network host --name exile_platform exile_platform
# docker run -d -p 5000:5000 --name exile_platform exile_platform
echo "run success"