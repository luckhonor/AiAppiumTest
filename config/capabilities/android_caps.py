"""
Android Desired Capabilities 配置
使用 UiAutomator2Options 适配 Appium Python Client v3+
"""
from appium.options.android import UiAutomator2Options


# 用户提供的设备配置
USER_CAPS = {
    "platformName": "Android",
    "appium:platformVersion": "12",
    "appium:deviceName": "192.168.3.9:5555",
    "appium:appPackage": "in.dradhanus.liveher",
    "appium:appActivity": "in.dradhanus.liveher.SplashActivity",
    "appium:automationName": "UIAutomator2",
}


def get_android_caps(app_path: str = None,
                     device_udid: str = None,
                     no_reset: bool = False,
                     full_reset: bool = False) -> UiAutomator2Options:
    """
    获取 Android 设备配置（返回 UiAutomator2Options 对象）
    """
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "12"
    options.device_name = device_udid or "192.168.3.9:5555"
    options.app_package = "in.dradhanus.liveher"
    options.app_activity = "in.dradhanus.liveher.SplashActivity"
    options.automation_name = "UIAutomator2"

    if app_path:
        options.app = app_path

    options.no_reset = no_reset
    options.full_reset = full_reset

    # 性能优化
    options.new_command_timeout = 300
    options.auto_accept_alerts = True

    return options