"""分类页 - 云鹿商城"""
import time
from appium.webdriver.common.appiumby import AppiumBy

from UI_Automation.Pages.base_page import BasePage
from UI_Automation.Pages.product_detail_page import ProductDetailPage


class CategoryPage(BasePage):
    """云鹿商城 - 分类页 Page Object"""
    
    # 左侧一级分类
    _CATEGORY_LEFT_LIST = (
        AppiumBy.ACCESSIBILITY_ID, 
        "left_category_list"
    )
    _CATEGORY_LEFT_ITEM = (
        AppiumBy.IOS_CLASS_CHAIN,
        "**/XCUIElementTypeTable/XCUIElementTypeCell"
    )
    
    # 右侧二级分类 / 商品
    _RIGHT_CONTENT = (
        AppiumBy.ACCESSIBILITY_ID,
        "right_content_area"
    )
    # 右侧二级分类 / 商品（动态构建，见 select_sub_category 方法）
    _CATEGORY_PRODUCT = (
        AppiumBy.IOS_PREDICATE,
        "type == 'XCUIElementTypeOther' AND identifier CONTAINS 'category_product'"
    )
    
    # 筛选排序
    _SORT_BTN = (AppiumBy.ACCESSIBILITY_ID, "sort_button")
    _FILTER_BTN = (AppiumBy.ACCESSIBILITY_ID, "filter_button")
    _PRICE_SORT = (
        AppiumBy.IOS_PREDICATE,
        "type == 'XCUIElementTypeButton' AND name CONTAINS '价格'"
    )
    _SALES_SORT = (
        AppiumBy.IOS_PREDICATE,
        "type == 'XCUIElementTypeButton' AND name CONTAINS '销量'"
    )
    
    def select_main_category(self, name: str) -> "CategoryPage":
        """选择左侧一级分类"""
        self.log_step(f"选择一级分类: {name}")
        locator = (AppiumBy.IOS_PREDICATE, f"type == 'XCUIElementTypeStaticText' AND name == '{self._predicate_escape(name)}'")
        self.wait_and_click(locator)
        time.sleep(0.8)
        return self
    
    def sort_by_price(self, ascending: bool = True) -> "CategoryPage":
        """按价格排序"""
        direction = "升序" if ascending else "降序"
        self.log_step(f"按价格{direction}排序")
        self.wait_and_click(self._PRICE_SORT)
        time.sleep(1)
        return self
    
    def sort_by_sales(self) -> "CategoryPage":
        """按销量排序"""
        self.log_step("按销量排序")
        self.wait_and_click(self._SALES_SORT)
        time.sleep(1)
        return self
    
    def click_first_product(self) -> ProductDetailPage:
        """点击分类下第一个商品"""
        self.log_step("点击分类中第一个商品")
        self.wait_and_click(self._CATEGORY_PRODUCT, timeout=10)
        return ProductDetailPage(self.driver)
    
    def get_product_count(self) -> int:
        """获取分类下商品数量"""
        products = self._find_elements(self._CATEGORY_PRODUCT, timeout=5)
        return len(products)
