"""
示例设置页面对象
"""
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy


class SettingsPage(BasePage):
    """设置页面"""

    # ===== 元素定位器 =====

    @property
    def switch_notification(self):
        """通知开关"""
        return (AppiumBy.ACCESSIBILITY_ID, "switch_notification")

    @property
    def back_button(self):
        """返回按钮"""
        return (AppiumBy.ACCESSIBILITY_ID, "back")

    # ===== 页面操作 =====

    def toggle_notification(self, enable: bool):
        """切换通知开关"""
        # 获取当前状态
        switch = self._find_element(self.switch_notification)
        is_checked = switch.get_attribute("checked") == "true"

        # 如果状态不一致，点击切换
        if is_checked != enable:
            self._click(self.switch_notification)

    def go_back(self) -> "ProfilePage":
        """返回上一页"""
        self._click(self.back_button)
        from pages.modules.profile_page import ProfilePage
        return ProfilePage.verify_page(self.driver)

    # ===== 页面验证 =====

    @classmethod
    def verify_page(cls, driver, timeout: int = 5) -> "SettingsPage":
        """验证当前是设置页面"""
        instance = cls(driver)
        instance._find_element(instance.switch_notification, timeout)
        return instance
