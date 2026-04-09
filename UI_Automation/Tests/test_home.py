"""
首页功能 UI 测试用例

覆盖场景：
- Banner 轮播展示与切换
- 分类导航点击
- 推荐商品加载
- 搜索入口
- 下拉刷新
- 底部 Tab 导航切换
"""
import allure
import pytest


@allure.feature("首页模块")
@allure.story("首页功能")
class TestHome:
    """首页功能 UI 测试"""
    
    @allure.title("首页加载 - 元素完整展示")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_home_page_load(self, home_page):
        """
        验证首页加载完成后所有核心元素可见
        """
        with allure.step("关闭可能的弹窗"):
            home_page.close_popup_if_exists()
        
        with allure.step("验证搜索栏可见"):
            assert home_page.is_on_home_page(), "首页加载失败"
        
        with allure.step("截图记录首页状态"):
            home_page.capture_screen("home_loaded")
    
    @allure.title("Banner 轮播展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_home_banner_display(self, home_page):
        """验证 Banner 区域正常展示"""
        home_page.close_popup_if_exists()
        
        count = home_page.get_banner_count()
        with allure.step(f"Banner 数量: {count}"):
            assert count >= 1, "Banner 未显示"
            
        # 切换一次 Banner
        with allure.step("左滑切换 Banner"):
            home_page.swipe_banner_left()
    
    @allure.title("下拉刷新功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_home_pull_to_refresh(self, home_page):
        """验证首页下拉刷新功能正常"""
        home_page.close_popup_if_exists()
        
        with allure.step("执行下拉刷新"):
            refreshed_page = home_page.pull_to_refresh()
        
        with allure.step("验证刷新后页面仍然正常"):
            assert refreshed_page.is_on_home_page(), "刷新后首页异常"
    
    @allure.title("点击搜索栏进入搜索页")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_home_search_entry(self, home_page):
        """从首页进入搜索功能"""
        home_page.close_popup_if_exists()
        
        with allure.step("点击搜索栏"):
            search_page = home_page.click_search()
        
        with allure.step("验证进入搜索页"):
            # SearchPage 应该有搜索框
            assert search_page is not None
    
    @allure.title("分类导航 - 点击数码分类")
    @allure.severity(allure.severity_level.NORMAL)
    def test_home_category_navigation(self, home_page):
        """通过首页分类导航进入分类页"""
        home_page.close_popup_if_exists()
        
        with allure.step("点击'数码'分类"):
            category_page = home_page.tap_category("数码")
        
        with allure.step("验证进入分类页"):
            # CategoryPage 对象创建成功即表示导航正常
            assert category_page is not None
    
    @allure.title("推荐商品列表加载")
    @allure.severity(allure.severity_level.NORMAL)
    def test_home_product_list(self, home_page):
        """验证推荐商品列表可以正常加载和展示"""
        home_page.close_popup_if_exists()
        
        with allure.step("点击第一个商品进入详情"):
            detail_page = home_page.click_first_product()
        
        with allure.step("验证商品详情页加载"):
            product_name = detail_page.get_product_name()
            assert product_name and len(product_name) > 0, "商品名称为空"
    
    @allue.title("底部Tab导航 - 切换到购物车")
    @allue.severity(allue.severity_level.NORMAL)
    def test_home_tab_cart(self, home_page):
        """底部 Tab 导航 - 切换到购物车"""
        home_page.close_popup_if_exists()
        
        cart_page = home_page.tap_cart_tab()
        assert cart_page is not None
    
    @allue.title("滚动加载更多商品")
    @allue.severity(allue.severity_level.MINOR)
    def test_home_scroll_load_more(self, home_page):
        """滑动到底部触发加载更多"""
        home_page.close_popup_if_exists()
        
        with allure.step("向下滚动加载更多"):
            home_page.scroll_to_bottom()
        
        with allure.step("验证页面仍正常"):
            assert home_page.is_on_home_page()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
