"""订单模块 API 封装"""
from API_Automation.api.base_api import BaseAPI


class OrderAPI(BaseAPI):
    """订单相关接口"""
    
    # ===== 创建订单 =====
    
    def create_order(
        self,
        address_id: int,
        items: list[dict],  # [{cart_item_id, spec_id, quantity}]
        coupon_id: int = None,
        remark: str = "",
        token: str = None
    ) -> dict:
        """
        创建订单（从购物车下单）
        
        items 格式示例:
        [
            {"cart_item_id": 123, "spec_id": 456, "quantity": 2},
        ]
        """
        data = {
            "address_id": address_id,
            "items": items,
            "remark": remark
        }
        if coupon_id:
            data["coupon_id"] = coupon_id
        
        return self.post("/order/create", token=token, json=data)
    
    # ===== 订单查询 =====
    
    def get_order_detail(
        self, 
        order_no: str, 
        token: str
    ) -> dict:
        """获取订单详情"""
        return self.get(f"/order/{order_no}/detail", token=token)
    
    def get_order_list(
        self,
        status: str = "all",  # all/pending/paid/shipping/completed/cancelled
        page: int = 1,
        page_size: int = 20,
        token: str = None
    ) -> dict:
        """获取订单列表"""
        return self.get(
            "/order/list",
            token=token,
            params={
                "status": status,
                "page": page,
                "page_size": page_size
            }
        )
    
    def get_order_count(self, status: str = "all", token: str = None) -> dict:
        """获取各状态订单数量统计"""
        return self.get("/order/count", token=token, params={"status": status})
    
    # ===== 订单操作 =====
    
    def cancel_order(
        self, 
        order_no: str, 
        reason: str = "",
        token: str
    ) -> dict:
        """取消订单"""
        return self.post(
            f"/order/{order_no}/cancel",
            token=token,
            json={"reason": reason}
        )
    
    def confirm_receive(
        self, 
        order_no: str, 
        token: str
    ) -> dict:
        """确认收货"""
        return self.post(f"/order/{order_no}/confirm", token=token)
    
    # ===== 支付 =====
    
    def get_pay_params(
        self, 
        order_no: str, 
        pay_method: str = "wechat",  # wechat/alipay
        token: str
    ) -> dict:
        """获取支付参数"""
        return self.post(
            f"/order/{order_no}/pay/params",
            token=token,
            json={"pay_method": pay_method}
        )
    
    def pay_callback(
        self, 
        order_no: str, 
        pay_result: dict,
        token: str
    ) -> dict:
        """支付结果回调通知"""
        return self.post(
            f"/order/{order_no}/pay/callback",
            token=token,
            json=pay_result
        )
    
    # ===== 售后 =====
    
    def apply_refund(
        self,
        order_no: str,
        reason: str,
        refund_type: str = "full",  # full/partial
        refund_amount: float = None,
        images: list[str] = None,
        token: str = None
    ) -> dict:
        """申请退款"""
        data = {
            "order_no": order_no,
            "reason": reason,
            "refund_type": refund_type
        }
        if refund_amount:
            data["refund_amount"] = refund_amount
        if images:
            data["images"] = images
        
        return self.post("/order/refund/apply", token=token, json=data)
    
    def get_refund_list(
        self, 
        page: int = 1, 
        token: str = None
    ) -> dict:
        """获取退款记录列表"""
        return self.get(
            "/order/refund/list",
            token=token,
            params={"page": page}
        )
