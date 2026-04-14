"""
登录首页 - 选择登录方式页面
针对 in.dradhanus.liveher 应用的登录方式选择页面
控件ID来源: appPage.md 第1部分
"""
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from typing import Optional


class LoginPage(BasePage):
    """登录首页 - 选择登录方式"""

    # ===== 元素定位器 =====
    _package = "in.dradhanus.liveher"

    @property
    def facebook_login_button(self):
        """Facebook登录按钮"""
        return (AppiumBy.ID, f"{self._package}:id/mTxtContinueWithFb")

    @property
    def google_login_button(self):
        """Google登录按钮"""
        return (AppiumBy.ID, f"{self._package}:id/mTxtContinueWithGoogle")

    @property
    def phone_login_button(self):
        """手机号登录按钮"""
        return (AppiumBy.ID, f"{self._package}:id/imgLoginPhoneLayout")

    @property
    def email_login_button(self):
        """邮箱登录按钮"""
        return (AppiumBy.ID, f"{self._package}:id/imgLoginEmailLayout")

    # ===== 页面操作 =====

    def click_facebook_login(self):
        """点击Facebook登录"""
        self._click(self.facebook_login_button)

    def click_google_login(self):
        """点击Google登录"""
        self._click(self.google_login_button)

    def click_phone_login(self) -> "PhoneInputPage":
        """点击手机号登录，进入手机号输入页面"""
        self._click(self.phone_login_button)
        from pages.modules.phone_input_page import PhoneInputPage
        return PhoneInputPage.verify_page(self.driver)

    def click_email_login(self):
        """点击邮箱登录"""
        self._click(self.email_login_button)

    # ===== 页面验证 =====

    @classmethod
    def verify_page(cls, driver, timeout: int = 5) -> "LoginPage":
        """验证当前是登录首页"""
        instance = cls(driver)
        instance._find_element(instance.phone_login_button, timeout)
        return instance
