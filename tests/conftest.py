"""
Pytest 配置和 Fixture 管理
每个测试用例执行后重置App数据
"""
import pytest
import os
import sys
import logging
import subprocess
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.driver_factory import DriverFactory
from utils.logger import setup_logger, get_logger
from config.capabilities.android_caps import get_android_caps

# 初始化日志
setup_logger()
logger = get_logger(__name__)


# ========== 命令行参数 ==========

def pytest_addoption(parser):
    """添加命令行参数"""
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        help="测试平台：ios 或 android"
    )
    parser.addoption(
        "--device",
        action="store",
        default="192.168.3.9:5555",
        help="设备地址或 UDID"
    )
    parser.addoption(
        "--app",
        action="store",
        default=None,
        help="App 路径"
    )
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="环境：dev/test/prod"
    )
    parser.addoption(
        "--appium-host",
        action="store",
        default="127.0.0.1",
        help="Appium Server 地址"
    )
    parser.addoption(
        "--appium-port",
        action="store",
        default=4723,
        type=int,
        help="Appium Server 端口"
    )
    parser.addoption(
        "--no-reset",
        action="store_true",
        default=False,
        help="不重置App数据（默认每个用例后重置）"
    )


# ========== Session 级 Fixture ==========

@pytest.fixture(scope="session")
def platform(request):
    """获取测试平台"""
    return request.config.getoption("--platform")


@pytest.fixture(scope="session")
def env(request):
    """获取测试环境"""
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def appium_host(request):
    """获取 Appium Server 地址"""
    return request.config.getoption("--appium-host")


@pytest.fixture(scope="session")
def appium_port(request):
    """获取 Appium Server 端口"""
    return request.config.getoption("--appium-port")


@pytest.fixture(scope="session")
def no_reset(request):
    """是否跳过App数据重置"""
    return request.config.getoption("--no-reset")


@pytest.fixture(scope="session")
def app_package():
    """获取App包名"""
    return "in.dradhanus.liveher"


@pytest.fixture(scope="session")
def config(platform, env, appium_host, appium_port, no_reset):
    """
    全局配置
    """
    return {
        "platform": platform,
        "env": env,
        "appium_host": appium_host,
        "appium_port": appium_port,
        "timeout": 30,
        "no_reset": no_reset,
    }


# ========== App 数据重置 ==========

