"""搜索页 - 云鹿商城"""
import time
from appium.webdriver.common.appiumby import AppiumBy

from UI_Automation.Pages.base_page import BasePage
from UI_Automation.Pages.product_detail_page import ProductDetailPage


class SearchPage(BasePage):
    """云鹿商城 - 搜索页 Page Object"""
    
    # 元素定位
    _SEARCH_INPUT = (AppiumBy.ACCESSIBILITY_ID, "search_input_field")
    _SEARCH_INPUT_XPATH = (
        AppiumBy.IOS_PREDICATE,
        "type == 'XCUIElementTypeSearchField'"
    )
    _SEARCH_BTN = (AppiumBy.ACCESSIBILITY_ID, "search_button")
    _CANCEL_BTN = (AppiumBy.ACCESSIBILITY_ID, "cancel_button")
    _CLEAR_BTN = (AppiumBy.ACCESSIBILITY_ID, "clear_text_btn")
    
    # 搜索结果
    _RESULT_LIST = (AppiumBy.ACCESSIBILITY_ID, "search_result_list")
    _RESULT_EMPTY_TIPS = (
        AppiumBy.IOS_PREDICATE,
        "type == 'XCUIElementTypeStaticText' AND (name == '没有找到相关商品' OR name CONTAINS '暂无')"
    )
    _RESULT_ITEM = (
        AppiumBy.IOS_PREDICATE,
        "type == 'XCUIElementTypeOther' AND identifier CONTAINS 'result_product'"
    )

    # 搜索历史/热搜（动态构建，见各方法）
    _HOT_SEARCH_KEYWORDS = (
        AppiumBy.IOS_PREDICATE,
        "type == 'XCUIElementTypeCollectionView' AND identifier == 'hot_search_list'"
    )

    def input_keyword(self, keyword: str) -> "SearchPage":
        """输入搜索关键词"""
        self.log_step(f"输入搜索词: {keyword}")
        try:
            self.wait_and_input(self._SEARCH_INPUT, keyword)
        except Exception:
            self.wait_and_input(self._SEARCH_INPUT_XPATH, keyword)
        return self
    
    def do_search(self, keyword: str = None) -> "SearchPage":
        """执行搜索"""
        if keyword:
            self.input_keyword(keyword)
        self.log_step("执行搜索")
        self.wait_and_click(self._SEARCH_BTN)
        time.sleep(1.5)
        return self
    
    def clear_search(self) -> "SearchPage":
        """清空搜索内容"""
        self.log_step("清空搜索")
        self.wait_and_click(self._CLEAR_BTN)
        return self
    
    def cancel_search(self) -> "HomePage":
        """取消搜索，返回首页"""
        from UI_Automation.Pages.home_page import HomePage
        self.log_step("取消搜索")
        self.wait_and_click(self._CANCEL_BTN)
        return HomePage(self.driver)
    
    def click_first_result(self) -> ProductDetailPage:
        """点击第一个搜索结果"""
        self.log_step("点击第一个搜索结果")
        self.wait_and_click(self._RESULT_ITEM, timeout=10)
        return ProductDetailPage(self.driver)
    
    def has_results(self) -> bool:
        """是否有搜索结果"""
        return not self.wait_and_check_visible(
            self._RESULT_EMPTY_TIPS, 
            timeout=3
        )
    
    def get_result_count(self) -> int:
        """获取搜索结果数量"""
        items = self._find_elements(self._RESULT_ITEM, timeout=5)
        return len(items)
