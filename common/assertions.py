"""
断言封装
提供丰富的断言方法用于测试验证
"""
import logging
from typing import Any, Optional, List
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class Assertion:
    """断言工具类"""

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.errors: List[str] = []

    # ========== 元素相关断言 ==========

    def assert_element_exists(self, locator: tuple, msg: str = None) -> bool:
        """断言元素存在"""
        try:
            element = self.driver.find_element(*locator)
            assert element is not None, msg or "元素不存在"
            logger.debug(f"断言通过：元素存在 {locator}")
            return True
        except Exception as e:
            self._fail(msg or f"元素不存在：{locator}", e)
            return False

    def assert_element_not_exists(self, locator: tuple, msg: str = None) -> bool:
        """断言元素不存在"""
        try:
            elements = self.driver.find_elements(*locator)
            assert len(elements) == 0, msg or "元素不应存在"
            logger.debug(f"断言通过：元素不存在 {locator}")
            return True
        except Exception as e:
            self._fail(msg or f"元素不应存在：{locator}", e)
            return False

    def assert_element_visible(self, locator: tuple, msg: str = None) -> bool:
        """断言元素可见"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            assert element.is_displayed(), msg or "元素不可见"
            logger.debug(f"断言通过：元素可见 {locator}")
            return True
        except Exception as e:
            self._fail(msg or f"元素不可见：{locator}", e)
            return False

    def assert_element_not_visible(self, locator: tuple, msg: str = None) -> bool:
        """断言元素不可见"""
        try:
            result = self.wait.until(EC.invisibility_of_element_located(locator))
            assert result, msg or "元素应不可见"
            logger.debug(f"断言通过：元素不可见 {locator}")
            return True
        except Exception as e:
            self._fail(msg or f"元素应不可见：{locator}", e)
            return False

    def assert_element_clickable(self, locator: tuple, msg: str = None) -> bool:
        """断言元素可点击"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            assert element.is_enabled(), msg or "元素不可点击"
            logger.debug(f"断言通过：元素可点击 {locator}")
            return True
        except Exception as e:
            self._fail(msg or f"元素不可点击：{locator}", e)
            return False

    def assert_element_count(
        self,
        locator: tuple,
        expected_count: int,
        msg: str = None
    ) -> bool:
        """断言元素数量"""
        try:
            elements = self.driver.find_elements(*locator)
            assert len(elements) == expected_count, \
                msg or f"元素数量不匹配：期望 {expected_count}, 实际 {len(elements)}"
            logger.debug(f"断言通过：元素数量 {expected_count} {locator}")
            return True
        except Exception as e:
            self._fail(msg or f"元素数量不匹配：{locator}", e)
            return False

    # ========== 文本相关断言 ==========

    def assert_text_equals(
        self,
        locator: tuple,
        expected_text: str,
        msg: str = None
    ) -> bool:
        """断言文本完全匹配"""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            actual_text = element.text.strip()
            assert actual_text == expected_text, \
                msg or f"文本不匹配：期望 '{expected_text}', 实际 '{actual_text}'"
            logger.debug(f"断言通过：文本匹配 '{expected_text}' {locator}")
            return True
        except Exception as e:
            self._fail(msg or f"文本不匹配：{locator}", e)
            return False

    def assert_text_contains(
        self,
        locator: tuple,
        expected_text: str,
        msg: str = None
    ) -> bool:
        """断言文本包含"""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            actual_text = element.text
            assert expected_text in actual_text, \
                msg or f"文本不包含：期望包含 '{expected_text}', 实际 '{actual_text}'"
            logger.debug(f"断言通过：文本包含 '{expected_text}' {locator}")
            return True
        except Exception as e:
            self._fail(msg or f"文本不包含：{locator}", e)
            return False

    def assert_attribute_equals(
        self,
        locator: tuple,
        attribute: str,
        expected_value: str,
        msg: str = None
    ) -> bool:
        """断言属性值等于期望值"""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            actual_value = element.get_attribute(attribute)
            assert actual_value == expected_value, \
                msg or f"属性不匹配：{attribute} 期望 '{expected_value}', 实际 '{actual_value}'"
            logger.debug(f"断言通过：属性 {attribute}='{expected_value}' {locator}")
            return True
        except Exception as e:
            self._fail(msg or f"属性不匹配：{locator}", e)
            return False

    def assert_attribute_contains(
        self,
        locator: tuple,
        attribute: str,
        expected_value: str,
        msg: str = None
    ) -> bool:
        """断言属性值包含期望值"""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            actual_value = element.get_attribute(attribute)
            assert expected_value in actual_value, \
                msg or f"属性不包含：{attribute} 期望包含 '{expected_value}', 实际 '{actual_value}'"
            logger.debug(f"断言通过：属性 {attribute} 包含 '{expected_value}' {locator}")
            return True
        except Exception as e:
            self._fail(msg or f"属性不包含：{locator}", e)
            return False

    # ========== 页面相关断言 ==========

    def assert_current_url_contains(self, expected_url: str, msg: str = None) -> bool:
        """断言当前 URL 包含期望字符串"""
        try:
            current_url = self.driver.current_url
            assert expected_url in current_url, \
                msg or f"URL 不包含：期望包含 '{expected_url}', 实际 '{current_url}'"
            logger.debug(f"断言通过：URL 包含 '{expected_url}'")
            return True
        except Exception as e:
            self._fail(msg or "URL 不匹配", e)
            return False

    def assert_title_equals(self, expected_title: str, msg: str = None) -> bool:
        """断言页面标题等于期望值"""
        try:
            actual_title = self.driver.title
            assert actual_title == expected_title, \
                msg or f"标题不匹配：期望 '{expected_title}', 实际 '{actual_title}'"
            logger.debug(f"断言通过：标题匹配 '{expected_title}'")
            return True
        except Exception as e:
            self._fail(msg or "标题不匹配", e)
            return False

    def assert_title_contains(self, expected_title: str, msg: str = None) -> bool:
        """断言页面标题包含期望字符串"""
        try:
            actual_title = self.driver.title
            assert expected_title in actual_title, \
                msg or f"标题不包含：期望包含 '{expected_title}', 实际 '{actual_title}'"
            logger.debug(f"断言通过：标题包含 '{expected_title}'")
            return True
        except Exception as e:
            self._fail(msg or "标题不匹配", e)
            return False

    # ========== 值相关断言 ==========

    def assert_equals(self, actual: Any, expected: Any, msg: str = None) -> bool:
        """断言等于"""
        try:
            assert actual == expected, \
                msg or f"值不匹配：期望 {expected}, 实际 {actual}"
            logger.debug(f"断言通过：{actual} == {expected}")
            return True
        except Exception as e:
            self._fail(msg or "值不匹配", e)
            return False

    def assert_not_equals(self, actual: Any, expected: Any, msg: str = None) -> bool:
        """断言不等于"""
        try:
            assert actual != expected, msg or f"值应不相等：{actual}"
            logger.debug(f"断言通过：{actual} != {expected}")
            return True
        except Exception as e:
            self._fail(msg or "值应不相等", e)
            return False

    def assert_true(self, condition: bool, msg: str = None) -> bool:
        """断言为真"""
        try:
            assert condition, msg or "条件应为真"
            logger.debug(f"断言通过：条件为真")
            return True
        except Exception as e:
            self._fail(msg or "条件应为真", e)
            return False

    def assert_false(self, condition: bool, msg: str = None) -> bool:
        """断言为假"""
        try:
            assert not condition, msg or "条件应为假"
            logger.debug(f"断言通过：条件为假")
            return True
        except Exception as e:
            self._fail(msg or "条件应为假", e)
            return False

    def assert_in(self, actual: Any, expected_collection: Any, msg: str = None) -> bool:
        """断言包含"""
        try:
            assert actual in expected_collection, \
                msg or f"'{actual}' 不在 '{expected_collection}' 中"
            logger.debug(f"断言通过：'{actual}' 在 '{expected_collection}' 中")
            return True
        except Exception as e:
            self._fail(msg or "值不在集合中", e)
            return False

    def assert_not_in(self, actual: Any, expected_collection: Any, msg: str = None) -> bool:
        """断言不包含"""
        try:
            assert actual not in expected_collection, \
                msg or f"'{actual}' 应在 '{expected_collection}' 中"
            logger.debug(f"断言通过：'{actual}' 不在 '{expected_collection}' 中")
            return True
        except Exception as e:
            self._fail(msg or "值应在集合中", e)
            return False

    def assert_greater_than(self, actual: Any, expected: Any, msg: str = None) -> bool:
        """断言大于"""
        try:
            assert actual > expected, \
                msg or f"值应大于：{actual} > {expected}"
            logger.debug(f"断言通过：{actual} > {expected}")
            return True
        except Exception as e:
            self._fail(msg or "值应大于期望值", e)
            return False

    def assert_less_than(self, actual: Any, expected: Any, msg: str = None) -> bool:
        """断言小于"""
        try:
            assert actual < expected, \
                msg or f"值应小于：{actual} < {expected}"
            logger.debug(f"断言通过：{actual} < {expected}")
            return True
        except Exception as e:
            self._fail(msg or "值应小于期望值", e)
            return False

    def assert_almost_equals(
        self,
        actual: float,
        expected: float,
        places: int = 7,
        msg: str = None
    ) -> bool:
        """断言浮点数近似相等"""
        try:
            assert round(actual - expected, places) == 0, \
                msg or f"值不近似：{actual} vs {expected}"
            logger.debug(f"断言通过：{actual} ≈ {expected}")
            return True
        except Exception as e:
            self._fail(msg or "值不近似", e)
            return False

    # ========== 内部方法 ==========

    def _fail(self, message: str, exception: Exception = None):
        """记录失败断言"""
        error_msg = message
        if exception:
            error_msg += f" | 异常：{type(exception).__name__}: {exception}"
        self.errors.append(error_msg)
        logger.error(f"断言失败：{error_msg}")

    def get_errors(self) -> List[str]:
        """获取所有错误信息"""
        return self.errors

    def clear_errors(self):
        """清空错误信息"""
        self.errors.clear()

    def verify_all(self) -> bool:
        """验证所有断言是否通过"""
        if self.errors:
            raise AssertionError(f"有 {len(self.errors)} 个断言失败：\n" + "\n".join(self.errors))
        return True


# ========== 快捷断言函数 ==========

def assert_equals(actual, expected, msg=None):
    """快捷断言：等于"""
    Assertion(None).assert_equals(actual, expected, msg)


def assert_true(condition, msg=None):
    """快捷断言：为真"""
    Assertion(None).assert_true(condition, msg)


def assert_false(condition, msg=None):
    """快捷断言：为假"""
    Assertion(None).assert_false(condition, msg)
