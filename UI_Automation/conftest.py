"""
UI 自动化测试 - conftest.py
提供 Appium WebDriver fixture 和 UI 测试专用钩子
"""
import os
import sys
from typing import Dict

import pytest
from appium import webdriver
from appium.options.ios.options import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy

# 添加项目根路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.log_util import get_logger

logger = get_logger("UI_Conftest")


def create_driver(appium_url: str = "http://127.0.0.1:4723", 
                   app_path: str = None,
                   device_name: str = "iPhone 15 Pro",
                   platform_version: str = "17.2",
                   no_reset: bool = True):
    """
    创建 Appium WebDriver 实例
    
    Args:
        appium_url: Appium Server 地址
        app_path: .app 文件路径
        device_name: 设备名称
        platform_version: iOS 版本
        no_reset: 是否在每次会话前重置 App 状态
        
    Returns:
        WebDriver 实例
    """
    options = XCUITestOptions()
    
    # 基础配置
    options.platform_name = "iOS"
    options.platform_version = platform_version
    options.device_name = device_name
    options.no_reset = no_reset
    
    # App 配置
    if app_path:
        options.app = app_path
    
    # 性能优化配置
    options.new_command_timeout = 60  # 命令超时
    options.launch_timeout = 120      # 启动超时
    
    # 自动化相关
    options.auto_accept_alerts = True   # 自动接受弹窗
    auto_dismiss_alerts = True         # 自动关闭系统警告
    
    logger.info(f"📱 创建 WebDriver: {device_name} (iOS {platform_version})")
    driver = webdriver.Remote(
        command_executor=appium_url,
        options=options
    )
    
    driver.implicitly_wait(10)  # 默认隐式等待
    return driver


@pytest.fixture(scope="function")
def ios_driver():
    """
    每个 UI 测试函数的 Driver fixture
    - 测试前启动/复用 App
    - 测试后自动关闭 session（如果失败则截图）
    """
    driver = None
    try:
        # 从环境变量或默认值获取配置
        appium_url = os.getenv("APPIUM_URL", "http://127.0.0.1:4723")
        app_path = os.getenv("APP_PATH")
        
        driver = create_driver(
            appium_url=appium_url,
            app_path=app_path,
            device_name=os.getenv("DEVICE_NAME", "iPhone 15 Pro"),
            platform_version=os.getenv("PLATFORM_VERSION", "17.2"),
            no_reset=True  # 保持登录状态等
        )
        
        yield driver
        
    except Exception as e:
        logger.error(f"❌ WebDriver 初始化失败: {e}")
        raise
    finally:
        if driver:
            try:
                # 失败时截图保存
                if hasattr(driver, 'session') and driver.session:
                    screenshot_dir = os.path.join(
                        os.path.dirname(__file__), 
                        "screenshots"
                    )
                    os.makedirs(screenshot_dir, exist_ok=True)
                    timestamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
                    driver.save_screenshot(
                        os.path.join(screenshot_dir, f"teardown_{timestamp}.png")
                    )
                driver.quit()
                logger.info("📱 WebDriver 已关闭")
            except Exception:
                pass


@pytest.fixture(scope="function")
def login_page(ios_driver):
    """获取登录页面对象"""
    from UI_Automation.Pages.login_page import LoginPage
    return LoginPage(ios_driver)


@pytest.fixture(scope="function")
def home_page(ios_driver):
    """
    获取首页对象（已登录状态）
    如果当前不在首页，先完成登录流程
    """
    from UI_Automation.Pages.home_page import HomePage
    from UI_Automation.Pages.login_page import LoginPage
    
    page = HomePage(ios_driver)
    
    # 如果不在首页，尝试登录
    if not page.is_on_home_page():
        logger.info("🔐 当前不在首页，执行登录流程...")
        login = LoginPage(ios_driver)
        test_phone = os.getenv("TEST_PHONE", "13800138000")
        test_code = os.getenv("TEST_CODE", "123456")
        page = login.login_with_code(test_phone, test_code)
    
    return page


# ==================== 跳过标记 ====================

def skip_without_appium():
    """Appium Server 未运行时跳过 UI 测试"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("127.0.0.1", 4723))
    sock.close()
    return result != 0


pytestmark = pytest.mark.skipif(
    skip_without_appium(), 
    reason="Appium Server 未启动，跳过 UI 测试"
)
