"""
手机号输入页面
针对 in.dradhanus.liveher 应用的手机号登录-输入手机号页面
控件ID来源: appPage.md 第2部分
"""
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from typing import Optional


class PhoneInputPage(BasePage):
    """手机号输入页面"""

    # ===== 元素定位器 =====
    _package = "in.dradhanus.liveher"

    @property
    def phone_input(self):
        """手机号输入框"""
        return (AppiumBy.ID, f"{self._package}:id/edtPhoneloginNumber")

    @property
    def confirm_button(self):
        """确认按钮"""
        return (AppiumBy.ID, f"{self._package}:id/txtPhoneloginLogin")

    @property
    def country_code_button(self):
        """国家区号按钮（默认+86）"""
        return (AppiumBy.ID, f"{self._package}:id/ftvFlagCode")

    # ===== 页面操作 =====

    def input_phone(self, phone: str) -> "PhoneInputPage":
        """输入手机号"""
        self._input(self.phone_input, phone)
        return self

    def click_confirm(self) -> Optional["PasswordInputPage"]:
        """点击确认按钮，进入密码输入页面"""
        self._click(self.confirm_button)
        from pages.modules.password_input_page import PasswordInputPage
        try:
            return PasswordInputPage.verify_page(self.driver, timeout=5)
        except Exception:
            return None

    def click_country_code(self) -> "PhoneInputPage":
        """点击国家区号按钮"""
        self._click(self.country_code_button)
        return self

    def clear_phone(self) -> "PhoneInputPage":
        """清空手机号"""
        self._find_element(self.phone_input).clear()
        return self

    def submit_phone(self, phone: str) -> Optional["PasswordInputPage"]:
        """
        输入手机号并提交

        Args:
            phone: 手机号码

        Returns:
            PasswordInputPage 页面对象，失败返回 None
        """
        self.input_phone(phone)
        return self.click_confirm()

    # ===== 页面验证 =====

    @classmethod
    def verify_page(cls, driver, timeout: int = 5) -> "PhoneInputPage":
        """验证当前是手机号输入页面"""
        instance = cls(driver)
        instance._find_element(instance.phone_input, timeout)
        instance._find_element(instance.confirm_button, timeout)
        return instance
