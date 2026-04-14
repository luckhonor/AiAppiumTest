"""
登录模块测试用例
演示 PageObject 模式的测试写法
登录流程: 登录首页 -> 选择登录方式
"""
import pytest
from pages.modules.login_page import LoginPage


class TestLogin:
    """登录测试套件"""

    @pytest.mark.smoke
    def test_phone_login_entry(self, driver):
        """
        测试手机号登录入口
        验证点击手机号登录后能进入手机号输入页面
        """
        login_page = LoginPage(driver)
        phone_input_page = login_page.click_phone_login()
        assert phone_input_page is not None, "未能进入手机号输入页面"

    @pytest.mark.smoke
    def test_login_page_elements(self, driver):
        """
        测试登录首页元素是否存在
        验证四个登录方式按钮都存在
        """
        login_page = LoginPage(driver)

        assert login_page._is_displayed(login_page.facebook_login_button), \
            "Facebook登录按钮未显示"
        assert login_page._is_displayed(login_page.google_login_button), \
            "Google登录按钮未显示"
        assert login_page._is_displayed(login_page.phone_login_button), \
            "手机号登录按钮未显示"
        assert login_page._is_displayed(login_page.email_login_button), \
            "邮箱登录按钮未显示"

    @pytest.mark.regression
    def test_facebook_login_entry(self, driver):
        """测试Facebook登录入口"""
        login_page = LoginPage(driver)
        login_page.click_facebook_login()

    @pytest.mark.regression
    def test_google_login_entry(self, driver):
        """测试Google登录入口"""
        login_page = LoginPage(driver)
        login_page.click_google_login()

    @pytest.mark.regression
    def test_email_login_entry(self, driver):
        """测试邮箱登录入口"""
        login_page = LoginPage(driver)
        login_page.click_email_login()
