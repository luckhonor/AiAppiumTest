"""
测试运行脚本
用于执行测试并生成 Allure 报告
"""
import os
import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path


def run_tests(platform: str = "android",
              markers: str = None,
              test_file: str = None,
              generate_report: bool = True,
              serve_report: bool = False):
    """
    运行测试并生成报告

    Args:
        platform: 测试平台 (android/ios)
        markers: pytest 标记过滤 (smoke/regression)
        test_file: 指定测试文件
        generate_report: 是否生成报告
        serve_report: 是否直接打开报告
    """
    # 项目根目录
    project_root = Path(__file__).parent
    reports_dir = project_root / "reports" / "allure-results"
    html_reports_dir = project_root / "reports" / "html"

    # 创建报告目录
    reports_dir.mkdir(parents=True, exist_ok=True)
    html_reports_dir.mkdir(parents=True, exist_ok=True)

    # 构建 pytest 命令
    cmd = [
        sys.executable, "-m", "pytest",
        "-v",
        "--tb=short",
        f"--platform={platform}",
        f"--alluredir={reports_dir}",
    ]

    # 添加标记过滤
    if markers:
        cmd.append(f"-m {markers}")

    # 指定测试文件
    if test_file:
        cmd.append(str(project_root / "tests" / "test_suite" / test_file))
    else:
        cmd.append(str(project_root / "tests"))

    # 添加重试
    cmd.extend(["--reruns", "1", "--reruns-delay", "2"])

    print(f"执行命令: {' '.join(cmd)}")
    print("=" * 60)

    # 运行测试
    result = subprocess.run(cmd, cwd=project_root)

    # 生成报告
    if generate_report and result.returncode != 1:  # 不是全部失败
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if serve_report:
            # 直接打开 Allure 报告服务
            serve_cmd = ["allure", "serve", str(reports_dir)]
            print(f"\n启动 Allure 报告服务...")
            subprocess.run(serve_cmd)
        else:
            # 生成静态 HTML 报告
            report_output = project_root / "reports" / f"allure-report-{timestamp}"
            generate_cmd = ["allure", "generate", str(reports_dir),
                           "-o", str(report_output), "--clean"]
            print(f"\n生成报告到: {report_output}")
            subprocess.run(generate_cmd)

            # 同时生成 pytest-html 报告
            html_report = html_reports_dir / f"report-{timestamp}.html"
            print(f"HTML 报告: {html_report}")

    return result.returncode


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="App 自动化测试运行脚本")

    parser.add_argument(
        "--platform", "-p",
        default="android",
        choices=["android", "ios"],
        help="测试平台"
    )

    parser.add_argument(
        "--markers", "-m",
        default=None,
        help="pytest 标记过滤 (smoke/regression)"
    )

    parser.add_argument(
        "--file", "-f",
        default=None,
        help="指定测试文件"
    )

    parser.add_argument(
        "--serve", "-s",
        action="store_true",
        help="直接打开 Allure 报告服务"
    )

    parser.add_argument(
        "--no-report",
        action="store_true",
        help="不生成报告"
    )

    args = parser.parse_args()

    # 运行测试
    exit_code = run_tests(
        platform=args.platform,
        markers=args.markers,
        test_file=args.file,
        generate_report=not args.no_report,
        serve_report=args.serve
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    # 直接运行时的默认配置
    print("=" * 60)
    print("App 自动化测试 - 手机号登录测试")
    print("=" * 60)

    run_tests(
        platform="android",
        test_file="test_phone_login.py",
        generate_report=True,
        serve_report=True  # 直接打开报告
    )