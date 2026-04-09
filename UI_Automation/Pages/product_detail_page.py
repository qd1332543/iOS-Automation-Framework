"""商品详情页 - 云鹿商城"""
import time
from appium.webdriver.common.appiumby import AppiumBy

from UI_Automation.Pages.base_page import BasePage
from UI_Automation.Pages.cart_page import CartPage


class ProductDetailPage(BasePage):
    """云鹿商城 - 商品详情页 Page Object"""
    
    # 商品图片轮播
    _IMAGE_BANNER = (AppiumBy.ACCESSIBILITY_ID, "product_image_gallery")
    _IMAGE_INDICATOR = (
        AppiumBy.XPATH,
        "//XCUIElementTypePageIndicator"
    )
    
    # 商品信息
    _PRODUCT_NAME = (AppiumBy.ACCESSIBILITY_ID, "product_name_label")
    _PRODUCT_PRICE = (AppiumBy.ACCESSIBILITY_ID, "product_price_label")
    _ORIGINAL_PRICE = (AppiumBy.ACCESSIBILITY_ID, "original_price_label")
    _SALES_COUNT = (AppiumBy.ACCESSIBILITY_ID, "sales_count_label")
    
    # 规格选择
    _SPEC_SELECTOR = (AppiumBy.ACCESSIBILITY_ID, "spec_selector")
    _SPEC_OPTION = (
        AppiumBy.XPATH,
        "//XCUIElementTypeButton[contains(@name, '{spec}')]"
    )
    _SIZE_OPTION = (
        AppiumBy.XPATH,
        "//XCUIElementTypeButton[contains(@name, '{size}')]"
    )
    
    # 数量选择
    _QUANTITY_MINUS = (AppiumBy.ACCESSIBILITY_ID, "quantity_minus")
    _QUANTITY_VALUE = (AppiumBy.ACCESSIBILITY_ID, "quantity_value")
    _QUANTITY_PLUS = (AppiumBy.ACCESSIBILITY_ID, "quantity_plus")
    
    # 操作按钮
    _ADD_TO_CART_BTN = (AppiumBy.ACCESSIBILITY_ID, "add_to_cart_button")
    _BUY_NOW_BTN = (AppiumBy.ACCESSIBILITY_ID, "buy_now_button")
    _COLLECT_BTN = (AppiumBy.ACCESSIBILITY_ID, "collect_button")
    _SHARE_BTN = (AppiumBy.ACCESSIBILITY_ID, "share_button")
    
    # 返回
    _BACK_BTN = (AppiumBy.ACCESSIBILITY_ID, "navigation_back")

    def get_product_name(self) -> str:
        """获取商品名称"""
        return self.wait_and_get_text(self._PRODUCT_NAME)
    
    def get_product_price(self) -> str:
        """获取商品价格"""
        return self.wait_and_get_text(self._PRODUCT_PRICE)
    
    def select_spec(self, spec: str) -> "ProductDetailPage":
        """选择规格"""
        self.log_step(f"选择规格: {spec}")
        locator = (AppiumBy.XPATH, f"//XCUIElementTypeButton[contains(@name, '{spec}')]")
        self.wait_and_click(locator)
        time.sleep(0.3)
        return self
    
    def select_size(self, size: str) -> "ProductDetailPage":
        """选择尺寸"""
        self.log_step(f"选择尺码: {size}")
        locator = (AppiumBy.XPATH, f"//XCUIElementTypeButton[contains(@name, '{size}')]")
        self.wait_and_click(locator)
        time.sleep(0.3)
        return self
    
    def increase_quantity(self) -> "ProductDetailPage":
        """增加数量 (+1)"""
        self.log_step("增加购买数量")
        self.wait_and_click(self._QUANTITY_PLUS)
        time.sleep(0.2)
        return self
    
    def decrease_quantity(self) -> "ProductDetailPage":
        """减少数量 (-1)"""
        self.log_step("减少购买数量")
        self.wait_and_click(self._QUANTITY_MINUS)
        time.sleep(0.2)
        return self
    
    def get_quantity(self) -> str:
        """获取当前数量"""
        return self.wait_and_get_text(self._QUANTITY_VALUE)
    
    def add_to_cart(self) -> "ProductDetailPage":
        """加入购物车"""
        self.log_step("加入购物车")
        self.wait_and_click(self._ADD_TO_CART_BTN)
        # 等待加入成功提示
        time.sleep(1.5)
        return self
    
    def buy_now(self) -> CartPage:
        """立即购买"""
        self.log_step("立即购买")
        self.wait_and_click(self._BUY_NOW_BTN)
        time.sleep(1.5)
        return CartPage(self.driver)
    
    def collect(self) -> "ProductDetailPage":
        """收藏商品"""
        self.log_step("收藏商品")
        self.wait_and_click(self._COLLECT_BTN)
        time.sleep(0.5)
        return self
    
    def go_back(self):
        """返回上一页"""
        self.log_step("返回上一页")
        self.wait_and_click(self._BACK_BTN)
        time.sleep(0.5)
    
    def swipe_image_left(self) -> "ProductDetailPage":
        """左滑查看下一张图"""
        self.log_step("查看下一张商品图")
        self.swipe_left(duration=400)
        time.sleep(0.5)
        return self
