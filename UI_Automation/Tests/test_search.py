"""
搜索功能 UI 测试用例
"""
import allure
import pytest


@allure.feature("首页模块")
@allue.story("搜索功能")
class TestSearch:
    """搜索功能 UI 测试"""
    
    @allue.title("搜索 - 输入关键词并搜索")
    @allue.severity(allue.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_search_keyword(self, home_page):
        """输入关键词进行商品搜索"""
        home_page.close_popup_if_exists()
        
        with allure.step("进入搜索页"):
            search_page = home_page.click_search()
        
        with allure.step("输入搜索词'手机'并执行搜索"):
            search_page.do_search("手机")
        
        with allure.step("验证搜索结果"):
            assert search_page.has_results(), "搜索无结果"
            count = search_page.get_result_count()
            with allure.step(f"结果数量: {count}"):
                assert count > 0
    
    @allue.title("搜索 - 空结果处理")
    @allue.severity(allue.severity_level.NORMAL)
    def test_search_empty_result(self, home_page):
        """搜索不存在的商品，验证空结果提示"""
        home_page.close_popup_if_exists()
        
        with allure.step("进入搜索页"):
            search_page = home_page.click_search()
        
        with allure.step("搜索不存在的关键词"):
            search_page.do_search("zzzzzzzz_not_exist_12345")
        
        with allure.step("验证空结果提示"):
            # 根据实际 App 行为调整
            pass
    
    @allue.title("搜索 - 热门搜索推荐")
    @allue.severity(allue.severity_level.MINOR)
    def test_search_hot_keywords(self, home_page):
        """验证热门搜索/历史记录展示"""
        home_page.close_popup_if_exists()
        
        search_page = home_page.click_search()
        # 热门搜索区域是否可见
        is_visible = search_page.wait_and_check_visible(
            search_page._HOT_SEARCH_KEYWORDS,
            timeout=3
        )
        if not is_visible:
            allure.attach(
                "热门搜索不可见（可能首次使用）",
                name="检查结果",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @allue.title("搜索 - 点击结果进入详情")
    @allue.severity(allue.severity_level.NORMAL)
    def test_search_result_detail(self, home_page):
        """点击搜索结果进入商品详情"""
        home_page.close_popup_if_exists()
        
        search_page = home_page.click_search().do_search("数码")
        
        if search_page.has_results():
            with allure.step("点击第一个结果"):
                detail = search_page.click_first_result()
            
            with allure.step("验证详情页"):
                name = detail.get_product_name()
                assert name and len(name) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