def reset_app_data(driver, app_package: str, device: str = None):
    """
    重置App数据，确保每个用例从干净状态开始

    Args:
        driver: WebDriver实例
        app_package: App包名
        device: 设备地址（用于adb命令）
    """
    logger.info(f"重置App数据: {app_package}")

    try:
        # 方法1: 使用Appium的reset方法（推荐）
        driver.reset()
        logger.info("App数据重置成功（通过driver.reset）")
        return True
    except Exception as e:
        logger.warning(f"driver.reset失败: {e}")

    try:
        # 方法2: 使用adb清除数据
        adb_cmd = ["adb"]
        if device:
            adb_cmd.extend(["-s", device])
        adb_cmd.extend(["shell", "pm", "clear", app_package])

        result = subprocess.run(adb_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            logger.info("App数据重置成功（通过adb pm clear）")
            return True
        else:
            logger.warning(f"adb清除失败: {result.stderr}")
    except Exception as e:
        logger.warning(f"adb命令执行失败: {e}")

    try:
        # 方法3: 使用Appium execute_script
        driver.execute_script('mobile: shell', {
            'command': f'pm clear {app_package}'
        })
        logger.info("App数据重置成功（通过mobile: shell）")
        return True
    except Exception as e:
        logger.warning(f"mobile: shell失败: {e}")

    logger.error("App数据重置失败")
    return False


def launch_app(driver):
    """
    重新启动App
    """
    logger.info("重新启动App")
    try:
        driver.activate_app("in.dradhanus.liveher")
        logger.info("App启动成功")
    except Exception as e:
        logger.warning(f"启动App失败: {e}")


# ========== Driver 管理 ==========

@pytest.fixture(scope="function")
def driver(request, config, app_package):
    """
    WebDriver Fixture
    每个测试用例独立使用一个 driver
    每个用例执行后重置App数据
    """
    platform = config["platform"]
    app_path = request.config.getoption("--app")
    device_udid = request.config.getoption("--device")

    logger.info(f"创建 Driver: platform={platform}, device={device_udid}")

    # 使用用户配置创建 driver
    from appium import webdriver

    caps = get_android_caps(app_path=app_path, device_udid=device_udid)

    driver_url = f"http://{config['appium_host']}:{config['appium_port']}"

    try:
        drv = webdriver.Remote(driver_url, options=caps)
        logger.info("Driver 创建成功")
    except Exception as e:
        logger.error(f"Driver 创建失败: {e}")
        raise

    yield drv

    # 测试完成后重置App数据
    if not config["no_reset"]:
        logger.info("测试完成，重置App数据")
        try:
            reset_app_data(drv, app_package, device_udid)
            # 重置后需要等待App重新启动或重新初始化
        except Exception as e:
            logger.warning(f"重置App数据时出错: {e}")

    logger.info("关闭 Driver")
    try:
        drv.quit()
    except Exception as e:
        logger.warning(f"关闭 Driver 时出错: {e}")


@pytest.fixture(scope="class")
def driver_class(request, config, app_package):
    """
    类级别 Driver Fixture
    一个测试类共享一个 driver
    每个用例之间手动重置App数据（需要在用例中调用）
    """
    platform = config["platform"]
    app_path = request.config.getoption("--app")
    device_udid = request.config.getoption("--device")

    logger.info(f"创建类级别 Driver: platform={platform}")

    from appium import webdriver

    caps = get_android_caps(app_path=app_path, device_udid=device_udid)
    driver_url = f"http://{config['appium_host']}:{config['appium_port']}"

    drv = webdriver.Remote(driver_url, options=caps)

    # 将driver和配置绑定到测试类，方便用例中重置
    request.cls.driver = drv
    request.cls.app_package = app_package
    request.cls.device_udid = device_udid
    request.cls.reset_app = lambda: reset_app_data(drv, app_package, device_udid)

    yield drv

    logger.info("测试类完成，关闭 Driver")
    drv.quit()


# ========== 用例级别重置 Fixture ==========

@pytest.fixture(scope="function", autouse=True)
def reset_app_state(request, driver, config, app_package):
    """
    自动在每个用例执行前重置App状态
    确保用例之间数据隔离
    """
    # 前置：确保App处于登录页面初始状态
    if not config["no_reset"]:
        # 检查是否是第一个用例（driver刚创建）
        # 如果不是，需要重置并重启App
        pass  # driver fixture已处理重置

    yield

    # 后置：重置App数据（在driver fixture中处理）


@pytest.fixture(scope="function")
def reset_app(driver, app_package):
    """
    手动重置App数据的Fixture
    在用例中可调用此函数强制重置
    """
    def do_reset():
        return reset_app_data(driver, app_package)
    return do_reset


# ========== 截图和日志 ==========

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试失败时自动截图
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # 获取 driver
        driver = None
        if "driver" in item.funcargs:
            driver = item.funcargs["driver"]

        if driver:
            try:
                # 截图保存
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_dir = Path("reports/failures")
                screenshot_dir.mkdir(parents=True, exist_ok=True)

                filename = f"{item.name}_{timestamp}.png"
                filepath = screenshot_dir / filename

                driver.save_screenshot(str(filepath))
                logger.error(f"测试失败，截图保存：{filepath}")

                # 附加到 Allure 报告
                if hasattr(report, "sections"):
                    report.sections.append(("Screenshot", str(filepath)))

                # 使用 allure 附加截图
                import allure
                with open(filepath, "rb") as f:
                    allure.attach(f.read(), name="失败截图",
                                 attachment_type=allure.attachment_type.PNG)

            except Exception as e:
                logger.error(f"截图失败：{e}")


# ========== 辅助 Fixture ==========

@pytest.fixture
def test_logger():
    """获取日志记录器"""
    return get_logger()


@pytest.fixture(scope="function")
def login_page(driver):
    """获取登录首页页面对象"""
    from pages.modules.login_page import LoginPage
    return LoginPage(driver)


@pytest.fixture(scope="function")
def phone_input_page(driver):
    """获取手机号输入页面对象"""
    from pages.modules.phone_input_page import PhoneInputPage
    return PhoneInputPage(driver)


@pytest.fixture(scope="function")
def password_input_page(driver):
    """获取密码输入页面对象"""
    from pages.modules.password_input_page import PasswordInputPage
    return PasswordInputPage(driver)


@pytest.fixture(scope="function")
def home_page(driver):
    """获取首页页面对象"""
    from pages.modules.home_page import HomePage
    return HomePage(driver)