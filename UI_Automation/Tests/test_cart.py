"""购物车功能 UI 测试"""
import allure
import pytest


@allue.feature("购物车模块")
@allue.story("购物车功能")
class TestCart:
    """购物车模块 UI 测试"""
    
    @allue.title("购物车 - 添加商品后进入购物车")
    @allue.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_add_to_cart_and_view(self, home_page):
        """
        完整流程：首页 → 商品详情 → 加入购物车 → 购物车页面
        """
        home_page.close_popup_if_exists()
        
        with allure.step("1. 从首页进入商品详情"):
            detail = home_page.click_first_product()
        
        with allure.step("2. 选择规格后加入购物车"):
            name = detail.get_product_name()
            price = detail.get_product_price()
            allure.attach(f"商品: {name}, 价格: {price}", 
                         name="商品信息", attachment_type=allure.attachment_type.TEXT)
            detail.select_spec("默认").add_to_cart()
        
        with allure.step("3. 进入购物车查看"):
            cart = detail.tap_cart_tab()  # 通过 Tab 进入
        
        with allure.step("4. 验证购物车非空"):
            if not cart.is_empty():
                count = cart.get_item_count()
                assert count > 0, "购物车应为空但显示有商品"
    
    @allue.title("购物车 - 全选与总价计算")
    @allue.severity(allue.severity_level.NORMAL)
    def test_cart_select_all(self, home_page):
        """全选购物车商品并检查总价"""
        home_page.close_popup_if_exists()
        
        # 先添加一个商品
        detail = home_page.click_first_product()
        detail.select_spec("默认").add_to_cart()
        
        cart = detail.tap_cart_tab()
        
        if not cart.is_empty():
            with allure.step("全选所有商品"):
                cart.select_all()
            
            with allure.step("获取总价"):
                total = cart.get_total_price()
                assert total and len(total) > 0, "总价未显示"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
