"""
Android Desired Capabilities 配置
"""


def get_android_caps(app_path: str = None, device_udid: str = "emulator-5554") -> dict:
    """
    获取 Android 设备配置

    Args:
        app_path: .apk 文件路径
        device_udid: 设备 UDID

    Returns:
        Android capabilities 字典
    """
    caps = {
        "platformName": "Android",
        "platformVersion": "14",
        "deviceName": "Pixel 8",
        "automationName": "UiAutomator2",
        "udid": device_udid,

        # App 配置
        "app": app_path,
        # "appPackage": "com.example",
        # "appActivity": ".MainActivity",

        # 性能优化
        "newCommandTimeout": 300,
        "waitForIdleTimeout": 10,
        "waitForSelectorTimeout": 5000,

        # 元素定位优化
        "allowInvisibleElements": False,
        "ignoreUnimportantViews": True,

        # UiAutomator2 特有配置
        "disableWindowAnimation": True,
        "skipUnlock": False,
        "unlockStrategy": "swipe",

        # 截图配置
        "nativeWebScreenshot": False,
    }

    return caps


def get_android_web_caps(device_udid: str = "emulator-5554") -> dict:
    """获取 Android Chrome Web 配置"""
    caps = get_android_caps(device_udid=device_udid)
    caps.pop("app", None)
    caps.pop("appPackage", None)
    caps.pop("appActivity", None)
    caps["browserName"] = "Chrome"
    return caps
