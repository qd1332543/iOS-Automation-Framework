"""
BasePage - 页面基类（Page Object 模式的核心）

封装了所有通用的页面操作：
- 元素定位与等待
- 点击、输入、滑动
- 截图与日志
- 显式等待策略
"""
import os
import time
from typing import List, Optional, Tuple, Union

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.log_util import get_logger
from utils.screenshot_util import ScreenshotUtil


class BasePage:
    """
    Page Object 基类
    
    所有页面的父类，提供：
    1. 统一的元素操作方法（wait_and_click, wait_and_input 等）
    2. 多种元素定位策略自动切换
    3. 显式等待机制
    4. 自动失败截图
    5. 操作日志记录
    """
    
    # 默认超时时间（秒）
    DEFAULT_TIMEOUT = 15
    # 轮询间隔（秒）
    POLL_FREQUENCY = 0.5
    
    def __init__(self, driver: WebDriver):
        """
        初始化页面
        
        Args:
            driver: Appium WebDriver 实例
        """
        self.driver = driver
        self.logger = get_logger(f"Page.{self.__class__.__name__}")
        self.screenshot_util = ScreenshotUtil(driver)
        
        self.logger.info(f"📄 进入页面: {self.__class__.__name__}")
    
    # ==================== 元素定位 ====================
    
    def _find_element(
        self, 
        locator: Tuple[str, str], 
        timeout: int = DEFAULT_TIMEOUT,
        auto_screenshot: bool = True
    ):
        """
        查找单个元素（带显式等待）
        
        Args:
            locator: 定位器 (By类型, 值)
            timeout: 超时时间
            auto_screenshot: 失败时是否自动截图
            
        Returns:
            WebElement 或 None
        """
        try:
            element = WebDriverWait(self.driver, timeout, self.POLL_FREQUENCY).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except Exception as e:
            self.logger.warning(f"⚠️ 元素未找到: {locator} | {e}")
            if auto_screenshot:
                self.screenshot_util.capture(f"fail_{self.__class__.__name__}")
            raise
    
    def _find_elements(
        self, 
        locator: Tuple[str, str], 
        timeout: int = DEFAULT_TIMEOUT
    ) -> List:
        """查找多个元素"""
        try:
            elements = WebDriverWait(self.driver, timeout, self.POLL_FREQUENCY).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except Exception as e:
            self.logger.warning(f"⚠️ 元素列表未找到: {locator} | {e}")
            return []
    
    # ==================== 核心操作 ====================
    
    def wait_and_click(
        self, 
        locator: Tuple[str, str], 
        timeout: int = DEFAULT_TIMEOUT,
        description: str = None
    ) -> "BasePage":
        """
        等待元素可见并点击
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
            description: 操作描述（用于日志）
            
        Returns:
            self (支持链式调用)
        """
        desc = description or f"点击 {locator}"
        self.logger.info(f"👆 {desc}")
        
        element = self._find_element(locator, timeout)
        try:
            element.click()
        except Exception:
            # 尝试使用 JavaScript 点击（解决 iOS 偶发点击失败问题）
            self.logger.debug("尝试 JS Click...")
            self.driver.execute_script("arguments[0].click();", element)
        
        time.sleep(0.3)  # 短暂等待 UI 响应
        return self
    
    def wait_and_input(
        self, 
        locator: Tuple[str, str], 
        text: str,
        timeout: int = DEFAULT_TIMEOUT,
        clear_first: bool = True,
        description: str = None
    ) -> "BasePage":
        """
        等待元素可见并输入文本
        
        Args:
            locator: 元素定位器
            text: 输入文本
            timeout: 超时时间
            clear_first: 是否先清空输入框
            description: 操作描述
            
        Returns:
            self (支持链式调用)
        """
        desc = description or f"输入 '{text}' 到 {locator}"
        self.logger.info(f"⌨️  {desc}")
        
        element = self._find_element(locator, timeout)
        
        if clear_first:
            element.clear()
            time.sleep(0.2)
        
        element.send_keys(text)
        time.sleep(0.3)
        return self
    
    def wait_and_get_text(
        self, 
        locator: Tuple[str, str],
        timeout: int = DEFAULT_TIMEOUT
    ) -> str:
        """获取元素文本"""
        element = self._find_element(locator, timeout)
        text = element.text
        self.logger.debug(f"📝 获取文本: {text}")
        return text
    
    def wait_and_check_visible(
        self, 
        locator: Tuple[str, str],
        timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        """检查元素是否可见"""
        try:
            self._find_element(locator, timeout)
            return True
        except Exception:
            return False
    
    # ==================== 手势操作 ====================
    
    def swipe_up(self, duration: int = 800):
        """向上滑动（内容向下滚动）"""
        size = self.driver.get_window_size()
        start_x = size["width"] / 2
        start_y = size["height"] * 0.7
        end_y = size["height"] * 0.3
        
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)
        self.logger.debug("👆 向上滑动")
        time.sleep(0.5)
        return self
    
    def swipe_down(self, duration: int = 800):
        """向下滑动（内容向上滚动）"""
        size = self.driver.get_window_size()
        start_x = size["width"] / 2
        start_y = size["height"] * 0.3
        end_y = size["height"] * 0.7
        
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)
        self.logger.debug("👇 向下滑动")
        time.sleep(0.5)
        return self
    
    def swipe_left(self, duration: int = 500):
        """向左滑动"""
        size = self.driver.get_window_size()
        start_x = size["width"] * 0.8
        end_x = size["width"] * 0.2
        y = size["height"] / 2
        
        self.driver.swipe(start_x, y, end_x, y, duration)
        self.logger.debug("⬅️ 向左滑动")
        time.sleep(0.5)
        return self
    
    def tap_by_coordinate(self, x: int, y: int):
        """通过坐标点击"""
        from appium.webdriver.common.touch_action import TouchAction
        action = TouchAction(self.driver)
        action.tap(x=x, y=y).perform()
        self.logger.debug(f"👆 坐标点击 ({x}, {y})")
        time.sleep(0.3)
        return self
    
    # ==================== 等待方法 ====================
    
    def wait_for_text_present(
        self, 
        text: str, 
        timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        """等待指定文本出现在屏幕上"""
        try:
            WebDriverWait(self.driver, timeout, self.POLL_FREQUENCY).until(
                lambda d: text in d.page_source
            )
            return True
        except Exception:
            self.logger.warning(f"⏰ 文本未出现: {text}")
            return False
    
    def wait_for_page_load(self, timeout: int = 10):
        """等待页面加载完成（通过判断 activity）"""
        # iOS 上可以检查当前 bundle identifier 或 page source 变化
        time.sleep(1)  # 最小等待
        # 实际场景中可以根据具体 App 特征来判断
        self.logger.debug("⏳ 等待页面加载")
    
    def custom_wait(self, condition, timeout: int = DEFAULT_TIMEOUT):
        """自定义等待条件"""
        return WebDriverWait(self.driver, timeout, self.POLL_FREQUENCY).until(condition)
    
    # ==================== 截图 & 日志 ====================
    
    def capture_screen(self, name: str = "") -> str:
        """截取当前屏幕"""
        return self.screenshot_util.capture(name or f"{self.__class__.__name__}")
    
    def log_step(self, message: str):
        """记录操作步骤到日志"""
        self.logger.info(f"📍 [步骤] {message}")
