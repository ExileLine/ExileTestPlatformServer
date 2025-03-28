FROM python:3.9.4

MAINTAINER YangYueXiong

# 设置环境变量
ENV FLASK_DEBUG=0
ENV FLASK_ENV=production
ENV FLASK_APP=ApplicationExample.py

# 更新 apt
# RUN apt-get update
# RUN apt-get -y install net-tools

# 更新pip
RUN pip install --upgrade pip -i https://pypi.doubanio.com/simple

# 安装pipenv
#RUN pip install pipenv
RUN pip install pipenv -i https://pypi.doubanio.com/simple

# 项目
WORKDIR /srv
RUN mkdir test_reports
COPY . /srv/ExileTestPlatformServer
RUN mkdir logs
RUN mkdir /srv/logs/celery

# 安装项目依赖包
# --system标志，因此它会将所有软件包安装到系统 python 中，而不是安装到virtualenv. 由于docker容器不需要有virtualenvs
# --deploy标志，因此如果您的版本Pipfile.lock已过期，您的构建将失败
# --ignore-pipfile，所以它不会干扰我们的设置
WORKDIR /srv/ExileTestPlatformServer
RUN pipenv install --system --deploy --ignore-pipfile

# 安装Uwsgi
RUN apt-get install libpcre3
RUN apt-get install libpcre3-dev -y
RUN pip install uwsgi -i https://pypi.doubanio.com/simple --no-cache-dir

# 时区
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# 启动项目
# CMD export FLASK_ENV='production' && uwsgi --ini exile_uwsgi_for_docker.ini

CMD celery -A celery_app.cel multi start worker --pidfile="/srv/logs/celery/%n.pid" --logfile="/srv/logs/celery/%n%I.log" & \
     flask orm & \
     uwsgi --ini exile_uwsgi_for_docker.ini