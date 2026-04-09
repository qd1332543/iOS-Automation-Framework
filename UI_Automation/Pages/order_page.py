"""订单确认/订单列表页 - 云鹿商城"""
import time
from appium.webdriver.common.appiumby import AppiumBy

from UI_Automation.Pages.base_page import BasePage


class OrderPage(BasePage):
    """云鹿商城 - 订单页 Page Object"""
    
    # 收货地址
    _ADDRESS_SELECTOR = (AppiumBy.ACCESSIBILITY_ID, "address_selector")
    _ADDRESS_INFO = (AppiumBy.ACCESSIBILITY_ID, "address_info_label")
    
    # 支付方式
    _PAYMENT_METHOD = (
        AppiumBy.XPATH,
        "//XCUIElementTypeButton[contains(@name, '{method}')]"
    )
    _WECHAT_PAY = (
        AppiumBy.XPATH,
        "//XCUIElementTypeButton[contains(@name, '微信支付') or contains(@name, '微信')]"
    )
    _ALI_PAY = (
        AppiumBy.XPATH,
        "//XCUIElementTypeButton[contains(@name, '支付宝') or contains(@name, 'Alipay')]"
    )
    
    # 订单金额
    _ORDER_AMOUNT = (AppiumBy.ACCESSIBILITY_ID, "order_amount")
    _DISCOUNT_LABEL = (AppiumBy.ACCESSIBILITY_ID, "discount_info")
    
    # 提交订单
    _SUBMIT_ORDER_BTN = (AppiumBy.ACCESSIBILITY_ID, "submit_order_button")
    
    # 订单列表
    _ORDER_LIST = (AppiumBy.ACCESSIBILITY_ID, "order_list")
    _ORDER_ITEM = (
        AppiumBy.XPATH,
        "//XCUIElementTypeOther[contains(@identifier, 'order_item')]"
    )
    _ORDER_STATUS = (
        AppiumBy.XPATH,
        "//XCUIElementTypeStaticText[contains(@name, 'status')]"
    )
    
    # 订单状态筛选
    _STATUS_TAB_ALL = (AppiumBy.ACCESSIBILITY_ID, "tab_all_orders")
    _STATUS_TAB_PENDING = (
        AppiumBy.ACCESSIBILITY_ID,
        "tab_pending_payment"
    )
    _STATUS_TAB_SHIPPING = (AppiumBy.ACCESSIBILITY_ID, "tab_shipping")
    _STATUS_TAB_COMPLETED = (AppiumBy.ACCESSIBILITY_ID, "tab_completed")
    
    def select_address(self) -> "OrderPage":
        """选择收货地址"""
        self.log_step("选择收货地址")
        self.wait_and_click(self._ADDRESS_SELECTOR)
        time.sleep(1)
        return self
    
    def select_wechat_pay(self) -> "OrderPage":
        """选择微信支付"""
        self.log_step("选择微信支付")
        self.wait_and_click(self._WECHAT_PAY)
        return self
    
    def select_alipay(self) -> "OrderPage":
        """选择支付宝支付"""
        self.log_step("选择支付宝")
        self.wait_and_click(self._ALI_PAY)
        return self
    
    def submit_order(self) -> "OrderPage":
        """提交订单"""
        self.log_step("提交订单")
        self.wait_and_click(self._SUBMIT_ORDER_BTN)
        time.sleep(2)
        return self
    
    def get_order_amount(self) -> str:
        """获取订单金额"""
        return self.wait_and_get_text(self._ORDER_AMOUNT)
    
    def filter_by_status(self, status: str) -> "OrderPage":
        """按状态筛选订单"""
        self.log_step(f"筛选订单状态: {status}")
        status_map = {
            "全部": self._STATUS_TAB_ALL,
            "待付款": self._STATUS_TAB_PENDING,
            "配送中": self._STATUS_TAB_SHIPPING,
            "已完成": self._STATUS_TAB_COMPLETED,
        }
        tab = status_map.get(status)
        if tab:
            self.wait_and_click(tab)
            time.sleep(1)
        return self
    
    def get_order_count(self) -> int:
        """获取订单数量"""
        orders = self._find_elements(self._ORDER_ITEM, timeout=5)
        return len(orders)
    
    def cancel_order(self) -> "OrderPage":
        """取消首个订单"""
        self.log_step("取消订单")
        orders = self._find_elements(self._ORDER_ITEM, timeout=5)
        if orders:
            orders[0].click()  # 进入订单详情
            time.sleep(1)
            cancel_btn = (AppiumBy.XPATH, "//XCUIElementTypeButton[contains(@name, '取消')]")
            if self.wait_and_check_visible(cancel_btn, timeout=3):
                self.wait_and_click(cancel_btn)
        return self
