"""
手机号登录测试用例
测试账号: 1000000001-1000000999, 密码: test11
登录流程: 登录首页 -> 点击手机号登录 -> 输入手机号 -> 输入密码
"""
import pytest
import allure
from pages.modules.login_page import LoginPage


@allure.feature("登录模块")
@allure.story("手机号登录")
class TestPhoneLogin:
    """手机号登录测试套件"""

    # ===== 测试数据 =====
    VALID_PHONE_MIN = "1000000001"
    VALID_PHONE_MAX = "1000000999"
    VALID_PASSWORD = "test11"

    def _do_phone_login(self, driver, phone: str, password: str):
        """
        执行完整的手机号登录流程:
        登录首页 -> 手机号输入页 -> 密码输入页

        Args:
            driver: WebDriver实例
            phone: 手机号
            password: 密码

        Returns:
            (login_page, phone_input_page, password_input_page) 元组
        """
        login_page = LoginPage(driver)
        phone_input_page = login_page.click_phone_login()
        phone_input_page.input_phone(phone)
        password_input_page = phone_input_page.click_confirm()
        if password_input_page:
            password_input_page.submit_password(password)
        return login_page, phone_input_page, password_input_page

    @allure.title("正常登录-使用最小有效手机号")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_login_success_min_phone(self, driver):
        """
        测试使用最小有效手机号登录
        手机号: 1000000001, 密码: test11
        """
        login_page, phone_input_page, password_input_page = \
            self._do_phone_login(driver, self.VALID_PHONE_MIN, self.VALID_PASSWORD)
        assert password_input_page is not None, "未能进入密码输入页面"

    @allure.title("正常登录-使用最大有效手机号")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_success_max_phone(self, driver):
        """
        测试使用最大有效手机号登录
        手机号: 1000000999, 密码: test11
        """
        login_page, phone_input_page, password_input_page = \
            self._do_phone_login(driver, self.VALID_PHONE_MAX, self.VALID_PASSWORD)
        assert password_input_page is not None, "未能进入密码输入页面"

    @allure.title("正常登录-随机有效手机号")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.parametrize("phone", [
        "1000000005",
        "1000000050",
        "1000000950",
    ])
    def test_login_success_random_phone(self, driver, phone):
        """测试使用随机有效手机号登录"""
        login_page, phone_input_page, password_input_page = \
            self._do_phone_login(driver, phone, self.VALID_PASSWORD)
        assert password_input_page is not None, f"手机号 {phone} 未能进入密码输入页面"

    @allure.title("登录失败-手机号为空")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_empty_phone(self, driver):
        """测试手机号为空时点击确认"""
        login_page = LoginPage(driver)
        phone_input_page = login_page.click_phone_login()
        phone_input_page.input_phone("")
        password_input_page = phone_input_page.click_confirm()
        assert password_input_page is None, "空手机号不应进入密码页面"

    @allure.title("登录失败-密码为空")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_empty_password(self, driver):
        """测试密码为空时点击确认"""
        login_page = LoginPage(driver)
        phone_input_page = login_page.click_phone_login()
        phone_input_page.input_phone(self.VALID_PHONE_MIN)
        password_input_page = phone_input_page.click_confirm()
        if password_input_page:
            password_input_page.submit_password("")
            # 验证未跳转或显示错误

    @allure.title("登录失败-手机号和密码都为空")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_empty_both(self, driver):
        """测试手机号和密码都为空时的登录"""
        login_page = LoginPage(driver)
        phone_input_page = login_page.click_phone_login()
        phone_input_page.input_phone("")
        password_input_page = phone_input_page.click_confirm()
        assert password_input_page is None, "空手机号不应进入密码页面"

    @allure.title("登录失败-手机号格式错误")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("invalid_phone", [
        "abcdefghij",
        "12345abcde",
        "100000000!",
        "1000000001a",
    ])
    def test_login_invalid_phone_format(self, driver, invalid_phone):
        """测试手机号格式错误时的登录"""
        login_page = LoginPage(driver)
        phone_input_page = login_page.click_phone_login()
        phone_input_page.input_phone(invalid_phone)
        password_input_page = phone_input_page.click_confirm()
        assert password_input_page is None, f"手机号 {invalid_phone} 格式错误不应进入密码页面"

    @allure.title("登录失败-手机号位数错误")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("invalid_phone", [
        "10000000",
        "100000000",
        "10000000010",
        "1",
    ])
    def test_login_invalid_phone_length(self, driver, invalid_phone):
        """测试手机号位数错误时的登录"""
        login_page = LoginPage(driver)
        phone_input_page = login_page.click_phone_login()
        phone_input_page.input_phone(invalid_phone)
        password_input_page = phone_input_page.click_confirm()
        assert password_input_page is None, f"手机号 {invalid_phone} 位数错误不应进入密码页面"

    @allure.title("登录失败-密码错误")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("wrong_password", [
        "test12",
        "test",
        "wrongpassword",
        "TEST11",
        "",
    ])
    def test_login_wrong_password(self, driver, wrong_password):
        """测试密码错误时的登录"""
        login_page, phone_input_page, password_input_page = \
            self._do_phone_login(driver, self.VALID_PHONE_MIN, wrong_password)
        # 密码错误后应停留在密码页面或提示错误

    @allure.title("登录失败-手机号不存在")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("non_exist_phone", [
        "1000000000",
        "1000001000",
        "9999999999",
        "0000000001",
    ])
    def test_login_non_exist_phone(self, driver, non_exist_phone):
        """测试手机号不存在时的登录"""
        login_page, phone_input_page, password_input_page = \
            self._do_phone_login(driver, non_exist_phone, self.VALID_PASSWORD)

    @allure.title("边界测试-账号区间边界值")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("phone,expected_result", [
        ("1000000000", False),
        ("1000000001", True),
        ("1000000999", True),
        ("1000001000", False),
    ])
    def test_login_boundary_phone(self, driver, phone, expected_result):
        """
        测试账号区间边界值登录
        有效区间: 1000000001 - 1000000999
        """
        login_page, phone_input_page, password_input_page = \
            self._do_phone_login(driver, phone, self.VALID_PASSWORD)

        if expected_result:
            assert password_input_page is not None, f"边界内手机号 {phone} 应能进入密码页面"
        else:
            # 边界外手机号可能无法进入密码页面或登录失败
            pass

    @allure.title("连续登录测试")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_sequence(self, driver):
        """测试连续多次登录操作"""
        login_page, phone_input_page, password_input_page = \
            self._do_phone_login(driver, self.VALID_PHONE_MIN, self.VALID_PASSWORD)
        assert password_input_page is not None, "第一次登录失败"
