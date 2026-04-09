"""
首页 - 云鹿商城

功能：
- Banner 轮播
- 分类导航入口
- 推荐商品列表
- 搜索入口
- 底部 Tab 导航
"""
import time
from appium.webdriver.common.appiumby import AppiumBy

from UI_Automation.Pages.base_page import BasePage
from UI_Automation.Pages.search_page import SearchPage
from UI_Automation.Pages.category_page import CategoryPage
from UI_Automation.Pages.product_detail_page import ProductDetailPage


class HomePage(BasePage):
    """云鹿商城 - 首页 Page Object"""
    
    # ========== 元素定位 ==========
    
    # Banner 区域
    _BANNER_CONTAINER = (AppiumBy.ACCESSIBILITY_ID, "home_banner_view")
    _BANNER_INDICATOR = (
        AppiumBy.XPATH,
        "//XCUIElementTypePageIndicator"
    )
    
    # 搜索框
    _SEARCH_BAR = (AppiumBy.ACCESSIBILITY_ID, "home_search_bar")
    _SEARCH_BAR_XPATH = (
        AppiumBy.XPATH,
        "//XCUIElementTypeSearchField[@name='搜索商品']"
    )
    
    # 分类图标区域（横向滚动的分类入口）
    _CATEGORY_ICON_AREA = (AppiumBy.ACCESSIBILITY_ID, "category_icon_scroll")
    
    # 具体分类图标
    _CATEGORY_ICON_TEMPLATE = (
        AppiumBy.XPATH,
        "//XCUIElementTypeImage[@name='{category_name}']/parent::*/preceding-sibling::* | //XCUIElementTypeStaticText[@name='{category_name}']"
    )
    
    # 商品列表区域
    _PRODUCT_LIST = (AppiumBy.ACCESSIBILITY_ID, "home_product_list")
    _PRODUCT_ITEM = (
        AppiumBy.XPATH,
        "//XCUIElementTypeOther[contains(@label, 'product_item')]"
    )
    _PRODUCT_CARD = (
        AppiumBy.XPATH,
        "//XCUIElementTypeOther[contains(@identifier, 'goods_card')]"
    )
    
    # 下拉刷新控件
    _PULL_TO_REFRESH = (
        AppiumBy.ACCESSIBILITY_ID,
        "pull_to_refresh_control"
    )
    
    # 底部 Tab 栏
    _TAB_HOME = (AppiumBy.ACCESSIBILITY_ID, "tab_home")
    _TAB_CATEGORY = (AppiumBy.ACCESSIBILITY_ID, "tab_category")
    _TAB_CART = (AppiumBy.ACCESSIBILITY_ID, "tab_cart")
    _TAB_PROFILE = (AppiumBy.ACCESSIBILITY_ID, "tab_profile")
    
    # 首页通知/活动弹窗（可能存在）
    _POPUP_CLOSE_BTN = (
        AppiumBy.XPATH,
        "//XCUIElementTypeButton[@name='close' or @name='关闭' or @name='我知道了']"
    )
    
    # ========== 业务操作 ==========
    
    def is_on_home_page(self) -> bool:
        """判断是否在首页"""
        return self.wait_and_check_visible(self._SEARCH_BAR, timeout=5) or \
               self.wait_and_check_visible(self._TAB_HOME, timeout=3)
    
    def close_popup_if_exists(self) -> "HomePage":
        """关闭可能出现的弹窗"""
        if self.wait_and_check_visible(self._POPUP_CLOSE_BTN, timeout=2):
            self.log_step("关闭弹窗")
            self.wait_and_click(self._POPUP_CLOSE_BTN)
            time.sleep(0.5)
        return self
    
    def click_search(self) -> SearchPage:
        """点击搜索栏，进入搜索页"""
        self.log_step("点击搜索栏")
        try:
            self.wait_and_click(self._SEARCH_BAR)
        except Exception:
            self.wait_and_click(self._SEARCH_BAR_XPATH)
        return SearchPage(self.driver)
    
    def tap_category(self, category_name: str) -> CategoryPage:
        """
        点击指定分类
        
        Args:
            category_name: 分类名称（如"数码"、"服饰"）
        """
        self.log_step(f"点击分类: {category_name}")
        locator = (
            AppiumBy.XPATH,
            f"//XCUIElementTypeStaticText[@name='{category_name}' or @value='{category_name}']"
        )
        self.wait_and_click(locator)
        return CategoryPage(self.driver)
    
    def click_first_product(self) -> ProductDetailPage:
        """点击第一个推荐商品，进入详情页"""
        self.log_step("点击第一个商品")
        try:
            self.wait_and_click(self._PRODUCT_CARD, timeout=5)
        except Exception:
            self.wait_and_click(self._PRODUCT_ITEM, timeout=5)
        return ProductDetailPage(self.driver)
    
    def pull_to_refresh(self) -> "HomePage":
        """下拉刷新"""
        self.log_step("下拉刷新首页")
        size = self.driver.get_window_size()
        start_x = size["width"] / 2
        start_y = size["height"] * 0.3
        end_y = size["height"] * 0.7
        self.driver.swipe(start_x, start_y, start_x, end_y, 800)
        time.sleep(2)  # 等待刷新完成
        return self
    
    def scroll_to_bottom(self) -> "HomePage":
        """滑动到底部加载更多"""
        self.log_step("滚动到页面底部加载更多")
        for i in range(3):
            self.swipe_up()
        return self
    
    def tap_cart_tab(self):
        """点击底部购物车 Tab"""
        from UI_Automation.Pages.cart_page import CartPage
        self.log_step("切换到购物车Tab")
        self.wait_and_click(self._TAB_CART)
        return CartPage(self.driver)
    
    def tap_profile_tab(self):
        """点击底部我的 Tab"""
        self.log_step("切换到我的Tab")
        self.wait_and_click(self._TAB_PROFILE)
        return self
    
    def get_banner_count(self) -> int:
        """获取当前 Banner 数量"""
        indicators = self._find_elements(self._BANNER_INDICATOR, timeout=3)
        return len(indicators)
    
    def swipe_banner_left(self) -> "HomePage":
        """向左滑动 Banner（切换下一张）"""
        self.log_step("切换 Banner")
        banner = self._find_element(self._BANNER_CONTAINER, timeout=5)
        size = banner.size
        location = banner.location
        start_x = size["width"] * 0.8 + location["x"]
        end_x = size["width"] * 0.2 + location["x"]
        y = size["height"] / 2 + location["y"]
        self.driver.swipe(start_x, y, end_x, y, 500)
        time.sleep(1)
        return self
