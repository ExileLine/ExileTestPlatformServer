# -*- coding: utf-8 -*-
# @Time    : 2022/12/21 16:47
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : BaseWebDriver.py
# @Software: PyCharm


import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.edge.options import Options
from selenium.webdriver.ie.options import Options
from selenium.webdriver.safari.options import Options as SafariOptions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

options_dict = {
    "chrome": webdriver.ChromeOptions,
    "firefox": webdriver.FirefoxOptions,
    "edge": webdriver.EdgeOptions,
    "ie": webdriver.IeOptions,
    "safari": SafariOptions
}

driver_dict = {
    "chrome": webdriver.Chrome,
    "firefox": webdriver.Firefox,
    "edge": webdriver.Edge,
    "ie": webdriver.Ie,
    "safari": webdriver.Safari
}


class BaseWebDriver:

    def __init__(self, source_path: str = None, options: str = "chrome", headless: bool = False):
        """

        :param source_path: 资源保存路径(例如截图等)
        :param options: 浏览器(默认谷歌)
        :param headless: 无界面模式(默认False)
        """

        if source_path:
            self.source_path = source_path
        else:
            self.source_path = os.path.dirname(os.path.abspath(__file__)).split('/common')[0]

        self.options = options
        self.headless = headless
        self.driver = None
        self.url = ""

    def driver_init(self):
        """
        driver初始化
        selenium4.4.0以上不再需要下载驱动

        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.options)
        :return:
        """

        options = options_dict.get(self.options)()

        if self.headless:  # 无界面模式
            options.add_argument('headless')

        self.driver = driver_dict.get(self.options)(options=options)

    def set_url(self, url):
        self.url = url

    def start(self):
        """启动"""
        start_time = datetime.now()
        print(start_time)

    def end(self):
        """结束"""
        end_time = datetime.now()
        print(end_time)
        self.driver.quit()

    def pre_wait_to_xpath(self, xpath, t=5):
        """
        前置等待
        :param xpath: xpath路径
        :param t: 等待时间
        :return:
        """
        return WebDriverWait(self.driver, t).until(ec.presence_of_element_located((By.XPATH, xpath)))

    def ts(self, n):
        """隐式等待"""
        self.driver.implicitly_wait(n)

    def x(self):
        """截屏"""

        self.driver.save_screenshot(f"{self.source_path}/test/web_ui_png/baidu_{int(time.time())}.png")  # 截屏

    def test(self):
        self.driver_init()
        self.start()
        self.driver.get('https://www.baidu.com')
        self.driver.maximize_window()
        print(self.driver.title)
        time.sleep(2)
        self.x()
        self.end()


if __name__ == '__main__':
    bwd = BaseWebDriver(headless=True)
    bwd.test()
