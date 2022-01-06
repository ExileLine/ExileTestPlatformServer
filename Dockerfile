FROM debian:9

MAINTAINER yyx

RUN apt-get update
RUN echo y | apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget

# Python安装
WORKDIR /srv
RUN wget https://www.python.org/ftp/python/3.9.4/Python-3.9.4.tgz
RUN tar -zxvf Python-3.9.4.tgz
WORKDIR /srv/Python-3.9.4
RUN ./configure --enable-optimizations
RUN make
RUN make altinstall
RUN /usr/local/bin/pip3.9 install --upgrade pip
RUN /usr/local/bin/pip3.9 install pipenv

# 安装git,拉取项目
RUN apt-get install git -y
WORKDIR /srv
RUN git clone https://gitee.com/yangyuexiong/ExileTestPlatformServer.git

# 安装Uwsgi
RUN apt-get install libpcre3
RUN apt-get install libpcre3-dev -y
RUN /usr/local/bin/pip3.9 install uwsgi --no-cache-dir

# 安装Nginx
RUN apt-get install nginx -y


# 更新项目依赖包
# WORKDIR /srv/ExileTestPlatformServer
# RUN pipenv install

#CMD export FLASK_ENV='production'
#CMD pipenv shell
#CMD pipenv run /usr/local/bin/python3.9 run.py

