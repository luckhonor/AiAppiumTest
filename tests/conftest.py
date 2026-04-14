"""
Pytest 配置和 Fixture 管理
"""
import pytest
import os
import logging
from pathlib import Path
from utils.driver_factory import DriverFactory
from utils.logger import setup_logger, get_logger
from datetime import datetime

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
        default=None,
        help="设备 UDID"
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
def config(platform, env):
    """
    全局配置
    根据平台和环境加载配置
    """
    config_map = {
        "dev": {
            "appium_host": "127.0.0.1",
            "appium_port": 4723,
            "timeout": 30,
        },
        "test": {
            "appium_host": "127.0.0.1",
            "appium_port": 4723,
            "timeout": 60,
        },
        "prod": {
            "appium_host": "127.0.0.1",
            "appium_port": 4723,
            "timeout": 60,
        },
    }
    return config_map.get(env, config_map["dev"])


# ========== Driver 管理 ==========

@pytest.fixture(scope="function")
def driver(request, platform, config):
    """
    WebDriver Fixture
    每个测试用例独立使用一个 driver
    """
    app_path = request.config.getoption("--app")
    device_udid = request.config.getoption("--device")

    logger.info(f"创建 Driver: platform={platform}, device={device_udid}")

    drv = DriverFactory.get_driver(
        platform=platform,
        app_path=app_path,
        device_udid=device_udid,
        appium_host=config["appium_host"],
        appium_port=config["appium_port"],
        reuse=False
    )

    yield drv

    logger.info("测试完成，关闭 Driver")
    DriverFactory.quit_driver(drv)


@pytest.fixture(scope="session")
def driver_shared(platform, config):
    """
    共享 Driver Fixture
    多个测试用例共享一个 driver（慎用）
    """
    app_path = pytest.config.getoption("--app") if hasattr(pytest, "config") else None
    device_udid = pytest.config.getoption("--device") if hasattr(pytest, "config") else None

    logger.info(f"创建共享 Driver: platform={platform}")

    drv = DriverFactory.get_driver(
        platform=platform,
        app_path=app_path,
        device_udid=device_udid,
        appium_host=config["appium_host"],
        appium_port=config["appium_port"],
        reuse=True
    )

    yield drv

    logger.info("所有测试完成，关闭共享 Driver")
    DriverFactory.quit_all()


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
        if hasattr(item, "fixtures"):
            driver = item.funcargs.get("driver")

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

                # 附加到报告
                report.sections.append(("Screenshot", str(filepath)))

            except Exception as e:
                logger.error(f"截图失败：{e}")


# ========== 辅助 Fixture ==========

@pytest.fixture
def logger():
    """获取日志记录器"""
    return get_logger()


@pytest.fixture(scope="function")
def setup_and_teardown(driver):
    """
    前后置处理 Fixture
    可在其中添加测试前后的通用逻辑
    """
    # 前置处理
    logger.info("测试前置处理")

    yield driver

    # 后置处理
    logger.info("测试后置处理")
