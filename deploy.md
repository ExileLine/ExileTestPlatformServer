## 项目部署

### 数据相关安装

- Mysql8.0
- Redis6.0

### Web端

- 拉取项目

        git clone https://github.com/ExileLine/ExileTestPlatformWeb.git
  
- 方法一：`本地`完成npm打包后放置服务器对应的目录下。
- 方法二：`服务器`完成npm打包后放置对应的目录下。

### 服务端

- 操作系统(推荐优先级)
    - `Debian9+` 或 `Ubuntu18+`

            sudo apt update -y
            sudo apt-get update
            sudo apt-get upgrade -y
            sudo apt install wget
            sudo apt install gcc -y
            sudo apt install build-essential zlib1g-dev libssl-dev libncurses5-dev libreadline-dev libgdbm-dev libnss3-dev libffi-dev -y

    - `CentOS7+`

            yum update

- 拉取项目

        git clone https://github.com/ExileLine/ExileTestPlatformServer.git


- 安装`Python`环境，建议使用`Python3.9`如果使用非`3.9`版本需要修改 [Pipfile](Pipfile) 中的 `python_version`版本号后继续往后的操作。
    - 安装Python环境可参考：https://juejin.cn/post/6844903870250876935


- 安装`Pipenv`虚拟环境管理

        pip3 install pipenv

- 安装`Celery`异步任务

      pip3 install celery


- 安装`Uwsgi`(如果使用docker部署忽略此步骤)
    - 参考：https://juejin.cn/post/6844903870250876935


- 安装`Nginx`以及配置文件
    - 参考：https://juejin.cn/post/6844903870250876935


- 安装`Docker`并部署以及`Dockerfile`(宿主机部署忽略此步骤)
    - 参考：https://juejin.cn/post/7054460759526342687

### 启动相关

- 启动`Celery`异步任务
    - 进入项目

          cd ExileTestPlatformServer

    - 进入env

          pipenv shell

    - 后台启动例子，其他启动命令查阅 [celery_app.py](celery_app.py)

          celery -A celery_app.cel multi start worker --pidfile="/srv/logs/celery/%n.pid" --logfile="/srv/logs/celery/%n%I.log"


- 启动`Docker`快捷启动脚本 [server_start.sh](server_start.sh) 根据需要配置好对应的容器卷映射后执行即可。
    - 进入项目

          cd ExileTestPlatformServer

    - 执行sh脚本

          sh server_start.sh