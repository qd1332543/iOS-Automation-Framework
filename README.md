# 🧪 iOS-Automation-Framework

> **基于云鹿商城的移动端自动化测试框架** | Appium + pytest + Allure + GitHub Actions + Web UI

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Appium+pytest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 项目简介

本项目是一个完整的 **iOS 移动端自动化测试工程**，以**云鹿商城 App** 为测试对象，实现了 **UI 自动化测试**、**接口自动化测试**、**性能测试** 三位一体的测试解决方案。

它在通用测试平台体系中的定位是：**测试代码载体和第一个接入样板**。本仓库负责“怎么测”，例如 pytest/Appium 用例、Page Object、测试数据、断言和报告输出；通用平台和 Local Agent 负责“谁来调度、在哪里执行、如何回传结果”。

内置的 `tools/webui` 仅作为单项目本地 Demo 控制台，用于浏览代码、执行测试、查看实时日志和 Allure 报告，不承担平台中心或通用 Agent 职责。

### 核心特性

| 特性 | 说明 |
|------|------|
| 🎯 **Page Object 模式** | UI 层与业务逻辑解耦，易于维护 |
| 📊 **数据驱动测试** | YAML 管理测试数据，支持多环境切换 |
| 🔌 **接口/UI 联动** | 统一框架同时支持 API 和 UI 测试 |
| 📈 **Allure 报告** | 可视化测试报告，支持历史趋势 |
| 🔄 **GitHub Actions CI** | 自动化流水线，PR 触发执行 |
| ⚡ **性能测试** | 基于 Locust 的压力测试脚本 |
| 🌐 **本地 Demo 控制台** | 本地 Web UI，支持代码浏览、测试执行、AI 问答 |
| 🔗 **平台接入协议** | 通过 `test-platform.yml` 描述套件、命令、依赖和产物路径 |

---

## 🏗️ 技术架构

```mermaid
graph TD
    A[🧪 pytest 测试执行层]
    A --> B[📱 UI_Automation<br/>Appium + XCUITest]
    A --> C[🔌 API_Automation<br/>Requests + pytest]
    A --> D[⚡ Performance<br/>Locust]

    B & C & D --> E[🛠️ 基础设施层<br/>Config / Logger / Utils]
    E --> F[🚀 CI/CD 层<br/>GitHub Actions / Fastlane]
    E --> G[🌐 本地 Demo 控制台<br/>FastAPI + Alpine.js]
```

---

## 📁 项目结构

