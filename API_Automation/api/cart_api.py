"""购物车模块 API 封装"""
from API_Automation.api.base_api import BaseAPI


class CartAPI(BaseAPI):
    """购物车相关接口"""
    
    def add_to_cart(
        self,
        product_id: int,
        spec_id: int,
        quantity: int = 1,
        token: str = None
    ) -> dict:
        """添加商品到购物车"""
        return self.post(
            "/cart/add",
            token=token,
            json={
                "product_id": product_id,
                "spec_id": spec_id,
                "quantity": quantity
            }
        )
    
    def update_quantity(
        self,
        cart_item_id: int,
        quantity: int,
        token: str
    ) -> dict:
        """修改购物车商品数量"""
        return self.put(
            f"/cart/item/{cart_item_id}",
            token=token,
            json={"quantity": quantity}
        )
    
    def remove_item(
        self, 
        cart_item_id: int, 
        token: str
    ) -> dict:
        """移除购物车中的商品"""
        return self.delete(f"/cart/item/{cart_item_id}", token=token)
    
    def clear_cart(self, token: str) -> dict:
        """清空购物车"""
        return self.post("/cart/clear", token=token)
    
    def get_cart_list(self, token: str) -> dict:
        """获取购物车列表（含商品详情、价格汇总）"""
        return self.get("/cart/list", token=token)
    
    def select_items(
        self, 
        item_ids: list[int], 
        token: str
    ) -> dict:
        """勾选购物车项（用于结算）"""
        return self.post(
            "/cart/select",
            token=token,
            json={"item_ids": item_ids}
        )
    
    def select_all(self, token: str) -> dict:
        """全选购物车"""
        return self.post("/cart/select/all", token=token)
    
    def get_cart_summary(self, token: str) -> dict:
        """获取购物车汇总信息（数量、总价等）"""
        return self.get("/cart/summary", token=token)
    
    # 购物车数量角标
    def get_cart_count(self, token: str) -> dict:
        """获取购物车商品总数"""
        return self.get("/cart/count", token=token)
