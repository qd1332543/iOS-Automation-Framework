"""购物车页 - 云鹿商城"""
from appium.webdriver.common.appiumby import AppiumBy

from UI_Automation.Pages.base_page import BasePage
from UI_Automation.Pages.order_page import OrderPage


class CartPage(BasePage):
    """云鹿商城 - 购物车页 Page Object"""
    
    # 购物车项
    _CART_ITEM = (
        AppiumBy.IOS_PREDICATE,
        "identifier CONTAINS 'cart_item'"
    )
    _CART_ITEM_CHECKBOX = (
        AppiumBy.IOS_PREDICATE,
        "identifier CONTAINS 'item_check' AND type == 'XCUIElementTypeSwitch'"
    )

    # 操作
    _ITEM_DELETE = (
        AppiumBy.IOS_PREDICATE,
        "name CONTAINS '删除' AND type == 'XCUIElementTypeButton'"
    )
    _ITEM_QUANTITY_MINUS = (
        AppiumBy.IOS_PREDICATE,
        "identifier CONTAINS 'minus' AND type == 'XCUIElementTypeButton'"
    )
    _ITEM_QUANTITY_PLUS = (
        AppiumBy.IOS_PREDICATE,
        "identifier CONTAINS 'plus' AND type == 'XCUIElementTypeButton'"
    )
    
    # 全选 & 结算
    _SELECT_ALL = (AppiumBy.ACCESSIBILITY_ID, "select_all_checkbox")
    _CHECKOUT_BTN = (AppiumBy.ACCESSIBILITY_ID, "checkout_button")
    
    # 价格汇总
    _TOTAL_PRICE = (AppiumBy.ACCESSIBILITY_ID, "total_price_label")
    _SELECTED_COUNT = (AppiumBy.ACCESSIBILITY_ID, "selected_count_label")
    
    # 空购物车
    _EMPTY_CART = (
        AppiumBy.IOS_PREDICATE,
        "type == 'XCUIElementTypeStaticText' AND (name == '购物车是空的' OR name CONTAINS '空')"
    )
    
    # 继续购物
    _CONTINUE_SHOPPING = (
        AppiumBy.ACCESSIBILITY_ID,
        "continue_shopping_btn"
    )

    def is_empty(self) -> bool:
        """购物车是否为空"""
        return self.wait_and_check_visible(self._EMPTY_CART, timeout=3)
    
    def select_all_items(self) -> "CartPage":
        """全选所有商品"""
        self.log_step("全选购物车商品")
        self.wait_and_click(self._SELECT_ALL)
        return self
    
    _SWIPE_START_RATIO = 0.8
    _SWIPE_END_RATIO = 0.2
    _SWIPE_DURATION_SECONDS = 0.5

    def delete_first_item(self) -> "CartPage":
        """删除第一个商品"""
        self.log_step("删除第一个商品")
        items = self._find_elements(self._CART_ITEM, timeout=5)
        if items:
            item = items[0]
            size = item.size
            location = item.location
            start_x = int(location["x"] + size["width"] * self._SWIPE_START_RATIO)
            end_x = int(location["x"] + size["width"] * self._SWIPE_END_RATIO)
            y = int(location["y"] + size["height"] / 2)
            self.driver.execute_script("mobile: dragFromToForDuration", {
                "duration": self._SWIPE_DURATION_SECONDS,
                "fromX": start_x, "fromY": y,
                "toX": end_x, "toY": y
            })
            self.wait_and_click(self._ITEM_DELETE)
        return self
    
    def checkout(self) -> OrderPage:
        """去结算"""
        self.log_step("去结算")
        self.wait_and_click(self._CHECKOUT_BTN)
        return OrderPage(self.driver)
    
    def get_total_price(self) -> str:
        """获取总价"""
        return self.wait_and_get_text(self._TOTAL_PRICE)
    
    def get_selected_count(self) -> str:
        """获取已选数量"""
        text = self.wait_and_get_text(self._SELECTED_COUNT)
        return text
    
    def get_item_count(self) -> int:
        """获取购物车商品数量"""
        items = self._find_elements(self._CART_ITEM, timeout=5)
        return len(items)
    
    def continue_shopping(self) -> "CartPage":
        """继续购物"""
        self.log_step("继续购物")
        self.wait_and_click(self._CONTINUE_SHOPPING)
        return self