```
iOS-Automation-Framework/
├── README.md                      # Project documentation
├── test-platform.yml              # TestPlatform suite contract
├── requirements.txt               # Python dependencies
├── pytest.ini                     # pytest configuration
├── conftest.py                    # Global fixtures
│
├── config/                        # Configuration layer
│   ├── __init__.py
│   ├── settings.py                # Global settings
│   ├── environments.yaml          # Multi-env config
│   └── local.yml.example          # Local config template
│
├── utils/                         # Utility layer
│   ├── __init__.py
│   ├── log_util.py                # Logger (loguru)
│   ├── request_util.py            # HTTP client
│   ├── assertion_util.py          # Assertions
│   └── screenshot_util.py         # Screenshot helper
│
├── UI_Automation/                 # UI tests (Appium + XCUITest)
│   ├── Pages/                     # Page Object Model
│   │   ├── __init__.py
│   │   ├── base_page.py           # Base page class
│   │   ├── login_page.py          # Login page
│   │   ├── home_page.py           # Home page
│   │   ├── category_page.py       # Category page
│   │   ├── search_page.py         # Search page
│   │   ├── product_detail_page.py # Product detail
│   │   ├── cart_page.py           # Cart page
│   │   └── order_page.py          # Order page
│   ├── Tests/                     # UI test cases
│   │   ├── __init__.py
│   │   ├── test_login.py          # Login tests
│   │   ├── test_home.py           # Home tests
│   │   ├── test_search.py         # Search tests
│   │   ├── test_cart.py           # Cart tests
│   │   └── test_order.py          # Order flow tests
│   ├── __init__.py
│   └── conftest.py                # UI fixtures
│
├── API_Automation/                # API tests
│   ├── api/                       # API wrappers
│   │   ├── __init__.py
│   │   ├── base_api.py            # Base API class
│   │   ├── user_api.py            # User API
│   │   ├── product_api.py         # Product API
│   │   ├── cart_api.py            # Cart API
│   │   └── order_api.py           # Order API
│   ├── cases/                     # API test cases
│   │   ├── __init__.py
│   │   ├── test_user.py           # User tests
│   │   ├── test_product.py        # Product tests
│   │   ├── test_cart.py           # Cart tests
│   │   └── test_order.py          # Order tests
│   └── data/                      # Test data (YAML)
│       ├── user_data.yaml
│       ├── product_data.yaml
│       └── order_data.yaml
│
├── Performance/                   # Performance tests
│   └── locust_scripts/
│       └── locustfile.py          # Locust entry point
│
├── CI/                            # CI/CD config
│   ├── jenkins/
│   │   └── Jenkinsfile            # Jenkins pipeline
│   └── fastlane/
│       └── Fastfile               # Fastlane config
│
├── Reports/                       # Test report output (git-ignored)
│   └── webui-runs/                # Web UI 每次运行的独立报告目录
│       └── {run_id}/
│           ├── logs.txt           # pytest 输出（已脱敏）
│           ├── allure-results/    # Allure 原始数据
│           └── allure-report/     # Allure HTML 报告
│
├── tools/                         # 工具目录
│   └── webui/                     # 本地 Demo 控制台
│       ├── app.py                 # FastAPI 主入口
│       ├── config.py              # 配置（读取环境变量）
│       ├── models.py              # Run 任务模型
│       ├── .env.example           # 配置模板
│       ├── services/
│       │   ├── ai_service.py      # AI 问答（mock / Claude）
│       │   ├── allure_service.py  # Allure 报告生成
│       │   ├── env_service.py     # 环境检查
│       │   ├── file_service.py    # 文件树/内容（白名单）
│       │   ├── run_service.py     # 测试执行（subprocess）
│       │   └── sanitize.py        # 日志脱敏
│       └── static/
│           └── index.html         # Alpine.js 单页前端
│
└── docs/                          # Documentation
    ├── design.md                  # Design notes
    └── platform-integration.md    # TestPlatform integration notes
```

| 目录 | 说明 |
|------|------|
| `config/` | 多环境配置，支持 dev / staging / prod |
| `utils/` | 日志、HTTP、断言、截图等公共工具 |
| `UI_Automation/` | Appium UI 自动化，Page Object 模式 |
| `API_Automation/` | 接口自动化，数据与用例分离 |
| `Performance/` | Locust 性能压测脚本 |
| `CI/` | GitHub Actions / Fastlane 配置 |
| `Reports/` | Allure 报告输出目录，webui-runs/ 存放 Web UI 运行记录 |
| `test-platform.yml` | 平台接入协议：声明项目、套件、命令、依赖和产物路径 |
| `tools/webui/` | 本地 Demo 控制台：代码浏览、测试执行、AI 问答 |
| `docs/platform-integration.md` | 与 TestPlatform / Local Agent 的职责边界和接入说明 |

---

## 🚀 快速开始

### 环境要求

- **Python**: 3.9+
- **Node.js**: 18+ (Appium 2.x 需要)
- **Appium**: 2.x (`npm install -g appium && appium driver install xcuitest`)
- **Xcode**: 14+ (iOS 模拟器)

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/your-username/iOS-Automation-Framework.git
cd iOS-Automation-Framework

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 安装 Appium
npm install -g appium
appium driver install xcuitest

# 5. 配置本地环境
cp config/local.yml.example config/local.yml
# 编辑 local.yml，填入你的设备名、App 路径和测试账号
```

### 运行测试

```bash
# ====== 接口自动化测试（并发执行）======
pytest API_Automation/cases -v --alluredir=./Reports/api-results

# 运行指定模块
pytest API_Automation/cases/test_user.py -v

