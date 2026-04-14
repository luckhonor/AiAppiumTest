"""
ADB 辅助工具
封装常用的 ADB 命令
"""
import subprocess
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


class ADBHelper:
    """ADB 工具类"""

    def __init__(self, device_id: str = None):
        self.device_id = device_id
        self.adb_cmd = "adb"

    def _run_command(self, args: List[str], timeout: int = 30) -> Optional[str]:
        """运行 ADB 命令"""
        try:
            cmd = [self.adb_cmd]
            if self.device_id:
                cmd.extend(["-s", self.device_id])
            cmd.extend(args)

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f"ADB 命令失败：{' '.join(cmd)}, 错误：{result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            logger.error(f"ADB 命令超时：{' '.join(args)}")
            return None
        except Exception as e:
            logger.error(f"ADB 命令异常：{e}")
            return None

    def get_devices(self) -> List[str]:
        """获取所有连接的设备"""
        output = self._run_command(["devices"])
        if output:
            lines = output.split("\n")[1:]  # 跳过表头
            return [line.split()[0] for line in lines if line.strip()]
        return []

    def get_device_state(self) -> Optional[str]:
        """获取设备状态"""
        output = self._run_command(["get-state"])
        return output

    def is_device_online(self) -> bool:
        """检查设备是否在线"""
        return self.get_device_state() == "device"

    def get_current_activity(self) -> Optional[str]:
        """获取当前 Activity"""
        output = self._run_command(["dumpsys", "window", "windows"])
        if output:
            for line in output.split("\n"):
                if "mCurrentFocus" in line or "mFocusedApp" in line:
                    # 提取 activity 名称
                    try:
                        return line.split("/")[-1].split("}")[0].strip()
                    except:
                        continue
        return None

    def get_current_package(self) -> Optional[str]:
        """获取当前 Package"""
        output = self._run_command(["dumpsys", "window", "windows"])
        if output:
            for line in output.split("\n"):
                if "mCurrentFocus" in line or "mFocusedApp" in line:
                    try:
                        return line.split("/")[0].split(" ")[-1].strip()
                    except:
                        continue
        return None

    def install_app(self, apk_path: str) -> bool:
        """安装 App"""
        result = self._run_command(["install", "-r", apk_path], timeout=300)
        return result is not None and "Success" in result

    def uninstall_app(self, package_name: str) -> bool:
        """卸载 App"""
        result = self._run_command(["uninstall", package_name])
        return result is not None and "Success" in result

    def clear_app_data(self, package_name: str) -> bool:
        """清除 App 数据"""
        result = self._run_command(["shell", "pm", "clear", package_name])
        return result is not None and "Success" in result

    def start_app(self, package_name: str, activity_name: str = None) -> bool:
        """启动 App"""
        if activity_name:
            component = f"{package_name}/{activity_name}"
        else:
            component = package_name

        result = self._run_command(["shell", "am", "start", "-n", component])
        return result is not None

    def stop_app(self, package_name: str) -> bool:
        """停止 App"""
        result = self._run_command(["shell", "am", "force-stop", package_name])
        return result is not None

    def take_screenshot(self, save_path: str) -> bool:
        """截图"""
        # 先截图到设备，再 pull 到本地
        remote_path = "/sdcard/screenshot.png"
        self._run_command(["shell", "screencap", "-p", remote_path])
        result = self._run_command(["pull", remote_path, save_path])
        return result is not None

    def get_device_info(self) -> dict:
        """获取设备信息"""
        info = {
            "model": self._run_command(["shell", "getprop", "ro.product.model"]),
            "brand": self._run_command(["shell", "getprop", "ro.product.brand"]),
            "version": self._run_command(["shell", "getprop", "ro.build.version.release"]),
            "sdk": self._run_command(["shell", "getprop", "ro.build.version.sdk"]),
        }
        return info


# 便捷函数
def get_connected_devices() -> List[str]:
    """获取已连接的设备列表"""
    helper = ADBHelper()
    return helper.get_devices()
