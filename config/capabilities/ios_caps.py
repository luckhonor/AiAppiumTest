"""
iOS Desired Capabilities 配置
"""


def get_ios_caps(app_path: str = None, device_udid: str = "auto") -> dict:
    """
    获取 iOS 设备配置

    Args:
        app_path: .app 文件路径
        device_udid: 设备 UDID

    Returns:
        iOS capabilities 字典
    """
    caps = {
        "platformName": "iOS",
        "platformVersion": "17.0",
        "deviceName": "iPhone 15",
        "automationName": "XCUITest",
        "udid": device_udid,

        # App 配置
        "app": app_path,

        # 性能优化
        "newCommandTimeout": 300,
        "waitForQuiescence": True,
        "waitForIdleTimeout": 10,

        # 元素定位优化
        "includeNonVisibleElements": True,
        "simpleIsVisibleCheck": False,

        # 日志配置
        "showIOSLog": False,
        "showXcodeLog": False,

        # 截图配置
        "nativeInvisibleElements": False,
        "screenshotQuality": 2,
    }

    return caps


def get_ios_web_caps(device_udid: str = "auto") -> dict:
    """获取 iOS Safari Web 配置"""
    caps = get_ios_caps(device_udid=device_udid)
    caps.pop("app", None)
    caps["browserName"] = "Safari"
    return caps