# 生成 Allure 报告
allure generate ./Reports/api-results -o ./Reports/api-report --clean
allure open ./Reports/api-report

# ====== UI 自动化测试（串行，需要真机/模拟器）======
# 1. 启动 Appium Server（新终端）
appium

# 2. 运行 UI 测试（-n 0 覆盖 pytest.ini 的并发设置）
pytest UI_Automation/Tests -v -n 0 --alluredir=./Reports/ui-results

# ====== 性能测试 ======
cd Performance/locust_scripts
locust -f locustfile.py --host=https://api-dev.yunlu.com
```

### 平台接入执行

通用平台或 Local Agent 应读取仓库根目录的 `test-platform.yml`，根据任务选择 suite 并执行其中的命令。

示例：

```bash
# 平台任务 task_id=local-demo-001 时，API 全量套件可写入固定产物目录
python -m pytest API_Automation/cases -v --alluredir=Reports/platform/local-demo-001/allure-results

# UI 套件由 Local Agent 负责准备 Appium、设备和 ipa/app 包路径
python -m pytest UI_Automation/Tests -v -n 0 --alluredir=Reports/platform/local-demo-001/allure-results
```

平台触发的运行建议统一输出到：

```text
Reports/platform/{task_id}/
├── logs.txt
├── allure-results/
├── allure-report/
└── screenshots/
```

被测 `.ipa` / `.app` 包应作为平台任务参数传入，例如 `app_path` 或 `app_url`。本仓库不负责构建 App，也不负责通用任务调度。

---

## 🌐 本地 Demo 控制台

内置本地 Web UI，无需命令行即可浏览代码、执行测试、查看实时日志和 Allure 报告。它只用于本仓库本地调试和演示，不是通用测试平台。

### 启动

```bash
python -m uvicorn tools.webui.app:app --host 127.0.0.1 --port 8000
# 访问 http://127.0.0.1:8000
```

### 配置

复制配置模板并按需修改：

```bash
cp tools/webui/.env.example tools/webui/.env
```

关键配置项：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `AI_PROVIDER` | `mock` | `mock` 或 `claude`（需配合 `AI_API_KEY`） |
| `AI_MODEL` | `claude-sonnet-4-6` | AI 模型 ID，可替换为其他模型 |
| `AI_API_KEY` | 空 | Claude API Key，mock 模式下不需要 |
| `ALLURE_BIN` | `allure` | allure 命令路径 |
| `MAX_CONCURRENT_RUNS` | `1` | 最大并发任务数 |

### 功能说明

| 功能 | 说明 |
|------|------|
| 文件树浏览 | 只展示白名单文件，敏感文件不可访问 |
| 代码查看 | 只读，单文件最大 200KB |
| AI 问答 | 基于项目文件检索回答，mock 模式无需 API Key |
| 测试执行 | 固定模块白名单，不支持任意命令输入 |
| 实时日志 | SSE 推送，日志自动脱敏（token、密码等） |
| Allure 报告 | 每次运行独立目录，需安装 allure 命令 |
| 环境检查 | 自动检测 Python/pytest/Allure/Appium/Xcode 状态 |

### 运行记录

每次执行测试会在 `Reports/webui-runs/{run_id}/` 生成：

```
{run_id}/
├── logs.txt           # pytest 完整输出（已脱敏）
├── allure-results/    # Allure 原始数据
└── allure-report/     # Allure HTML 报告（需 allure 命令）
```

### 注意事项

- iOS UI 测试需要 **macOS + Xcode + Appium**，Windows/Linux 下 UI 模块自动禁用
- Web UI 仅供本地单用户 Demo 使用，不适合生产部署
- 通用 Local Agent 应放在 TestPlatform 侧，本仓库只暴露测试套件和执行命令
- 接入真实 AI 需设置 `AI_PROVIDER=claude` 和 `AI_API_KEY`

### 为什么选择 Page Object 模式？

**问题**：传统线性脚本的维护成本极高，UI 变更需要修改大量测试代码。

**方案**：Page Object 模式将每个页面抽象为一个对象：
- **元素定位**集中在 Page 类中
- **业务操作**封装为 Page 方法
- **测试用例**只关注业务流程，不关心元素细节

**优势**：UI 变更只需修改对应的 Page 类，不影响测试用例。

### 为什么选择 Appium + pytest？

| 维度 | 选择 | 理由 |
|------|------|------|
| UI 框架 | Appium | 跨平台、生态成熟、社区活跃 |
| 测试框架 | pytest | fixture 强大、参数化便捷、插件丰富 |
| 报告系统 | Allure | 可视化好、支持历史对比、便于分享 |
| 数据驱动 | YAML + parametrize | 数据与代码分离，非技术人员可维护 |

### 如何保证测试稳定性？

1. **显式等待**：替代 `sleep()` 和隐式等待，使用 `WebDriverWait` 精确控制
2. **多策略元素定位**：优先 Accessibility ID → XPath → Predicate → Class Chain
3. **重试机制**：`pytest-rerunfailures` 失败自动重试
4. **失败截图**：每次失败自动截图 + 日志记录
5. **数据隔离**：每条用例独立数据，避免状态污染

---

## 📊 测试覆盖范围

### UI 自动化（云鹿商城）

| 模块 | 功能点 | 用例数 |
|------|--------|--------|
| 登录模块 | 手机号登录、验证码、密码登录 | 15 |
| 首页 | Banner 轮播、分类导航、推荐商品 | 12 |
| 分类 | 分类列表、筛选排序、商品卡片 | 10 |
| 商品详情 | 图片预览、规格选择、加入购物车 | 18 |
| 购物车 | 数量修改、删除、结算 | 14 |
| 订单 | 提交订单、支付、订单列表 | 20 |
| **合计** | | **89** |

### 接口自动化

| 模块 | 接口数 | 用例数 |
|------|--------|--------|
| 用户模块 | 8 | 32 |
| 商品模块 | 12 | 48 |
| 购物车模块 | 6 | 24 |
| 订单模块 | 10 | 40 |
| **合计** | **36** | **144** |

---

## 🔧 核心代码示例

### Page Object 示例

```python
# UI_Automation/Pages/login_page.py
class LoginPage(BasePage):
    """云鹿商城 - 登录页"""
    
    # 元素定位
    _PHONE_INPUT = (MobileBy.ACCESSIBILITY_ID, "phone_input")
    _CODE_INPUT = (MobileBy.ACCESSIBILITY_ID, "code_input")
    _LOGIN_BTN = (MobileBy.ACCESSIBILITY_ID, "login_button")
    _AGREE_CHECKBOX = (MobileBy.XPATH, "//XCUIElementTypeSwitch")
    
    def input_phone(self, phone: str):
        """输入手机号"""
        self.wait_and_input(self._PHONE_INPUT, phone)
        return self
    
    def input_code(self, code: str):
        """输入验证码"""
        self.wait_and_input(self._CODE_INPUT, code)
        return self
    
    def click_login(self):
        """点击登录按钮"""
        self.wait_and_click(self._LOGIN_BTN)
        return HomePage(self.driver)
    
    def login(self, phone, code):
        """完整登录流程"""
        return (self.input_phone(phone)
                   .input_code(code)
                   .click_login())
```

### 数据驱动测试示例

```yaml
# API_Automation/data/user_data.yaml
login_cases:
  - name: 正常手机号登录
    phone: "13800138000"
    code: "123456"
    expected_code: 0
    expected_msg: "success"
    
  - name: 错误的手机号格式
    phone: "123"
    code: "123456"
    expected_code: 1001
    expected_msg: "手机号格式错误"
    
  - name: 错误验证码
    phone: "13800138000"
    code: "000000"
    expected_code: 1002
    expected_msg: "验证码错误"
```

---


## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

---

## 📄 License

MIT License © 2024

---

## 👨‍💻 作者

iOS 开发工程师，关注工程质量与交付效率。本项目源于对移动端自动化测试体系的系统性思考——从 Page Object 设计、接口分层到 CI/CD 落地，记录完整的工程实践过程。
