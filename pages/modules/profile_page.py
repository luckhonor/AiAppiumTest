"""
示例个人中心页面对象
"""
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy


class ProfilePage(BasePage):
    """个人中心页面"""

    # ===== 元素定位器 =====

    @property
    def nickname(self):
        """昵称"""
        return (AppiumBy.ACCESSIBILITY_ID, "nickname")

    @property
    def settings_button(self):
        """设置按钮"""
        return (AppiumBy.ACCESSIBILITY_ID, "settings")

    # ===== 页面操作 =====

    def get_nickname(self) -> str:
        """获取昵称"""
        return self._get_text(self.nickname)

    def click_settings(self) -> "SettingsPage":
        """点击设置"""
        self._click(self.settings_button)
        from pages.modules.settings_page import SettingsPage
        return SettingsPage.verify_page(self.driver)

    # ===== 页面验证 =====

    @classmethod
    def verify_page(cls, driver, timeout: int = 5) -> "ProfilePage":
        """验证当前是个人中心页面"""
        instance = cls(driver)
        instance._find_element(instance.nickname, timeout)
        return instance
