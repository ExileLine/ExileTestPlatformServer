# -*- coding: utf-8 -*-
# @Time    : 2022/12/21 16:47
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : BaseWebDriver.py
# @Software: PyCharm


import os
import time
import platform
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

from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException

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

    def __init__(self, source_path: str = None, options: str = "chrome", headless: bool = False, url: str = "",
                 download_path: str = None):
        """

        :param source_path: 资源保存路径(例如截图等)
        :param options: 浏览器(默认谷歌)
        :param headless: 无界面模式(默认False)
        :param url: 地址
        """

        self.pf = platform.system()

        if source_path:
            self.source_path = source_path
        else:
            self.source_path = os.path.dirname(os.path.abspath(__file__)).split('/common')[0]

        self.options = options
        self.headless = headless
        self.driver = None
        self.url = url
        self.start_time = 0
        self.end_time = 0

        self.download_path = download_path

        self.custom_ele_text_dict = {}

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

        if self.pf == "Linux":
            options.add_argument("--no-sandbox")

        if self.options == 'chrome':
            prefs = {
                'profile.default_content_settings.popups': 0,
                'download.default_directory': self.download_path,
                "profile.default_content_setting_values.automatic_downloads": 1
            }  # 取消下载多个文件的弹窗，直接自动下载多个文件
            options.add_experimental_option('prefs', prefs)

        self.driver = driver_dict.get(self.options)(options=options)
        print(self.driver)

    def set_url(self, url):
        self.url = url

    def open(self, url):
        """启动浏览器"""

        self.url = url
        self.driver_init()
        self.start()
        self.driver.get(self.url)

    def close(self, **kwargs):
        """关闭"""

        self.end()

    def start(self):
        """启动"""

        self.start_time = datetime.now()
        print(self.start_time)
        print(self.driver.title)

    def end(self):
        """结束"""

        self.end_time = datetime.now()
        print(self.end_time)
        self.driver.quit()

    def ts(self, n):
        """隐式等待"""

        self.driver.implicitly_wait(n)

    def x(self):
        """截屏"""

        self.driver.save_screenshot(f"{self.source_path}/test/web_ui_png/baidu_{int(time.time())}.png")  # 截屏

    def wait_element(self, by: By, value: str, timeout: int = 5):
        """
        显式等待
        :param by: By.ID , By.XPATH ...
        :param value: 元素名称
        :param timeout: 等待时间
        :return: 元素
        """

        locator = (by, value)
        wait = WebDriverWait(self.driver, timeout=timeout)
        element = wait.until(ec.presence_of_element_located(locator))
        return element

    def fluent_wait_element(self, by: By, value: str, timeout: int = 5):
        """
        流畅等待
        :param by: By.ID , By.XPATH ...
        :param value: 元素名称
        :param timeout: 等待时间
        :return:
        """

        wait = WebDriverWait(
            self.driver, timeout=timeout, poll_frequency=1,
            ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]
        )
        element = wait.until(ec.element_to_be_clickable((by, value)))
        return element

    def get_element(self, mode: str, value: str):
        """
        获取定位对象
        :param mode: 定位方式,例如id,class,xpath等
        :param value: 定位对应的值,例如id的值
        :return:
        """

        by = getattr(By, mode)
        ele = self.wait_element(by=by, value=value)
        return ele

    def custom_input(self, mode: str, value: str, data: any):
        """
        输入
        :param mode: 定位方式,例如id,class,xpath等
        :param value: 定位对应的值,例如id的值
        :param data: 输入框的值
        :return:
        """

        ele = self.get_element(mode=mode, value=value)
        ele.send_keys(data)

    def custom_click(self, mode: str, value: str):
        """
        点击
        :param mode: 定位方式,例如id,class,xpath等
        :param value: 定位对应的值,例如id的值
        :return:
        """

        ele = self.get_element(mode=mode, value=value)
        ele.click()

    def custom_clear(self, mode: str, value: str):
        """
        清空输入框
        :param mode:
        :param value:
        :return:
        """

        ele = self.get_element(mode=mode, value=value)
        ele.clear()

        if ele.text not in ('', None):
            if self.pf == "Darwin":
                ActionChains(self.driver).key_down(Keys.COMMAND).send_keys('a').key_down(Keys.BACKSPACE).key_up(
                    Keys.COMMAND).key_up(Keys.BACKSPACE).perform()
            else:
                ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_down(Keys.BACKSPACE).key_up(
                    Keys.CONTROL).key_up(Keys.BACKSPACE).perform()

    def custom_sleep(self, num: (int, float)):
        """
        等待
        :param num:
        :return:
        """

        try:
            if isinstance(num, str):
                n = float(num) if '.' in num else int(num)
            else:
                n = num
        except:
            n = 0

        time.sleep(n)
        print(f'等待 {n} s')

    def custom_get_text(self, mode: str, value: str, data: str):
        """获取文本字符串"""

        ele = self.get_element(mode=mode, value=value)
        self.custom_ele_text_dict[data] = ele.text
        print("=== custom_ele_text_dict ===", self.custom_ele_text_dict)

    def test(self):
        self.driver_init()
        self.start()
        self.driver.get('https://www.baidu.com')
        # self.driver.maximize_window()
        print(self.driver.title)
        # time.sleep(2)

        res1 = self.wait_element(by=By.XPATH, value="""//*[@id="kw2"]""")
        res1.send_keys('yyx')

        res2 = self.wait_element(by=By.XPATH, value="""//*[@id="su"]""")
        res2.click()

        # res1 = self.wait_element(by=By.ID, value="kw")
        # res1.send_keys('yyx')
        # res2 = self.wait_element(by=By.ID, value="su")
        # res2.click()

        self.end()

    def test_h5(self):
        """
        1.设置窗口大小触发H5适配
        2.设置为手机模式与对应宽和高
        :return:
        """

        self.driver_init()
        self.start()

        # self.driver.get('https://www.metatuple.com/')
        self.driver.get('http://192.168.8.97:9966/play/73I96Vc0')
        # self.driver.get('https://www.baidu.com')
        self.driver.set_window_size(390, 844)

        # self.driver.set_window_size(390, 844)
        # set_device_metrics_override = dict({
        #     "width": 390,
        #     "height": 844,
        #     "deviceScaleFactor": 1000,
        #     "mobile": False
        # })
        # self.driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', set_device_metrics_override)
        # self.driver.get('https://www.metatuple.com/')


if __name__ == '__main__':
    bwd = BaseWebDriver(headless=False)
    bwd.test()
    # bwd.test_h5()
