"""
设计思路文档

## 一、项目背景与目标

### 1.1 为什么选择云鹿商城作为测试对象？

参考项目资料中的 **山海悦兮** 项目包含 `yunlucang-ios` 和 `yunlujiapp-ios` 两个 iOS 应用，均为电商类 App（"云鹿仓"、"云鹿集"）。电商 App 是自动化测试的最佳实践场景：

- 功能模块完整（登录、分类、搜索、购物车、订单）
- 业务流程清晰（浏览→加购→结算→支付→售后）
- UI 元素丰富（列表、表单、弹窗、Tab导航）
- 接口规范标准（RESTful API）

### 1.2 项目目标

本框架的目标是：
1. **展示技术能力**：证明具备独立设计、搭建企业级测试框架的能力
2. **覆盖面试考点**：Page Object、数据驱动、CI/CD、Allure 报告等全部落地
3. **可直接复用**：代码结构清晰，可快速适配其他项目
4. **完整的工程实践**：包含从设计到部署的完整链路

---

## 二、架构设计决策

### 2.1 为什么选择 Page Object 模式？

| 问题 | 传统线性脚本 | Page Object |
|------|---------------|-------------|
| 元素变更 | 需修改所有使用处 | 只改对应 Page 类 |
| 维护成本 | 高 | 低 |
| 可读性 | 差 | 好 |
| 复用性 | 无 | 强 |

### 2.2 技术栈选择理由

| 组件 | 选择 | 替代方案 | 选择理由 |
|------|------|----------|----------|
| UI 自动化框架 | Appium | XCUITest / WebDriverAgent | 跨平台、社区活跃、Python 生态好 |
| 测试框架 | pytest | unittest / nose2 | fixture强大、插件丰富、Allure集成好 |
| 报告系统 | Allure | pytest-html / HTMLTestRunner | 可视化优秀、支持历史对比 |
| 数据管理 | YAML + parametrize | Excel / JSON | 与代码分离、易维护 |
| HTTP 客户端 | requests | httpx | 成熟稳定 |

### 2.3 目录结构分层逻辑

```
config/     → 配置层（环境隔离、多环境切换）
utils/      → 基础设施层（日志、HTTP封装、断言、截图）
API_Auto/   → 接口自动化层（API 封装 → 用例 → 数据）
UI_Auto/    → UI 自动化层（Page Object → 测试用例）
Performance/→ 性能测试层（Locust 场景脚本）
CI/         → 持续集成层（Jenkins/Fastlane 配置）
```

每层职责清晰，依赖方向单向（上层依赖下层）。

---

## 三、关键设计模式

### 3.1 元素定位策略（多重备选）

iOS 自动化最大的痛点是元素定位不稳定。解决方案：

```python
# 主定位方式：Accessibility ID（最稳定）
_PHONE_INPUT = (AppiumBy.ACCESSIBILITY_ID, "phone_input")

# 备选方式：XPath（兜底）
_PHONE_INPUT_XPATH = (AppiumBy.XPATH, "//...")

# 使用时自动尝试主方案，失败则降级到备选
```

### 3.2 数据驱动测试

YAML 文件管理测试数据，实现数据与代码分离：

- **优势**：非技术人员也能维护测试数据
- **参数化**：通过 @pytest.mark.parametrize 批量生成用例
- **多环境**：同一套数据可用于 dev/staging/prod

### 3.3 稳定性保障机制

1. **显式等待**：替代 sleep()，基于条件等待
2. **重试机制**：pytest-rerunfailures 失败自动重试 2 次
3. **失败截图**：每次失败自动截图 + 日志附加
4. **Session 隔离**：每个测试函数独立的 Driver session
5. **连接池**：requests.Session 复用 TCP 连接

---

## 四、扩展性设计

### 4.1 如何添加新页面？

1. 在 `UI_Automation/Pages/` 创建新文件 `xxx_page.py`
2. 继承 `BasePage`
3. 定义元素定位器和业务方法
4. 在 `__init__.py` 中导出
5. 编写对应测试用例

### 4.2 如何添加新的 API 模块？

1. 在 `API_Automation/api/` 创建 `xxx_api.py`
2. 继承 `BaseAPI`
3. 封装该模块的所有接口方法
4. 在 `cases/` 中编写测试用例

### 4.3 如何接入新的 CI 系统？

只需修改 `CI/jenkins/Jenkinsfile` 或创建新的 pipeline 配置。

---

## 五、性能指标预期

| 指标 | 目标值 | 说明 |
|------|--------|------|
| API 用例执行时间 | < 60s | 全量接口测试 |
| UI 单个用例时间 | < 30s | 含等待时间 |
| 并发用户数 | 100+ | Locust 压力测试 |
| 测试通过率 | > 95% | 核心功能稳定 |
| 失败重试成功率 | > 80% | 偶发问题自动恢复 |
