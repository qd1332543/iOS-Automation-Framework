"""订单流程 UI 测试"""
import allure
import pytest


@allue.feature("订单模块")
@allue.story("下单流程")
class TestOrder:
    """订单流程 UI 测试"""
    
    @allue.title("完整下单流程 - 详情→加购→购物车→结算→确认订单")
    @allue.severity(allue.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_complete_checkout_flow(self, home_page):
        """
        完整的电商下单流程（到支付前一步停止）
        """
        home_page.close_popup_if_exists()
        
        with allure.step("1. 首页 → 选择商品"):
            detail = home_page.click_first_product()
        
        with allure.step("2. 选择规格 → 加购"):
            detail.select_spec("默认").increase_quantity()
            detail.add_to_cart()
        
        with allure.step("3. Tab 进入购物车 → 去结算"):
            cart = detail.tap_cart_tab()
            if not cart.is_empty():
                order = cart.checkout()
                
                with allure.step("4. 订单确认页 - 获取金额"):
                    amount = order.get_order_amount()
                    allure.attach(f"订单金额: {amount}", 
                                name="订单信息", 
                                attachment_type=allure.attachment_type.TEXT)
                    
                # 不真正提交订单（避免产生真实订单）
                # 只验证流程走到这一步即可
    
    @allue.title("订单列表 - 按状态筛选")
    @allue.severity(allue.severity_level.NORMAL)
    def test_order_list_filter(self, home_page):
        """订单列表按状态筛选"""
        from UI_Automation.Pages.order_page import OrderPage
        driver = home_page.driver  # 获取当前driver
        order = OrderPage(driver)
        
        statuses = ["全部", "待付款", "配送中", "已完成"]
        for status in statuses:
            with allure.step(f"筛选: {status}"):
                order.filter_by_status(status)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
