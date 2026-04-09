"""
登录页 - 云鹿商城

功能：
- 手机号 + 验证码登录
- 密码登录
- 协议勾选
- 第三方登录（微信/Apple ID）
"""
from appium.webdriver.common.appiumby import AppiumBy

from UI_Automation.Pages.base_page import BasePage
from UI_Automation.Pages.home_page import HomePage


class LoginPage(BasePage):
    """云鹿商城 - 登录页 Page Object"""
    
    # ========== 元素定位 ==========
    # 使用 Accessibility ID 作为首选方案（iOS 最佳实践）
    
    # 手机号输入框
    _PHONE_INPUT = (AppiumBy.ACCESSIBILITY_ID, "phone_number_text_field")
    # 备选 XPath
    _PHONE_INPUT_XPATH = (
        AppiumBy.XPATH, 
        "//XCUIElementTypeTextField[@name='请输入手机号' or @placeholder='请输入手机号']"
    )
    
    # 验证码输入框  
    _CODE_INPUT = (AppiumBy.ACCESSIBILITY_ID, "verification_code_text_field")
    _CODE_INPUT_XPATH = (
        AppiumBy.XPATH,
        "//XCUIElementTypeTextField[@name='请输入验证码' or @placeholder='请输入验证码']"
    )
    
    # 获取验证码按钮
    _GET_CODE_BTN = (AppiumBy.ACCESSIBILITY_ID, "get_verification_code_button")
    _GET_CODE_BTN_XPATH = (
        AppiumBy.XPATH,
        "//XCUIElementTypeButton[@name='获取验证码']"
    )
    
    # 登录按钮
    _LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "login_button")
    _LOGIN_BUTTON_XPATH = (
        AppiumBy.XPATH,
        "//XCUIElementTypeButton[@name='登录']"
    )
    
    # 用户协议勾选框
    _AGREE_CHECKBOX = (
        AppiumBy.XPATH,
        "//XCUIElementTypeSwitch[@name='agree_switch']"
    )
    
    # 密码登录切换
    _PASSWORD_LOGIN_TAB = (
        AppiumBy.ACCESSIBILITY_ID,
        "password_login_tab"
    )
    
    # 密码输入框
    _PASSWORD_INPUT = (
        AppiumBy.ACCESSIBILITY_ID,
        "password_text_field"
    )
    
    # 微信登录按钮
    _WECHAT_LOGIN_BTN = (
        AppiumBy.XPATH,
        "//XCUIElementTypeButton[contains(@name, '微信')]"
    )
    
    # Apple 登录按钮
    _APPLE_LOGIN_BTN = (
        AppiumBy.XPATH,
        "//XCUIElementTypeButton[@value='Sign in with Apple' or contains(@name, 'Apple')]"
    )
    
    # ========== 业务操作 ==========
    
    def input_phone(self, phone: str) -> "LoginPage":
        """
        输入手机号
        
        Args:
            phone: 11位手机号
        """
        self.log_step(f"输入手机号: {phone[:3]}****{phone[-4:]}")
        # 尝试主定位方式，失败则用备选
        try:
            self.wait_and_input(self._PHONE_INPUT, phone)
        except Exception:
            self.wait_and_input(self._PHONE_INPUT_XPATH, phone)
        return self
    
    def input_code(self, code: str) -> "LoginPage":
        """
        输入验证码
        
        Args:
            code: 6位验证码
        """
        self.log_step("输入验证码")
        try:
            self.wait_and_input(self._CODE_INPUT, code)
        except Exception:
            self.wait_and_input(self._CODE_INPUT_XPATH, code)
        return self
    
    def input_password(self, password: str) -> "LoginPage":
        """输入密码"""
        self.log_step("输入密码")
        self.wait_and_input(self._PASSWORD_INPUT, password)
        return self
    
    def click_get_code(self) -> "LoginPage":
        """点击获取验证码按钮"""
        self.log_step("点击获取验证码")
        try:
            self.wait_and_click(self._GET_CODE_BTN)
        except Exception:
            self.wait_and_click(self._GET_CODE_BTN_XPATH)
        # 等待倒计时开始
        time.sleep(1)
        return self
    
    def click_login(self) -> HomePage:
        """
        点击登录按钮
        
        Returns:
            HomePage - 登录成功后跳转到首页
        """
        self.log_step("点击登录按钮")
        try:
            self.wait_and_click(self._LOGIN_BUTTON, description="登录按钮")
        except Exception:
            self.wait_and_click(self._LOGIN_BUTTON_XPATH, description="登录按钮(备选)")
        
        # 等待首页加载
        self.wait_for_page_load()
        return HomePage(self.driver)
    
    def agree_protocol(self) -> "LoginPage":
        """勾选用户协议"""
        self.log_step("勾选用户协议")
        if not self.wait_and_check_visible(self._AGREE_CHECKBOX, timeout=3):
            self.logger.warning("协议勾选框不可见，可能已默认勾选")
        else:
            self.wait_and_click(self._AGREE_CHECKBOX)
        return self
    
    def switch_to_password_login(self) -> "LoginPage":
        """切换到密码登录模式"""
        self.log_step("切换到密码登录")
        self.wait_and_click(self._PASSWORD_LOGIN_TAB)
        return self
    
    def login_with_code(self, phone: str, code: str) -> HomePage:
        """
        验证码登录完整流程（链式调用）
        
        Args:
            phone: 手机号
            code: 验证码
            
        Returns:
            HomePage
        """
        return (self.agree_protocol()
                   .input_phone(phone)
                   .input_code(code)
                   .click_login())
    
    def login_with_password(self, phone: str, password: str) -> HomePage:
        """
        密码登录完整流程
        
        Args:
            phone: 手机号
            password: 密码
            
        Returns:
            HomePage
        """
        return (self.agree_protocol()
                   .input_phone(phone)
                   .switch_to_password_login()
                   .input_password(password)
                   .click_login())
    
    def is_on_login_page(self) -> bool:
        """判断当前是否在登录页"""
        return (self.wait_and_check_visible(self._LOGIN_BUTTON, timeout=3) or
                self.wait_and_check_visible(self._LOGIN_BUTTON_XPATH, timeout=2))
    
    def wechat_login(self) -> HomePage:
        """微信快捷登录"""
        self.log_step("微信登录")
        self.wait_and_click(self._WECHAT_LOGIN_BTN)
        self.wait_for_page_load()
        return HomePage(self.driver)
    
    def apple_login(self) -> HomePage:
        """Apple ID 登录"""
        self.log_step("Apple ID 登录")
        self.wait_and_click(self._APPLE_LOGIN_BTN)
        self.wait_for_page_load()
        return HomePage(self.driver)


# 避免循环导入问题，在文件末尾导入 time
import time
