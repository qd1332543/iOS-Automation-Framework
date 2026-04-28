"""购物车接口测试"""
import allure
import pytest
from API_Automation.api.cart_api import CartAPI
from API_Automation.api.product_api import ProductAPI
from utils.assertion_util import AssertUtil


@allure.feature("购物车模块")
@allure.story("购物车操作")
class TestCart:
    """购物车接口测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, request_util, login_token):
        self.cart_api = CartAPI(request_util)
        self.product_api = ProductAPI(request_util)
        self.token = login_token
    
    @allure.title("添加商品到购物车-正常流程")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_add_to_cart(self):
        with allure.step("添加商品到购物车"):
            result = self.cart_api.add_to_cart(
                product_id=10001,
                spec_id=20001,
                quantity=1,
                token=self.token
            )
        
        AssertUtil().assert_response_code(result)
        
        with allure.step("验证购物车列表"):
            cart = self.cart_api.get_cart_list(self.token)
            AssertUtil().assert_response_code(cart)
            items = cart.get("data", {}).get("items", [])
            assert len(items) > 0, "购物车不应为空"
    
    @allure.title("获取购物车汇总信息")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_summary(self):
        # 先确保有商品
        self.cart_api.add_to_cart(product_id=10001, spec_id=20001, token=self.token)
        
        with allure.step("获取汇总"):
            result = self.cart_api.get_cart_summary(self.token)
            AssertUtil().assert_response_code(result)
            
            summary = result.get("data", {})
            with allure.step("校验汇总字段"):
                assert "total_price" in summary or "total_amount" in summary
                assert "item_count" in summary or "quantity" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
