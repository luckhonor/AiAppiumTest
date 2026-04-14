# App 页面控件定义

## 登录页面 (LoginPage)

### 页面路径
`in.dradhanus.liveher.SplashActivity` -> 登录页面

### 控件定义

| 控件名称 | 定位方式 | 定位值 | 描述 |
|---------|---------|--------|------|
| 手机号输入框 | ID | `et_phone` | 输入手机号码 |
| 密码输入框 | ID | `et_password` | 输入登录密码 |
| 登录按钮 | ID | `btn_login` | 点击登录 |
| 错误提示 | ID | `tv_error_msg` | 显示错误信息 |
| 忘记密码 | ID | `tv_forgot_password` | 忘记密码入口 |
| 用户协议勾选 | ID | `cb_agreement` | 同意用户协议 |
| 注册入口 | ID | `tv_register` | 注册链接 |

### Android定位器代码
```python
# 手机号输入框
(AppiumBy.ID, "in.dradhanus.liveher:id/et_phone")

# 密码输入框
(AppiumBy.ID, "in.dradhanus.liveher:id/et_password")

# 登录按钮
(AppiumBy.ID, "in.dradhanus.liveher:id/btn_login")

# 错误提示
(AppiumBy.ID, "in.dradhanus.liveher:id/tv_error_msg")

# 忘记密码
(AppiumBy.ID, "in.dradhanus.liveher:id/tv_forgot_password")

# 用户协议勾选
(AppiumBy.ID, "in.dradhanus.liveher:id/cb_agreement")

# 注册入口
(AppiumBy.ID, "in.dradhanus.liveher:id/tv_register")
```

---

## 首页 (HomePage)

### 控件定义

| 控件名称 | 定位方式 | 定位值 | 描述 |
|---------|---------|--------|------|
| 欢迎文本 | ID | `tv_welcome` | 显示欢迎信息 |
| 用户头像 | ID | `iv_avatar` | 用户头像 |
| 个人中心入口 | ID | `iv_profile` | 进入个人中心 |

---

## 测试账号信息

| 账号类型 | 手机号范围 | 密码 | 用途 |
|---------|----------|------|------|
| 正常账号 | 1000000001 - 1000000999 | test11 | 正常登录测试 |
| 边界账号 | 1000000000, 1000001000 | test11 | 边界值测试 |
| 无效账号 | 非上述范围 | test11 | 登录失败测试 |

---

## 测试场景覆盖

### 正向测试
- 正常手机号登录成功
- 账号区间边界登录测试

### 异向测试
- 手机号为空
- 密码为空
- 手机号格式错误（非数字）
- 手机号位数错误（少于10位/多于10位）
- 密码错误
- 手机号不存在
- 未勾选用户协议

### 边界测试
- 最小手机号 1000000001
- 最大手机号 1000000999
- 边界外手机号 1000000000, 1000001000