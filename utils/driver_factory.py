"""
Driver 工厂模式
统一管理 WebDriver 的创建和销毁
"""
from appium.webdriver.webdriver import WebDriver
from appium import webdriver
from typing import Optional
import logging
from config.capabilities import ios_caps, android_caps

logger = logging.getLogger(__name__)


class DriverFactory:
    """Driver 工厂类"""

    _instances: dict = {}

    @classmethod
    def get_driver(
        cls,
        platform: str,
        app_path: Optional[str] = None,
        device_udid: Optional[str] = None,
        appium_host: str = "127.0.0.1",
        appium_port: int = 4723,
        reuse: bool = False
    ) -> WebDriver:
        """
        获取 WebDriver 实例

        Args:
            platform: 平台类型 'ios' 或 'android'
            app_path: App 路径
            device_udid: 设备 UDID
            appium_host: Appium Server 地址
            appium_port: Appium Server 端口
            reuse: 是否复用已有 driver

        Returns:
            WebDriver 实例
        """
        cache_key = f"{platform}_{device_udid or 'default'}"

        # 检查是否复用
        if reuse and cache_key in cls._instances:
            driver = cls._instances[cache_key]
            try:
                # 验证 driver 是否有效
                driver.current_activity
                logger.info(f"复用已有 Driver: {cache_key}")
                return driver
            except:
                logger.warning(f"Driver 已失效，重新创建：{cache_key}")
                cls._instances.pop(cache_key, None)

        # 创建新 Driver
        logger.info(f"创建新 Driver: platform={platform}, device={device_udid}")

        if platform.lower() == "ios":
            caps = ios_caps.get_ios_caps(app_path=app_path, device_udid=device_udid or "auto")
        elif platform.lower() == "android":
            caps = android_caps.get_android_caps(app_path=app_path, device_udid=device_udid or "emulator-5554")
        else:
            raise ValueError(f"不支持的平台：{platform}")

        server_url = f"http://{appium_host}:{appium_port}"

        try:
            driver = webdriver.Remote(server_url, caps)
            logger.info(f"Driver 创建成功：{driver.session_id}")

            if reuse:
                cls._instances[cache_key] = driver

            return driver

        except Exception as e:
            logger.error(f"Driver 创建失败：{e}")
            raise

    @classmethod
    def quit_driver(cls, driver: WebDriver):
        """安全关闭 Driver"""
        if driver:
            try:
                driver.quit()
                logger.info("Driver 已关闭")
            except Exception as e:
                logger.warning(f"关闭 Driver 异常：{e}")

    @classmethod
    def quit_all(cls):
        """关闭所有 Driver 实例"""
        for key, driver in list(cls._instances.items()):
            logger.info(f"关闭 Driver: {key}")
            cls.quit_driver(driver)
        cls._instances.clear()
