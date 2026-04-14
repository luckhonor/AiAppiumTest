"""
通用封装模块
"""
from common.gestures import Gestures
from common.waits import WaitStrategy
from common.assertions import Assertion
from common.text_locator import TextLocator

__all__ = ["Gestures", "WaitStrategy", "Assertion", "TextLocator"]
