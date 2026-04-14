"""
示例登录页面对象
用于演示 PageObject 模式
"""
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from typing import Optional


class LoginPage(BasePage):
    """登录页面"""

    # ===== 元素定位器 =====

    @property
    def username_input(self):
        """用户名输入框"""
        return (AppiumBy.ACCESSIBILITY_ID, "username")

    @property
    def password_input(self):
        """密码输入框"""
        return (AppiumBy.ACCESSIBILITY_ID, "password")

    @property
    def login_button(self):
        """登录按钮"""
        return (AppiumBy.ACCESSIBILITY_ID, "login")

    @property
    def error_message(self):
        """错误提示"""
        return (AppiumBy.ACCESSIBILITY_ID, "error_message")

    @property
    def forgot_password(self):
        """忘记密码"""
        return (AppiumBy.ACCESSIBILITY_ID, "forgot_password")

    # ===== 页面操作 =====

    def input_username(self, username: str) -> "LoginPage":
        """输入用户名"""
        self._input(self.username_input, username)
        return self

    def input_password(self, password: str) -> "LoginPage":
        """输入密码"""
        self._input(self.password_input, password)
        return self

    def click_login(self) -> Optional["HomePage"]:
        """点击登录"""
        self._click(self.login_button)
        # 导入避免循环依赖
        from pages.modules.home_page import HomePage
        return HomePage.verify_page(self.driver)

    def login(self, username: str, password: str) -> Optional["HomePage"]:
        """
        快捷登录方法

        Args:
            username: 用户名
            password: 密码

        Returns:
            HomePage 页面对象
        """
        self.input_username(username)
        self.input_password(password)
        return self.click_login()

    def get_error_message(self) -> str:
        """获取错误提示"""
        return self._get_text(self.error_message)

    def is_error_displayed(self) -> bool:
        """错误提示是否显示"""
        return self._is_displayed(self.error_message, timeout=3)

    def click_forgot_password(self) -> None:
        """点击忘记密码"""
        self._click(self.forgot_password)

    # ===== 页面验证 =====

    @classmethod
    def verify_page(cls, driver, timeout: int = 5) -> "LoginPage":
        """
        验证当前是登录页面

        Args:
            driver: WebDriver 实例
            timeout: 超时时间

        Returns:
            LoginPage 实例
        """
        instance = cls(driver)
        # 验证登录按钮存在
        instance._find_element(instance.login_button, timeout)
        return instance
