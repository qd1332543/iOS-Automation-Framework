"""
全局 conftest.py - 共享 fixtures 和钩子函数
"""
import os
import sys
import pytest
import allure
import yaml
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ==================== 配置加载 ====================

@pytest.fixture(scope="session")
def env_config():
    """
    加载环境配置
    从 environments.yaml 读取当前环境配置
    """
    config_path = os.path.join(os.path.dirname(__file__), "config", "environments.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # 通过环境变量切换环境，默认 dev
    env = os.getenv("TEST_ENV", "dev")
    return config.get(env, config.get("dev"))


# ==================== API 测试 Fixtures ====================

@pytest.fixture(scope="session")
def api_base_url(env_config):
    """API 基础 URL"""
    return env_config["api"]["base_url"]


@pytest.fixture(scope="session")
def request_util(api_base_url):
    """HTTP 请求工具实例"""
    from utils.request_util import RequestUtil
    return RequestUtil(base_url=api_base_url)


@pytest.fixture(scope="function")
def login_token(request_util, env_config):
    """
    获取登录 Token
    每个测试函数使用独立的 Token，保证数据隔离
    """
    login_data = env_config["test_account"]
    response = request_util.post(
        "/user/login",
        json={
            "phone": login_data["phone"],
            "code": login_data["code"]
        }
    )
    result = response.json()
    assert result["code"] == 0, f"登录失败: {result.get('msg')}"
    return result["data"]["token"]


@pytest.fixture(scope="function")
def auth_headers(login_token):
    """带认证的请求头"""
    return {
        "Authorization": f"Bearer {login_token}",
        "Content-Type": "application/json"
    }


# ==================== 数据驱动 Fixture ====================

@pytest.fixture(scope="session")
def user_test_data():
    """加载用户模块测试数据"""
    data_path = os.path.join(
        os.path.dirname(__file__), 
        "API_Automation", "data", "user_data.yaml"
    )
    with open(data_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def product_test_data():
    """加载商品模块测试数据"""
    data_path = os.path.join(
        os.path.dirname(__file__), 
        "API_Automation", "data", "product_data.yaml"
    )
    with open(data_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ==================== Pytest 钩子函数 ====================

def pytest_configure(config):
    """pytest 初始化配置"""
    # 注册自定义标记
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "regression: 回归测试")
    config.addinivalue_line("markers", "api: 接口测试")
    config.addinivalue_line("markers", "ui: UI测试")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    钩子：在测试报告中添加额外信息
    包括：用例执行时间、测试数据快照等
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.passed:
        # 记录通过信息
        pass


def pytest_runtest_logreport(report):
    """
    钩子：记录测试日志
    失败时自动附加截图和日志
    """
    if report.failed and hasattr(report, "longreprtext"):
        with allure.step("错误详情"):
            allure.attach(
                report.longreprtext or "无详细信息",
                name="错误堆栈",
                attachment_type=allure.attachment_type.TEXT
            )


# ==================== Allure 环境信息 ====================

@pytest.fixture(autouse=True, scope="session")
def allure_environment(env_config):
    """配置 Allure 报告的环境信息"""
    env_properties = {
        "Python版本": sys.version.split()[0],
        "测试环境": env_config.get("name", "dev"),
        "API地址": env_config.get("api", {}).get("base_url", ""),
        "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "测试框架": "pytest + Appium + Allure",
    }
    
    env_dir = os.path.join(os.path.dirname(__file__), "Reports", "allure-results")
    os.makedirs(env_dir, exist_ok=True)
    
    env_file = os.path.join(env_dir, "environment.properties")
    with open(env_file, "w", encoding="utf-8") as f:
        for key, value in env_properties.items():
            f.write(f"{key}={value}\n")
