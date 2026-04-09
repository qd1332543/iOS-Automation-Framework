"""
截图工具 - 失败时自动截图
支持 Appium WebDriver 截图和本地保存
"""
import os
from datetime import datetime

from appium.webdriver.common.appiumby import AppiumBy

from utils.log_util import get_logger

logger = get_logger("ScreenshotUtil")


class ScreenshotUtil:
    """
    截图工具类
    
    功能：
    - 测试失败自动截图
    - 关键步骤截图（用于 Allure 报告）
    - 截图文件管理
    """
    
    def __init__(self, driver=None, screenshot_dir: str = None):
        """
        Args:
            driver: Appium WebDriver 实例
            screenshot_dir: 截图保存目录
        """
        self.driver = driver
        if screenshot_dir is None:
            screenshot_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "UI_Automation", "screenshots"
            )
        self.screenshot_dir = screenshot_dir
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def set_driver(self, driver):
        """设置 WebDriver"""
        self.driver = driver
    
    def capture(self, name: str = None) -> str:
        """
        截取当前屏幕
        
        Args:
            name: 截图文件名前缀
            
        Returns:
            截图文件的绝对路径
        """
        if self.driver is None:
            logger.warning("WebDriver 未设置，无法截图")
            return ""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name or 'screenshot'}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        try:
            self.driver.save_screenshot(filepath)
            logger.info(f"📸 截图已保存: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"❌ 截图失败: {e}")
            return ""
    
    def capture_element(
        self, 
        locator: tuple, 
        name: str = "element"
    ) -> str:
        """
        对指定元素进行截图
        
        Args:
            locator: 元素定位器 (By, value)
            name: 文件名前缀
            
        Returns:
            截图路径
        """
        if self.driver is None:
            return ""
        
        try:
            element = self.driver.find_element(*locator)
            element.screenshot(os.path.join(
                self.screenshot_dir,
                f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            ))
        except Exception as e:
            logger.warning(f"元素截图失败，改用全屏截图: {e}")
            return self.capture(name)
        
        return ""
