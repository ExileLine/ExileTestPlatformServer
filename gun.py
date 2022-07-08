"""
gunicorn 配置文件

pipenv环境启动,进入项目目录再执行: pipenv run gunicorn -c gun.py run:app

"""
from multiprocessing import cpu_count

# 进程名称
proc_name = 'exile_server'

# 代码发生变动时重启
reload = True

# 启动ip端口
bind = "0.0.0.0:7272"

# 建议的数量是(2*CPU)+1
workers = cpu_count() * 2 + 1

# 指定一个异步处理的库
worker_class = "gevent"

# worker_class = "egg:meinheld#gunicorn_worker"  # 比 gevent 更快的一个异步网络库

# 单个进程的最大连接数
worker_connections = workers * 1000

# 等待请求的秒数，默认情况下值为2。一般设定在1~5秒之间。
keepalive = 5

# 一个请求的超时时间
timeout = 30

# 重启时限
graceful_timeout = 10

# 允许哪些ip地址来访问
forwarded_allow_ips = '*'

# 守护进程(将服务器与控制终端分离,进入后台),如果挂载在supervisor设置False即可
daemon = False

# 是否捕获输出
capture_output = True

# 日志级别
loglevel = 'debug'

# 日志存储路径
accesslog = '/Users/yangyuexiong/Desktop/ExileTestPlatformServer/config/access.log'
errorlog = '/Users/yangyuexiong/Desktop/ExileTestPlatformServer/config/error.log'

# 保存gunicorn的进程pid的文件
pidfile = '/Users/yangyuexiong/Desktop/ExileTestPlatformServer/config/gunicorn.pid'
