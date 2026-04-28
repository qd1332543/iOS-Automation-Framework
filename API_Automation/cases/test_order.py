"""订单模块接口测试"""
import allure
import pytest
from API_Automation.api.order_api import OrderAPI
from utils.assertion_util import AssertUtil


@allure.feature("订单模块")
@allure.story("订单管理")
class TestOrder:
    """订单接口测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, request_util, login_token):
        self.order_api = OrderAPI(request_util)
        self.token = login_token
    
    @allure.title("获取订单列表")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_order_list(self):
        with allure.step("获取全部订单"):
            result = self.order_api.get_order_list(token=self.token)
        
        AssertUtil().assert_response_code(result)
        orders = result.get("data", {}).get("orders", [])
        
        allure.attach(
            f"订单数量: {len(orders)}",
            name="结果摘要",
            attachment_type=allure.attachment_type.TEXT
        )
    
    @allure.title("按状态筛选订单")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("status", ["pending", "shipping", "completed", "cancelled"])
    def test_filter_order_by_status(self, status):
        with allure.step(f"筛选状态: {status}"):
            result = self.order_api.get_order_list(status=status, token=self.token)
        
        AssertUtil().assert_response_code(result)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
