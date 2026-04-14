"""
日志封装
基于 loguru 的统一日志管理
"""
import sys
import logging
from pathlib import Path
from loguru import logger


def setup_logger(
    log_dir: str = "logs",
    level: str = "INFO",
    rotation: str = "100 MB",
    retention: str = "7 days",
    format: str = None
) -> None:
    """
    配置日志系统

    Args:
        log_dir: 日志目录
        level: 日志级别
        rotation: 轮转大小
        retention: 保留时间
        format: 日志格式
    """
    # 创建日志目录
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # 移除默认 handler
    logger.remove()

    # 默认格式
    if format is None:
        format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{module}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

    # 控制台输出
    logger.add(
        sys.stderr,
        level=level,
        format=format,
        colorize=True,
    )

    # 文件输出 - 所有日志
    logger.add(
        log_path / "app.log",
        level=level,
        format=format,
        rotation=rotation,
        retention=retention,
        encoding="utf-8",
    )

    # 文件输出 - 仅错误日志
    logger.add(
        log_path / "error.log",
        level="ERROR",
        format=format,
        rotation=rotation,
        retention=retention,
        encoding="utf-8",
    )

    # 捕获异常
    logger.add(
        log_path / "exception.log",
        level="ERROR",
        format=format + "\n{exception}",
        rotation=rotation,
        retention=retention,
        enqueue=True,
    )


def get_logger(name: str = __name__):
    """
    获取日志记录器

    Args:
        name: 模块名称

    Returns:
        配置好的 logger 实例
    """
    return logger


# 初始化日志
setup_logger()
