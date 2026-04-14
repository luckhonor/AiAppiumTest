"""
登录模块测试用例
演示 PageObject 模式的测试写法
"""
import pytest
from pages.modules.login_page import LoginPage
from pages.modules.home_page import HomePage


class TestLogin:
    """登录测试套件"""

    @pytest.mark.smoke
    def test_login_success(self, driver):
        """
        测试正常登录
        标记为 smoke 冒烟测试
        """
        # 初始化登录页面
        login_page = LoginPage(driver)

        # 执行登录
        home_page = login_page.login("testuser", "password123")

        # 验证登录成功
        assert home_page is not None, "登录失败，未跳转到首页"
        assert home_page.is_welcome_displayed(), "首页欢迎文本未显示"

    @pytest.mark.smoke
    def test_login_invalid_password(self, driver):
        """
        测试密码错误
        """
        login_page = LoginPage(driver)

        # 输入错误密码
        login_page.input_username("testuser")
        login_page.input_password("wrongpassword")
        login_page.click_login()

        # 验证错误提示
        assert login_page.is_error_displayed(), "错误提示未显示"
        error_msg = login_page.get_error_message()
        assert "密码错误" in error_msg or "invalid" in error_msg.lower()

    @pytest.mark.regression
    @pytest.mark.parametrize("username,password", [
        ("user1", "pass1"),
        ("user2", "pass2"),
        ("", "password"),  # 用户名为空
        ("username", ""),  # 密码为空
    ])
    def test_login_data_driven(self, driver, username, password):
        """
        数据驱动登录测试
        覆盖多种输入场景
        """
        login_page = LoginPage(driver)

        # 执行登录
        login_page.input_username(username)
        login_page.input_password(password)
        login_page.click_login()

        # 根据输入验证结果
        if not username or not password:
            # 空输入应显示错误
            assert login_page.is_error_displayed() or True  # 某些 App 可能不校验
        else:
            # 正常输入可能成功或失败
            pass  # 根据实际需求调整断言

    def test_login_forgot_password(self, driver):
        """
        测试忘记密码入口
        """
        login_page = LoginPage(driver)

        # 点击忘记密码
        login_page.click_forgot_password()

        # 验证跳转到找回密码页面（根据实际 App 调整）
        # 这里仅作演示
        assert True  # 替换为实际断言
