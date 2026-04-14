"""
文案定位策略封装
基于文本内容定位元素，适配 iOS/Android 双端
特别适合 AI 生成脚本场景
"""
from typing import Optional, List
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)


class TextLocator:
    """
    文案定位器
    统一的文本定位接口，自动适配 Android/iOS
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.platform = driver.capabilities.get("platformName", "").lower()
        self.wait = WebDriverWait(driver, timeout)

    # ========== 精确匹配 ==========

    def find_by_text(self, text: str) -> any:
        """
        通过精确文本查找元素

        Args:
            text: 要查找的文本内容

        Returns:
            元素对象

        Raises:
            TimeoutException: 未找到元素
        """
        if self.platform == "android":
            # Android: 使用 UiSelector text 精确匹配
            locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
        else:
            # iOS: 使用 iOS_PREDICATE label 精确匹配
            locator = (AppiumBy.IOS_PREDICATE, f'label == "{text}"')

        return self.wait.until(EC.presence_of_element_located(locator))

    def find_by_text_exists(self, text: str) -> bool:
        """
        检查文本元素是否存在（不抛异常）

        Args:
            text: 要查找的文本内容

        Returns:
            是否存在
        """
        try:
            self.find_by_text(text)
            return True
        except:
            return False

    # ========== 模糊匹配 ==========

    def find_by_text_contains(self, text: str) -> any:
        """
        通过包含文本查找元素

        Args:
            text: 要查找的文本内容（部分匹配）

        Returns:
            元素对象
        """
        if self.platform == "android":
            # Android: 使用 UiSelector textContains
            locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text}")')
        else:
            # iOS: 使用 iOS_PREDICATE label CONTAINS
            locator = (AppiumBy.IOS_PREDICATE, f'label CONTAINS "{text}"')

        return self.wait.until(EC.presence_of_element_located(locator))

    def find_by_text_starts_with(self, text: str) -> any:
        """
        通过开头文本查找元素

        Args:
            text: 要查找的文本内容（开头匹配）

        Returns:
            元素对象
        """
        if self.platform == "android":
            # Android: 使用 XPath text 开头匹配
            locator = (AppiumBy.XPATH, f'//*[starts-with(@text, "{text}")]')
        else:
            # iOS: 使用 iOS_PREDICATE label BEGINSWITH
            locator = (AppiumBy.IOS_PREDICATE, f'label BEGINSWITH "{text}"')

        return self.wait.until(EC.presence_of_element_located(locator))

    def find_by_text_ends_with(self, text: str) -> any:
        """
        通过结尾文本查找元素

        Args:
            text: 要查找的文本内容（结尾匹配）

        Returns:
            元素对象
        """
        if self.platform == "android":
            # Android: 使用 XPath text 结尾匹配
            locator = (AppiumBy.XPATH, f'//*[substring(@text, string-length(@text)-string-length("{text}")+1) = "{text}"]')
        else:
            # iOS: 使用 iOS_PREDICATE label ENDSWITH
            locator = (AppiumBy.IOS_PREDICATE, f'label ENDSWITH "{text}"')

        return self.wait.until(EC.presence_of_element_located(locator))

    # ========== 多元素查找 ==========

    def find_elements_by_text_contains(self, text: str) -> List:
        """
        查找所有包含指定文本的元素

        Args:
            text: 要查找的文本内容

        Returns:
            元素列表
        """
        if self.platform == "android":
            locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text}")')
        else:
            locator = (AppiumBy.IOS_PREDICATE, f'label CONTAINS "{text}"')

        try:
            return self.driver.find_elements(*locator)
        except:
            return []

    # ========== 组合定位 ==========

    def find_by_text_and_class(self, text: str, class_name: str) -> any:
        """
        通过文本 + 类名组合定位

        Args:
            text: 文本内容
            class_name: 类名

        Returns:
            元素对象
        """
        if self.platform == "android":
            locator = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().text("{text}").className("{class_name}")'
            )
        else:
            # iOS: 使用 type 和 label 组合
            locator = (
                AppiumBy.IOS_PREDICATE,
                f'type == "{class_name}" AND label == "{text}"'
            )

        return self.wait.until(EC.presence_of_element_located(locator))

    def find_by_text_and_resource_id(
        self,
        text: str,
        resource_id: str
    ) -> any:
        """
        通过文本 + resource_id 组合定位（仅 Android）

        Args:
            text: 文本内容
            resource_id: 资源 ID

        Returns:
            元素对象
        """
        if self.platform == "android":
            locator = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().text("{text}").resourceId("{resource_id}")'
            )
        else:
            # iOS 不支持 resourceId，降级为仅文本匹配
            logger.warning("iOS 不支持 resourceId 定位，降级为文本匹配")
            return self.find_by_text(text)

        return self.wait.until(EC.presence_of_element_located(locator))

    # ========== 智能定位（多策略降级） ==========

    def find_smart(self, text: str) -> any:
        """
        智能定位：尝试多种策略，自动降级

        策略顺序：
        1. 精确文本匹配
        2. 包含文本匹配
        3. XPath 全文匹配（备选）

        Args:
            text: 要查找的文本内容

        Returns:
            元素对象
        """
        strategies = [
            ("精确匹配", self._try_exact_match, text),
            ("包含匹配", self._try_contains_match, text),
            ("XPath 匹配", self._try_xpath_match, text),
        ]

        for strategy_name, strategy_func, param in strategies:
            try:
                logger.debug(f"尝试定位策略：{strategy_name}")
                element = strategy_func(param)
                if element:
                    logger.info(f"定位成功，策略：{strategy_name}")
                    return element
            except Exception as e:
                logger.debug(f"策略 {strategy_name} 失败：{e}")
                continue

        raise TimeoutException(f"所有定位策略都失败：{text}")

    def _try_exact_match(self, text: str) -> any:
        """尝试精确匹配"""
        return self.find_by_text(text)

    def _try_contains_match(self, text: str) -> any:
        """尝试包含匹配"""
        return self.find_by_text_contains(text)

    def _try_xpath_match(self, text: str) -> any:
        """尝试 XPath 匹配"""
        if self.platform == "android":
            locator = (AppiumBy.XPATH, f'//*[@text="{text}"]')
        else:
            locator = (AppiumBy.XPATH, f'//*[@label="{text}"]')
        return self.wait.until(EC.presence_of_element_located(locator))

    # ========== 点击操作 ==========

    def click_by_text(self, text: str):
        """
        通过文本定位并点击

        Args:
            text: 要点击的文本内容
        """
        element = self.find_by_text(text)
        element.click()
        logger.info(f"点击元素：{text}")

    def click_by_text_contains(self, text: str):
        """
        通过包含文本定位并点击

        Args:
            text: 要点击的文本内容（部分匹配）
        """
        element = self.find_by_text_contains(text)
        element.click()
        logger.info(f"点击元素（包含）：{text}")

    # ========== 文本验证 ==========

    def verify_text_exists(self, text: str) -> bool:
        """
        验证文本是否存在

        Args:
            text: 要验证的文本

        Returns:
            是否存在
        """
        return self.find_by_text_exists(text)

    def verify_text_exact(self, text: str, expected: str) -> bool:
        """
        验证文本完全匹配

        Args:
            text: 定位文本
            expected: 期望的文本值

        Returns:
            是否匹配
        """
        element = self.find_by_text(text)
        return element.text == expected

    def verify_text_contains(self, text: str, expected: str) -> bool:
        """
        验证文本包含

        Args:
            text: 定位文本
            expected: 期望包含的内容

        Returns:
            是否包含
        """
        element = self.find_by_text(text)
        return expected in element.text


# ========== 便捷函数 ==========

def find_by_text(driver: WebDriver, text: str, timeout: int = 10) -> any:
    """便捷函数：通过文本查找元素"""
    locator = TextLocator(driver, timeout)
    return locator.find_by_text(text)


def click_by_text(driver: WebDriver, text: str, timeout: int = 10):
    """便捷函数：通过文本点击元素"""
    locator = TextLocator(driver, timeout)
    locator.click_by_text(text)


def text_exists(driver: WebDriver, text: str, timeout: int = 10) -> bool:
    """便捷函数：检查文本是否存在"""
    locator = TextLocator(driver, timeout)
    return locator.find_by_text_exists(text)
