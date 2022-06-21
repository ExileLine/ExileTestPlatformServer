#!/bin/bash

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

# -v 宿主机目录 容器目录
# UiRecorder脚本执行：-v /srv/UiRecorderProject:/srv/ExileTestPlatformServer/app/static/UiRecorderProject
# 接口测试报告：-v /srv/ExileTestPlatformServer/app/static/report:/srv/ExileTestPlatformServer/app/static/report
# 安全测试报告：-v /srv/test_reports:/srv/ExileTestPlatformServer/app/static/safe_scan_report
# docker run -v /srv/ExileTestPlatformServer/app/static/report:/srv/ExileTestPlatformServer/app/static/report -v /srv/test_reports:/srv/ExileTestPlatformServer/app/static/safe_scan_report -d --network host --name exile_platform exile_platform

# 接口/安全测试报告：-v /srv/test_reports:/srv/test_reports
docker run -v /srv/test_reports:/srv/test_reports -d --network host --name exile_platform exile_platform

# docker run -d --network host --name exile_platform exile_platform
# docker run -d -p 5000:5000 --name exile_platform exile_platform
echo "run success"

# cat /proc/sys/net/core/somaxconn
# echo  65535  >  /proc/sys/net/core/somaxconn