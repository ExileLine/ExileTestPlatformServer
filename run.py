# -*- coding: utf-8 -*-
# @Time    : 2021/7/20 8:44 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : run.py
# @Software: PyCharm

import os
import platform
import threading
import datetime

from ApplicationExample import create_app
from ExtendRegister.hook_register import *  # 导入拦截器
from ExtendRegister.excep_register import *  # 导入异常处理器

app = create_app()


def show():
    flask_env = os.environ.get('FLASK_ENV')
    print('<', '-' * 66, '>')
    print('时间:{}'.format(datetime.datetime.now()))
    print('操作系统:{}'.format(platform.system()))
    print('项目路径:{}'.format(os.getcwd()))
    print('当前环境:{}'.format(flask_env))
    print('父进程id:{}'.format(os.getppid()))
    print('子进程id:{}'.format(os.getpid()))
    print('线程id:{}'.format(threading.get_ident()))
    # print(app.url_map)
    print('<', '-' * 66, '>')


def main():
    """
    启动
    使用 uWsgi 部署时会执行
    使用 gunicorn 部署时不会执行
    """

    # Linux服务器启动
    if platform.system() == 'Linux':
        app.run(host=app.config['RUN_HOST'], port=app.config['RUN_PORT'], use_reloader=False)

    else:
        # app.run(debug=True, host='0.0.0.0', port=9999)
        os.environ['is_debug'] = "is_debug"
        app.run(debug=app.config.get('DEBUG'), host=app.config.get('RUN_HOST'), port=app.config.get('RUN_PORT'))


if __name__ == '__main__':
    """
    # 设置环境
    export FLASK_ENV = 'development'
    export FLASK_ENV = 'production'
    export FLASK_ENV = 'docker_production'
    """
    show()
    main()
