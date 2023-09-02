import time

from kuto.utils.log import logger
from kuto.core.ios.driver import IosDriver
from kuto.utils.common import dict_to_str, calculate_time
from kuto.utils.exceptions import NoSuchElementException


class IosElem(object):
    """
    IOS原生元素定义
    """

    def __init__(self,
                 iosDriver: IosDriver = None,
                 name: str = None,
                 label: str = None,
                 labelCont: str = None,
                 value: str = None,
                 valueCont: str = None,
                 text: str = None,
                 textCont: str = None,
                 className: str = None,
                 xpath: str = None,
                 index: int = None):
        """
        param iosDriver,
        param name,
        param label,
        param value,
        param text,
        param className,
        param xpath,
        param index: 索引
        """
        self._driver = iosDriver

        self._kwargs = {}
        if name is not None:
            self._kwargs["name"] = name
        if label is not None:
            self._kwargs["label"] = label
        if labelCont is not None:
            self._kwargs["labelContains"] = labelCont
        if value is not None:
            self._kwargs["value"] = value
        if valueCont is not None:
            self._kwargs["valueContains"] = valueCont
        if text is not None:
            self._kwargs["text"] = text
        if textCont is not None:
            self._kwargs["textContains"] = textCont
        if className is not None:
            self._kwargs["className"] = className
        if index is not None:
            self._kwargs["index"] = index

        self._xpath = xpath

    def __get__(self, instance, owner):
        """po模式中element初始化不需要带driver的关键"""
        if instance is None:
            return None

        self._driver = instance.driver
        return self

    @calculate_time
    def find(self, timeout=5):
        """
        针对元素定位失败的情况，抛出NoSuchElementException异常
        @param timeout:
        @return:
        """
        if self._xpath is not None:
            logger.info(f'查找控件: xpath={self._xpath}')
        else:
            logger.info(f'查找控件: {self._kwargs}')

        _element = self._driver.d.xpath(self._xpath) if \
            self._xpath else self._driver.d(**self._kwargs)
        try:
            if _element.wait(timeout=timeout):
                logger.info(f"查找成功")
                return _element
            else:
                logger.info(f"查找失败")
                self._driver.screenshot(dict_to_str(self._kwargs) + "_查找失败")
                raise NoSuchElementException(f"控件 {self._kwargs} 查找失败")
        except ConnectionError:
            logger.info('wda连接失败, 进行重连!!!')
            # 由于WDA会意外链接错误
            self._driver = IosDriver(self._driver.device_id, self._driver.pkg_name)
            time.sleep(5)

            logger.info('重连成功, 重新开始查找控件')
            if _element.wait(timeout=timeout):
                logger.info(f"查找成功")
                return _element
            else:
                logger.info(f"查找失败")
                self._driver.screenshot(dict_to_str(self._kwargs))
                raise NoSuchElementException(f"控件 {self._kwargs} 查找失败")

    @property
    def text(self):
        """获取元素文本"""
        logger.info(f"获取空间文本属性")
        text = [elem.text for elem in self.find(timeout=5).find_elements()]
        logger.info(text)
        return text

    def exists(self, timeout=3):
        """
        判断元素是否存在当前页面
        @param timeout:
        @return:
        """
        logger.info("检查控件是否存在")
        _element = self._driver.d.xpath(self._xpath) if \
            self._xpath else self._driver.d(**self._kwargs)
        result = _element.wait(timeout=timeout, raise_error=False)
        logger.info(result)
        return result

    def _adapt_center(self, timeout=5):
        """
        修正控件中心坐标
        """
        bounds = self.find(timeout=timeout).bounds
        left_top_x, left_top_y, width, height = \
            bounds.x, bounds.y, bounds.width, bounds.height
        center_x = int(left_top_x + width/2)
        center_y = int(left_top_y + height/2)
        logger.info(f'{center_x}, {center_y}')
        return center_x, center_y

    def click(self, timeout=5):
        """
        单击
        @param: retry，重试次数
        @param: timeout，每次重试超时时间
        """
        logger.info('点击控件')
        x, y = self._adapt_center(timeout=timeout)
        self._driver.d.appium_settings({"snapshotMaxDepth": 0})
        self._driver.d.tap(x, y)
        self._driver.d.appium_settings({"snapshotMaxDepth": 50})

    def click_exists(self, timeout=3):
        logger.info(f"控件存在才点击")
        if self.exists(timeout=timeout):
            self.click()

    def clear(self):
        """清除文本"""
        logger.info("清除输入框文本")
        self.find().clear_text()

    def input(self, text):
        """输入内容"""
        logger.info(f"输入文本：{text}")
        self.find().set_text(text)

    def input_exists(self, text: str, timeout=3):
        logger.info(f"控件存在才输入: {text}")
        if self.exists(timeout=timeout):
            self.input(text)
            logger.info("输入成功")
        else:
            logger.info("控件不存在")

    def assert_exists(self, timeout=3):
        logger.info("断言控件存在")
        status = self.exists(timeout=timeout)
        assert status, f"控件不存在"

    def assert_text(self, text, timeout=3):
        logger.info(f"断言控件文本属性包括: {text}")
        self.find(timeout=timeout)
        _text = self.text
        assert text in _text, f"文本属性 {_text} 不包含 {text}"


if __name__ == '__main__':
    driver = IosDriver(
        device_id="00008101-000E646A3C29003A",
        pkg_name="com.qizhidao.company"
    )
    print(IosElem(driver, labelCont="华为").text)















