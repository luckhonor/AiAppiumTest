"""
密码输入页面
针对 in.dradhanus.liveher 应用的手机号登录-输入密码页面
控件ID来源: appPage.md 第3部分
"""
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from typing import Optional


class PasswordInputPage(BasePage):
    """密码输入页面"""

    # ===== 元素定位器 =====
    _package = "in.dradhanus.liveher"

    @property
    def password_input(self):
        """密码输入框"""
        return (AppiumBy.ID, f"{self._package}:id/edtPassword")

    @property
    def confirm_button(self):
        """确认按钮"""
        return (AppiumBy.ID, f"{self._package}:id/txtConfirm")

    # ===== 页面操作 =====

    def input_password(self, password: str) -> "PasswordInputPage":
        """输入密码"""
        self._input(self.password_input, password)
        return self

    def click_confirm(self):
        """点击确认按钮"""
        self._click(self.confirm_button)

    def clear_password(self) -> "PasswordInputPage":
        """清空密码"""
        self._find_element(self.password_input).clear()
        return self

    def submit_password(self, password: str):
        """
        输入密码并提交

        Args:
            password: 登录密码
        """
        self.input_password(password)
        self.click_confirm()

    # ===== 页面验证 =====

    @classmethod
    def verify_page(cls, driver, timeout: int = 5) -> "PasswordInputPage":
        """验证当前是密码输入页面"""
        instance = cls(driver)
        instance._find_element(instance.password_input, timeout)
        instance._find_element(instance.confirm_button, timeout)
        return instance
