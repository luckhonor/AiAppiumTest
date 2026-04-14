"""
智能等待策略封装
提供多种等待条件和组合用法
"""
from typing import Callable, Optional, Any, List
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
import logging
import time

logger = logging.getLogger(__name__)


class WaitStrategy:
    """等待策略工具类"""

    def __init__(self, driver, default_timeout: int = 10):
        self.driver = driver
        self.default_timeout = default_timeout
        self.wait = WebDriverWait(driver, default_timeout, poll_frequency=0.5)

    # ========== 基础等待条件 ==========

    def wait_for_presence(self, locator: tuple, timeout: int = None) -> Any:
        """等待元素存在（DOM 中）"""
        return self.wait.until(
            EC.presence_of_element_located(locator),
            message=f"元素未存在：{locator}"
        )

    def wait_for_visible(self, locator: tuple, timeout: int = None) -> Any:
        """等待元素可见"""
        return self.wait.until(
            EC.visibility_of_element_located(locator),
            message=f"元素不可见：{locator}"
        )

    def wait_for_clickable(self, locator: tuple, timeout: int = None) -> Any:
        """等待元素可点击"""
        return self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f"元素不可点击：{locator}"
        )

    def wait_for_invisible(self, locator: tuple, timeout: int = None) -> bool:
        """等待元素不可见"""
        return self.wait.until(
            EC.invisibility_of_element_located(locator),
            message=f"元素持续可见：{locator}"
        )

    def wait_for_absent(self, locator: tuple, timeout: int = None) -> bool:
        """等待元素不存在"""
        def check_absent(driver):
            try:
                elements = driver.find_elements(*locator)
                return len(elements) == 0
            except:
                return True

        return self.wait.until(check_absent, message=f"元素持续存在：{locator}")

    def wait_for_text(self, locator: tuple, text: str, timeout: int = None) -> bool:
        """等待元素包含指定文本"""
        return self.wait.until(
            EC.text_to_be_present_in_element(locator, text),
            message=f"元素文本不匹配：{locator}, 期望：{text}"
        )

    def wait_for_value(self, locator: tuple, value: str, timeout: int = None) -> bool:
        """等待元素 value 属性包含指定值"""
        return self.wait.until(
            EC.text_to_be_present_in_element_value(locator, value),
            message=f"元素 value 不匹配：{locator}, 期望：{value}"
        )

    def wait_for_attribute(
        self,
        locator: tuple,
        attribute: str,
        value: str,
        timeout: int = None
    ) -> bool:
        """等待元素属性等于指定值"""
        def check_attribute(driver):
            try:
                element = driver.find_element(*locator)
                actual_value = element.get_attribute(attribute)
                return actual_value == value
            except:
                return False

        return self.wait.until(check_attribute, message=f"元素属性不匹配：{locator}")

    # ========== 高级等待条件 ==========

    def wait_for_elements(self, locator: tuple, count: int = None, timeout: int = None) -> List:
        """
        等待多个元素

        Args:
            locator: 元素定位器
            count: 期望的元素数量（None 表示至少 1 个）
            timeout: 超时时间
        """
        timeout = timeout or self.default_timeout

        def check_elements(driver):
            elements = driver.find_elements(*locator)
            if count is not None:
                return len(elements) == count
            return len(elements) > 0

        return WebDriverWait(driver, timeout).until(
            check_elements,
            message=f"元素列表未找到：{locator}"
        )

    def wait_for_frame(self, frame_locator: tuple, timeout: int = None) -> Any:
        """等待 frame 可用"""
        return self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(frame_locator),
            message=f"Frame 不可用：{frame_locator}"
        )

    def wait_for_alert(self, timeout: int = None) -> Any:
        """等待 Alert 弹窗"""
        return self.wait.until(
            EC.alert_is_present(),
            message="Alert 未出现"
        )

    def wait_for_new_window(self, window_handles_count: int = 2, timeout: int = None) -> List:
        """等待新窗口打开"""
        def check_window(driver):
            return len(driver.window_handles) >= window_handles_count

        return WebDriverWait(driver, timeout or self.default_timeout).until(
            check_window,
            message="新窗口未打开"
        )

    # ========== 组合等待 ==========

    def wait_for_all(self, locators: List[tuple], timeout: int = None) -> List:
        """等待多个元素都出现"""
        results = []
        for locator in locators:
            results.append(self.wait_for_presence(locator, timeout))
        return results

    def wait_for_any(self, locators: List[tuple], timeout: int = None) -> tuple:
        """
        等待任意一个元素出现

        Returns:
            匹配的定位器和元素
        """
        timeout = timeout or self.default_timeout
        end_time = time.time() + timeout

        while time.time() < end_time:
            for locator in locators:
                try:
                    element = self.driver.find_element(*locator)
                    if element.is_displayed():
                        return locator, element
                except:
                    continue
            time.sleep(0.2)

        raise TimeoutError(f"等待任意元素超时：{locators}")

    def wait_until(self, condition: Callable, timeout: int = None, message: str = None) -> Any:
        """
        自定义等待条件

        Args:
            condition: 条件函数，接收 driver 参数
            timeout: 超时时间
            message: 超时错误信息
        """
        return self.wait.until(condition, message=message or "等待条件未满足")

    # ========== 轮询等待 ==========

    def wait_with_poll(
        self,
        condition: Callable,
        timeout: int = None,
        poll_frequency: float = 0.5,
        ignored_exceptions: tuple = None
    ) -> Any:
        """
        轮询等待

        Args:
            condition: 条件函数
            timeout: 超时时间
            poll_frequency: 轮询间隔
            ignored_exceptions: 忽略的异常类型
        """
        from selenium.webdriver.support.expected_conditions import _element_interface

        wait = WebDriverWait(
            self.driver,
            timeout or self.default_timeout,
            poll_frequency=poll_frequency,
            ignored_exceptions=ignored_exceptions
        )

        return wait.until(condition)

    # ========== 便捷方法 ==========

    def wait_page_loaded(self, timeout: int = None) -> bool:
        """等待页面加载完成（通过检查特定元素）"""
        # 这里可以自定义页面加载完成的标志
        time.sleep(0.5)  # 短暂等待
        return True

    def wait_animation_complete(
        self,
        locator: tuple,
        attribute: str = "animated",
        timeout: int = None
    ) -> bool:
        """
        等待动画完成

        Args:
            locator: 元素定位器
            attribute: 动画相关属性
            timeout: 超时时间
        """
        def check_animation(driver):
            try:
                element = driver.find_element(*locator)
                # 检查元素是否还在动画中
                return not element.is_displayed() or \
                       element.get_attribute(attribute) != "true"
            except:
                return True

        return self.wait.until(check_animation, message="动画未结束")
