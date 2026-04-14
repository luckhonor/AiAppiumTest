"""
示例首页页面对象
用于演示 PageObject 模式
"""
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy


class HomePage(BasePage):
    """首页"""

    # ===== 元素定位器 =====

    @property
    def welcome_text(self):
        """欢迎文本"""
        return (AppiumBy.ACCESSIBILITY_ID, "welcome_text")

    @property
    def logout_button(self):
        """退出登录按钮"""
        return (AppiumBy.ACCESSIBILITY_ID, "logout")

    @property
    def profile_icon(self):
        """个人中心图标"""
        return (AppiumBy.ACCESSIBILITY_ID, "profile")

    # ===== 页面操作 =====

    def get_welcome_text(self) -> str:
        """获取欢迎文本"""
        return self._get_text(self.welcome_text)

    def is_welcome_displayed(self) -> bool:
        """欢迎文本是否显示"""
        return self._is_displayed(self.welcome_text)

    def click_logout(self) -> "LoginPage":
        """点击退出登录"""
        self._click(self.logout_button)
        from pages.modules.login_page import LoginPage
        return LoginPage.verify_page(self.driver)

    def click_profile(self) -> "ProfilePage":
        """点击个人中心"""
        self._click(self.profile_icon)
        from pages.modules.profile_page import ProfilePage
        return ProfilePage.verify_page(self.driver)

    # ===== 页面验证 =====

    @classmethod
    def verify_page(cls, driver, timeout: int = 5) -> "HomePage":
        """
        验证当前是首页

        Args:
            driver: WebDriver 实例
            timeout: 超时时间

        Returns:
            HomePage 实例
        """
        instance = cls(driver)
        instance._find_element(instance.welcome_text, timeout)
        return instance
