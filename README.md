# App 自动化测试框架

基于 Appium + pytest 的 PageObject 模式自动化测试框架，支持 iOS/Android 双端测试。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动 Appium Server

```bash
appium --address 127.0.0.1 --port 4723
```

### 3. 运行测试

```bash
# Android 平台
pytest --platform=android --app=/path/to/app.apk

# iOS 平台
pytest --platform=ios --app=/path/to/app.app

# 冒烟测试
pytest -m smoke

# 生成报告
pytest --alluredir=./reports/allure-results
allure serve ./reports/allure-results
```

## 项目结构

```
appautotest/
├── config/                    # 配置目录
│   ├── capabilities/          # 设备配置
│   ├── settings.yaml          # 全局配置
│   └── devices.yaml           # 设备列表
├── pages/                     # 页面对象层
│   ├── base_page.py           # BasePage 基类
│   └── modules/               # 业务页面
├── tests/                     # 测试用例层
│   ├── conftest.py            # pytest fixture
│   └── test_suite/            # 测试集
├── common/                    # 通用封装
│   ├── gestures.py            # 手势操作
│   ├── waits.py               # 等待策略
│   ├── assertions.py          # 断言封装
│   └── text_locator.py        # 文案定位
├── utils/                     # 工具类
│   ├── driver_factory.py      # Driver 工厂
│   ├── logger.py              # 日志封装
│   ├── adb_helper.py          # ADB 辅助
│   └── ios_helper.py          # iOS 辅助
├── reports/                   # 测试报告
├── logs/                      # 日志目录
├── pytest.ini                 # pytest 配置
└── requirements.txt           # 依赖清单
```

## 编写测试用例

```python
import pytest
from pages.modules.login_page import LoginPage


class TestLogin:

    @pytest.mark.smoke
    def test_login_success(self, driver):
        """测试正常登录"""
        login_page = LoginPage(driver)

        # 执行登录
        home_page = login_page.login("testuser", "password123")

        # 验证登录成功
        assert home_page is not None
        assert home_page.is_welcome_displayed()
```

## 页面对象模板

```python
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy


class MyPage(BasePage):

    @property
    def my_element(self):
        return (AppiumBy.ACCESSIBILITY_ID, "element_id")

    def click_my_element(self):
        self._click(self.my_element)
        return self

    @classmethod
    def verify_page(cls, driver, timeout=5):
        instance = cls(driver)
        instance._find_element(instance.my_element, timeout)
        return instance
```

## 常用命令

```bash
# 运行指定测试文件
pytest tests/test_suite/test_login.py -v

# 运行指定标记的测试
pytest -m smoke -v

# 并行执行
pytest -n 2

# 失败重跑
pytest --reruns 2 --reruns-delay 1

# 生成 HTML 报告
pytest --html=reports/test_report.html

# 生成 Allure 报告
allure serve ./reports/allure-results
```

## 元素定位优先级

1. `accessibility_id` (首选，跨平台)
2. `id` (resource-id / accessibilityLabel)
3. 文案定位 (TextLocator)
4. `class name` + index
5. `xpath` (最后手段)

## 配置说明

### 命令行参数

| 参数 | 说明 | 默认值 |
|-----|------|--------|
| --platform | 测试平台 | android |
| --device | 设备 UDID | auto |
| --app | App 路径 | None |
| --env | 环境 | dev |

### settings.yaml

```yaml
appium:
  host: 127.0.0.1
  port: 4723
  timeout: 30

test:
  default_timeout: 10
  screenshot_on_fail: true
```

## 框架特性

- ✅ PageObject 设计模式
- ✅ pytest 测试框架
- ✅ Allure 可视化报告
- ✅ 失败自动截图
- ✅ 智能等待策略
- ✅ 统一手势封装
- ✅ 文案定位策略
- ✅ 日志分级管理
- ✅ 数据驱动测试
- ✅ 并行执行支持

## 故障排查

### 元素找不到

1. 检查页面是否完全加载
2. 使用 Appium Inspector 重新定位
3. 尝试其他定位策略
4. 检查是否在正确的 context

### 测试不稳定

1. 增加显式等待条件
2. 添加重试机制
3. 检查设备性能

## License

MIT
