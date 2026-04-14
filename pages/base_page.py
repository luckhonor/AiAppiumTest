"""
PageObject 基类
所有页面对象继承自此类
"""
from typing import Optional, TypeVar, Type
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from functools import wraps
import logging

logger = logging.getLogger(__name__)
T = TypeVar('T', bound='BasePage')


class BasePage:
    """PageObject 基类"""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10, poll_frequency=0.5)

    def _find_element(self, locator: tuple, timeout: int = 10):
        """查找元素（显式等待）"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"元素未找到：{locator}")
            self._screenshot_on_error(f"element_not_found_{locator[0].value}")
            raise

    def _find_elements(self, locator: tuple, timeout: int = 10):
        """查找多个元素"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            logger.error(f"元素列表未找到：{locator}")
            return []

    def _click(self, locator: tuple, timeout: int = 10):
        """点击元素"""
        element = self._find_element(locator, timeout)
        try:
            element.click()
            logger.debug(f"点击元素：{locator}")
        except Exception as e:
            logger.error(f"点击失败：{locator}, 错误：{e}")
            raise

    def _input(self, locator: tuple, value: str, timeout: int = 10):
        """输入文本"""
        element = self._find_element(locator, timeout)
        element.clear()
        element.send_keys(value)
        logger.debug(f"输入文本：{locator} = {value}")

    def _get_text(self, locator: tuple, timeout: int = 10) -> str:
        """获取元素文本"""
        element = self._find_element(locator, timeout)
        return element.text

    def _is_displayed(self, locator: tuple, timeout: int = 5) -> bool:
        """元素是否可见"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def _is_exist(self, locator: tuple, timeout: int = 2) -> bool:
        """元素是否存在（不抛异常）"""
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False

    def _swipe(self, start_x: float, start_y: float, end_x: float, end_y: float, duration: int = 500):
        """滑动操作"""
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        logger.debug(f"滑动：({start_x}, {start_y}) -> ({end_x}, {end_y})")

    def _swipe_up(self, percent: float = 0.5, duration: int = 500):
        """向上滑动"""
        size = self.driver.get_window_size()
        start_y = size['height'] * percent
        end_y = size['height'] * (1 - percent)
        center_x = size['width'] / 2
        self._swipe(center_x, start_y, center_x, end_y, duration)

    def _swipe_down(self, percent: float = 0.5, duration: int = 500):
        """向下滑动"""
        size = self.driver.get_window_size()
        start_y = size['height'] * (1 - percent)
        end_y = size['height'] * percent
        center_x = size['width'] / 2
        self._swipe(center_x, start_y, center_x, end_y, duration)

    def _screenshot(self, filename: str):
        """截图"""
        import os
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        filepath = os.path.join(screenshot_dir, f"{filename}.png")
        self.driver.save_screenshot(filepath)
        logger.info(f"截图保存：{filepath}")
        return filepath

    def _screenshot_on_error(self, error_name: str):
        """失败时截图"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{error_name}_{timestamp}"
        return self._screenshot(filename)

    def _wait_until(self, condition, timeout: int = 10):
        """自定义等待条件"""
        try:
            return WebDriverWait(self.driver, timeout).until(condition)
        except TimeoutException:
            logger.error(f"等待超时：{condition}")
            raise

    @classmethod
    def verify_page(cls: Type[T], driver: WebDriver, locator: tuple = None, timeout: int = 5) -> T:
        """
        验证当前页面并返回页面对象
        用于页面对象的链式调用
        """
        instance = cls(driver)
        if locator:
            try:
                instance._find_element(locator, timeout)
            except TimeoutException:
                raise AssertionError(f"页面验证失败：{cls.__name__}")
        return instance
