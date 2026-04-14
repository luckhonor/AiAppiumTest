"""
通用手势操作封装
支持滑动、长按、拖动、缩放等操作
"""
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.touch_actions import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class Gestures:
    """手势操作工具类"""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def _get_window_size(self) -> Tuple[int, int]:
        """获取窗口大小"""
        size = self.driver.get_window_size()
        return size["width"], size["height"]

    def _get_element_center(self, locator: tuple) -> Tuple[int, int]:
        """获取元素中心点坐标"""
        element = self.driver.find_element(*locator)
        location = element.location
        size = element.size
        x = location["x"] + size["width"] // 2
        y = location["y"] + size["height"] // 2
        return x, y

    # ========== 滑动操作 ==========

    def swipe(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: int = 500
    ):
        """基础滑动"""
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        logger.debug(f"滑动：({start_x}, {start_y}) -> ({end_x}, {end_y})")

    def swipe_up(self, percent: float = 0.7, duration: int = 500):
        """
        向上滑动（从下往上）
        percent: 滑动起始位置百分比
        """
        width, height = self._get_window_size()
        start_y = int(height * percent)
        end_y = int(height * (1 - percent))
        center_x = width // 2
        self.swipe(center_x, start_y, center_x, end_y, duration)

    def swipe_down(self, percent: float = 0.7, duration: int = 500):
        """向下滑动（从上往下）"""
        width, height = self._get_window_size()
        start_y = int(height * (1 - percent))
        end_y = int(height * percent)
        center_x = width // 2
        self.swipe(center_x, start_y, center_x, end_y, duration)

    def swipe_left(self, percent: float = 0.7, duration: int = 500):
        """向左滑动（从右往左）"""
        width, height = self._get_window_size()
        start_x = int(width * percent)
        end_x = int(width * (1 - percent))
        center_y = height // 2
        self.swipe(start_x, center_y, end_x, center_y, duration)

    def swipe_right(self, percent: float = 0.7, duration: int = 500):
        """向右滑动（从左往右）"""
        width, height = self._get_window_size()
        start_x = int(width * (1 - percent))
        end_x = int(width * percent)
        center_y = height // 2
        self.swipe(start_x, center_y, end_x, center_y, duration)

    def swipe_until(
        self,
        direction: str,
        check_locator: tuple,
        max_swipes: int = 10,
        percent: float = 0.7,
        duration: int = 500
    ) -> bool:
        """
        滑动直到元素出现

        Args:
            direction: 滑动方向 (up/down/left/right)
            check_locator: 要查找的元素定位器
            max_swipes: 最大滑动次数
            percent: 滑动百分比
            duration: 滑动持续时间

        Returns:
            是否找到元素
        """
        swipe_map = {
            "up": self.swipe_up,
            "down": self.swipe_down,
            "left": self.swipe_left,
            "right": self.swipe_right,
        }

        swipe_func = swipe_map.get(direction.lower())
        if not swipe_func:
            raise ValueError(f"不支持的滑动方向：{direction}")

        for i in range(max_swipes):
            logger.debug(f"第 {i + 1} 次滑动")
            try:
                element = self.driver.find_element(*check_locator)
                if element.is_displayed():
                    logger.info(f"滑动 {i + 1} 次后找到元素")
                    return True
            except:
                pass

            swipe_func(percent, duration)

        logger.warning(f"滑动 {max_swipes} 次后未找到元素")
        return False

    # ========== 长按操作 ==========

    def long_press(self, locator: tuple, duration: int = 2000):
        """长按元素"""
        x, y = self._get_element_center(locator)
        action = TouchAction(self.driver)
        action.long_press(x=x, y=y, duration=duration).release().perform()
        logger.debug(f"长按元素：({x}, {y}), 时长：{duration}ms")

    def long_press_by_coord(self, x: int, y: int, duration: int = 2000):
        """按坐标长按"""
        action = TouchAction(self.driver)
        action.long_press(x=x, y=y, duration=duration).release().perform()
        logger.debug(f"长按坐标：({x}, {y}), 时长：{duration}ms")

    # ========== 点击操作 ==========

    def tap(self, locator: tuple):
        """点击元素"""
        x, y = self._get_element_center(locator)
        action = TouchAction(self.driver)
        action.tap(x=x, y=y).perform()
        logger.debug(f"点击元素：({x}, {y})")

    def tap_by_coord(self, x: int, y: int):
        """按坐标点击"""
        action = TouchAction(self.driver)
        action.tap(x=x, y=y).perform()
        logger.debug(f"点击坐标：({x}, {y})")

    def double_tap(self, locator: tuple):
        """双击元素"""
        x, y = self._get_element_center(locator)
        action = TouchAction(self.driver)
        action.tap(x=x, y=y, count=2).perform()
        logger.debug(f"双击元素：({x}, {y})")

    # ========== 拖动操作 ==========

    def drag_and_drop(self, from_locator: tuple, to_locator: tuple, duration: int = 500):
        """拖动元素"""
        from_x, from_y = self._get_element_center(from_locator)
        to_x, to_y = self._get_element_center(to_locator)

        action = TouchAction(self.driver)
        action.long_press(x=from_x, y=from_y, duration=duration)
        action.move(x=to_x, y=to_y).release().perform()
        logger.debug(f"拖动：({from_x}, {from_y}) -> ({to_x}, {to_y})")

    # ========== 缩放操作 ==========

    def zoom_in(self, center_x: Optional[int] = None, center_y: Optional[int] = None, zoom_percent: float = 0.5):
        """双指放大"""
        width, height = self._get_window_size()
        cx = center_x or width // 2
        cy = center_y or height // 2

        offset_x = int(width * zoom_percent / 2)
        offset_y = int(height * zoom_percent / 2)

        # 双指从中心向外展开
        multi_action = MultiAction(self.driver)

        action1 = TouchAction(self.driver)
        action1.long_press(x=cx - offset_x, y=cy - offset_y).move(x=cx + offset_x, y=cy + offset_y)

        action2 = TouchAction(self.driver)
        action2.long_press(x=cx + offset_x, y=cy + offset_y).move(x=cx - offset_x, y=cy - offset_y)

        multi_action.add(action1, action2)
        multi_action.perform()
        logger.debug("执行放大手势")

    def zoom_out(self, center_x: Optional[int] = None, center_y: Optional[int] = None, zoom_percent: float = 0.5):
        """双指缩小"""
        width, height = self._get_window_size()
        cx = center_x or width // 2
        cy = center_y or height // 2

        offset_x = int(width * zoom_percent / 2)
        offset_y = int(height * zoom_percent / 2)

        # 双指从外向内合拢
        multi_action = MultiAction(self.driver)

        action1 = TouchAction(self.driver)
        action1.long_press(x=cx - offset_x, y=cy - offset_y).move(x=cx + offset_x, y=cy + offset_y)

        action2 = TouchAction(self.driver)
        action2.long_press(x=cx + offset_x, y=cy + offset_y).move(x=cx - offset_x, y=cy - offset_y)

        multi_action.add(action1, action2)
        multi_action.perform()
        logger.debug("执行缩小手势")

    # ========== 滚动操作 ==========

    def scroll_to_element(self, locator: tuple, direction: str = "down", max_swipes: int = 10) -> bool:
        """
        滚动到指定元素

        Args:
            locator: 目标元素定位器
            direction: 滚动方向
            max_swipes: 最大滚动次数
        """
        return self.swipe_until(direction, locator, max_swipes)
