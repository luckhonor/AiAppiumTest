"""
首页页面对象
针对 in.dradhanus.liveher 应用的首页
"""
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from typing import Optional


class HomePage(BasePage):
    """首页"""

    # ===== 元素定位器 =====
    # 基于 appPage.md 中定义的控件ID
    _package = "in.dradhanus.liveher"

    @property
    def welcome_text(self):
        """欢迎文本"""
        return (AppiumBy.ID, f"{self._package}:id/tv_welcome")

    @property
    def user_avatar(self):
        """用户头像"""
        return (AppiumBy.ID, f"{self._package}:id/iv_avatar")

    @property
    def profile_icon(self):
        """个人中心入口"""
        return (AppiumBy.ID, f"{self._package}:id/iv_profile")

    # 注意：退出按钮未在appPage.md定义，需从Appium Inspector获取实际ID
    # 暂时保留占位，实际运行时需要确认正确ID
    @property
    def logout_button(self):
        """退出登录按钮 - 需确认实际控件ID"""
        return (AppiumBy.ID, f"{self._package}:id/btn_logout")

    # ===== 页面操作 =====

    def get_welcome_text(self) -> str:
        """获取欢迎文本"""
        return self._get_text(self.welcome_text)

    def is_welcome_displayed(self) -> bool:
        """欢迎文本是否显示"""
        return self._is_displayed(self.welcome_text)

    def click_profile(self) -> Optional["ProfilePage"]:
        """点击个人中心"""
        self._click(self.profile_icon)
        from pages.modules.profile_page import ProfilePage
        try:
            return ProfilePage.verify_page(self.driver)
        except Exception:
            return None

    def click_logout(self) -> Optional["LoginPage"]:
        """点击退出登录"""
        self._click(self.logout_button)
        from pages.modules.login_page import LoginPage
        try:
            return LoginPage.verify_page(self.driver)
        except Exception:
            return None

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
        # 验证欢迎文本或用户头像存在
        try:
            instance._find_element(instance.welcome_text, timeout)
        except Exception:
            instance._find_element(instance.user_avatar, timeout)
        return instance