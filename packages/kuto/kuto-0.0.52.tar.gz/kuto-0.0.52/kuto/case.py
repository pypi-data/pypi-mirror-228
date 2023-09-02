import json
import time
from typing import Union
from urllib import parse

from kuto.core.android.driver import AndroidDriver
from kuto.core.api.request import HttpReq
from kuto.core.ios.driver import IosDriver
from kuto.core.web.driver import PlayWrightDriver
from kuto.core.web.element import WebElem

from kuto.utils.config import config
from kuto.utils.log import logger
from kuto.utils.exceptions import HostIsNull


class Page(object):
    """页面基类，用于pom模式封装"""

    def __init__(self, driver):
        self.driver = driver


class Case(HttpReq):
    """
    测试用例基类，所有测试用例需要继承该类
    """

    driver: Union[AndroidDriver, IosDriver, PlayWrightDriver] = None

    # ---------------------初始化-------------------------------
    def start_class(self):
        """
        Hook method for setup_class fixture
        :return:
        """
        pass

    def end_class(self):
        """
        Hook method for teardown_class fixture
        :return:
        """
        pass

    @classmethod
    def setup_class(cls):
        cls().start_class()

    @classmethod
    def teardown_class(cls):
        cls().end_class()

    def start(self):
        """
        Hook method for setup_method fixture
        :return:
        """
        pass

    def end(self):
        """
        Hook method for teardown_method fixture
        :return:
        """
        pass

    def setup_method(self):
        self.start_time = time.time()
        platform = config.get_common("platform")
        if platform == "android":
            device_id = config.get_app("device_id")
            pkg_name = config.get_app("pkg_name")
            self.driver = AndroidDriver(device_id, pkg_name)
        elif platform == "ios":
            device_id = config.get_app("device_id")
            wda_url = config.get_app("wda_url")
            pkg_name = config.get_app("pkg_name")
            if wda_url:
                self.driver = IosDriver(wda_url=wda_url, pkg_name=pkg_name)
            else:
                self.driver = IosDriver(device_id=device_id, pkg_name=pkg_name)
        elif platform == "web":
            browserName = config.get_web("browser_name")
            headless = config.get_web("headless")
            state = config.get_web("state")
            if state:
                state_json = json.loads(state)
                self.driver = PlayWrightDriver(browserName=browserName, headless=headless, state=state_json)
            else:
                self.driver = PlayWrightDriver(browserName=browserName, headless=headless)
        if isinstance(self.driver, (AndroidDriver, IosDriver)):
            if config.get_app("auto_start") is True:
                self.driver.start_app()
        self.start()

    def teardown_method(self):
        self.end()
        if isinstance(self.driver, PlayWrightDriver):
            self.driver.close()
        if isinstance(self.driver, (AndroidDriver, IosDriver)):
            if config.get_app("auto_start") is True:
                self.driver.stop_app()
        take_time = time.time() - self.start_time
        logger.info("用例耗时: {:.2f} s".format(take_time))

    @staticmethod
    def sleep(n: float):
        """休眠"""
        logger.info(f"暂停: {n}s")
        time.sleep(n)

    def open_url(self, url=None):
        """浏览器打开页面"""
        # 拼接域名
        if url is None:
            base_url = config.get_web("base_url")
            if not base_url:
                raise HostIsNull('base_url is null')
            url = base_url
        else:
            if "http" not in url:
                base_url = config.get_web("base_url")
                if not base_url:
                    raise HostIsNull('base_url is null')
                url = parse.urljoin(base_url, url)
        # 访问页面
        self.driver.open_url(url)
        # 设置cookies
        cookies = config.get_web("cookies")
        if cookies:
            self.driver.set_cookies(cookies)

    def switch_tab(self, **kwargs):
        """切换到新页签，需要先定位导致跳转的元素"""
        locator = WebElem(self.driver, **kwargs)
        self.driver.switch_tab(locator)

    def screenshot(self, name: str):
        """截图"""
        self.driver.screenshot(name)

    # 断言
    def assert_act(self, activity_name: str, timeout=5):
        """断言当前activity，安卓端使用"""
        self.driver.assert_act(activity_name, timeout=timeout)

    def assert_title(self, title: str, timeout=5):
        """断言页面title，web端使用"""
        self.driver.assert_title(title, timeout=timeout)

    def assert_url(self, url: str = None, timeout=5):
        """断言页面url，web端使用"""
        # 拼接域名
        if url is None:
            base_url = config.get_web("base_url")
            if not base_url:
                raise HostIsNull('base_url is null')
            url = base_url + "/"
        else:
            if "http" not in url:
                base_url = config.get_web("base_url")
                if not base_url:
                    raise HostIsNull('base_url is null')
                url = parse.urljoin(base_url, url)
        self.driver.assert_url(url, timeout=timeout)



