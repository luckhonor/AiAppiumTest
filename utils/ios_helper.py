"""
iOS 辅助工具
封装常用的 iOS 设备操作命令
"""
import subprocess
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


class IOSHelper:
    """iOS 工具类"""

    def __init__(self, device_udid: str = None):
        self.device_udid = device_udid
        self.simctl_cmd = "xcrun simctl"
        self.device_cmd = "xcrun devicectl"

    def _run_command(self, cmd: str, timeout: int = 30) -> Optional[str]:
        """运行命令"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f"命令失败：{cmd}, 错误：{result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            logger.error(f"命令超时：{cmd}")
            return None
        except Exception as e:
            logger.error(f"命令异常：{e}")
            return None

    def list_simulators(self) -> List[dict]:
        """列出所有模拟器"""
        output = self._run_command("xcrun simctl list devices --json")
        # 简化处理，实际需要解析 JSON
        return []

    def get_simulator_state(self, udid: str) -> Optional[str]:
        """获取模拟器状态"""
        output = self._run_command(f"xcrun simctl list devices | grep {udid}")
        if output:
            if "Booted" in output:
                return "booted"
            elif "Shutdown" in output:
                return "shutdown"
        return None

    def boot_simulator(self, udid: str) -> bool:
        """启动模拟器"""
        state = self.get_simulator_state(udid)
        if state == "booted":
            logger.info(f"模拟器已在运行：{udid}")
            return True

        result = self._run_command(f"xcrun simctl boot {udid}", timeout=60)
        return result is not None

    def shutdown_simulator(self, udid: str) -> bool:
        """关闭模拟器"""
        result = self._run_command(f"xcrun simctl shutdown {udid}")
        return result is not None

    def erase_simulator(self, udid: str) -> bool:
        """重置模拟器"""
        result = self._run_command(f"xcrun simctl erase {udid}")
        return result is not None

    def install_app(self, udid: str, app_path: str) -> bool:
        """安装 App（模拟器）"""
        result = self._run_command(f"xcrun simctl install {udid} {app_path}")
        return result is not None

    def uninstall_app(self, udid: str, bundle_id: str) -> bool:
        """卸载 App（模拟器）"""
        result = self._run_command(f"xcrun simctl uninstall {udid} {bundle_id}")
        return result is not None

    def launch_app(self, udid: str, bundle_id: str) -> bool:
        """启动 App（模拟器）"""
        result = self._run_command(f"xcrun simctl launch {udid} {bundle_id}")
        return result is not None

    def terminate_app(self, udid: str, bundle_id: str) -> bool:
        """停止 App（模拟器）"""
        result = self._run_command(f"xcrun simctl terminate {udid} {bundle_id}")
        return result is not None

    def get_screenshot(self, udid: str, save_path: str) -> bool:
        """截图（模拟器）"""
        result = self._run_command(f"xcrun simctl io {udid} screenshot {save_path}")
        return result is not None

    def list_real_devices(self) -> List[str]:
        """列出所有真机"""
        output = self._run_command("system_profiler SPUSBDataType | grep -i 'iPhone'")
        # 简化处理
        return []

    def get_real_device_info(self, udid: str) -> dict:
        """获取真机信息"""
        info = {
            "name": self._run_command(f"xcrun devicectl device info -d {udid}"),
        }
        return info


# 便捷函数
def get_simulator_by_name(name: str) -> Optional[str]:
    """根据名称获取模拟器 UDID"""
    helper = IOSHelper()
    output = helper._run_command("xcrun simctl list devices | grep -A 1 '{name}'")
    # 简化处理，实际需解析
    return None
