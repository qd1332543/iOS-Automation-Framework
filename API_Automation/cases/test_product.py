"""商品模块接口测试"""
import allure
import pytest
from API_Automation.api.product_api import ProductAPI
from utils.assertion_util import AssertUtil


@allure.feature("商品模块")
@allue.story("商品搜索")
class TestProductSearch:
    """商品搜索接口测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, request_util):
        self.product_api = ProductAPI(request_util)
        self.assertion = AssertUtil()
    
    @allue.title("搜索关键词'手机'- 应有结果")
    @allue.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_search_phone(self):
        with allure.step("搜索'手机'"):
            result = self.product_api.search_products(keyword="手机")
        
        self.assertion.assert_response_code(result)
        
        products = result.get("data", {}).get("products", [])
        with allure.step(f"结果数量: {len(products)}"):
            assert len(products) > 0, "搜索无结果"
    
    @allue.title("搜索不存在的商品- 返回空列表")
    @allue.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_search_not_exist(self):
        with allure.step("搜索不存在的关键词"):
            result = self.product_api.search_products(
                keyword="zzzz_not_exist_2024"
            )
        
        self.assertion.assert_response_code(result)
        products = result.get("data", {}).get("products", [])
        assert len(products) == 0, "不存在的商品不应有结果"


@allure.feature("商品模块")
@allue.story("分类浏览")
class TestCategory:
    """分类接口测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, request_util):
        self.product_api = ProductAPI(request_util)
    
    @allue.title("获取一级分类列表")
    @allue.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_category_list(self):
        with allure.step("获取一级分类"):
            result = self.product_api.get_category_list(parent_id=0)
        
        AssertUtil().assert_response_code(result)
        
        categories = result.get("data", [])
        with allure.step(f"分类数量 >= 5"):
            assert len(categories) >= 5, f"一级分类数量过少: {len(categories)}"
    
    @allue.title("获取子分类")
    @allue.severity(allure.severity_level.NORMAL)
    def test_get_sub_category(self):
        with allure.step("获取数码类子分类"):
            result = self.product_api.get_category_list(parent_id=1)
        
        AssertUtil().assert_response_code(result)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
