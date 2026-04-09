"""
Locust 性能测试脚本 - 云鹿商城 API 压力测试

使用方法:
    cd Performance/locust_scripts
    locust -f locustfile.py --host=https://api-dev.yunlu.com
    然后访问 http://localhost:8089 查看 Web UI
"""
import random
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner

# ===================== 自定义事件 =====================

# 记录请求耗时分布
request_stats = events.RequestStats()

# ===================== 用户场景定义 =====================

class NormalUser(HttpUser):
    """
    正常用户行为模型
    
    场景：
    - 浏览首页
    - 搜索商品
    - 查看商品详情
    - 加入购物车
    - 下单（到支付前停止）
    """
    
    # 用户思考时间：请求间隔 1-5 秒，模拟真实用户操作节奏
    wait_time = between(1, 5)
    
    def on_start(self):
        """每个用户开始时的操作"""
        self.client.post("/user/login", json={
            "phone": f"13800138{random.randint(0,99):02}",
            "code": "123456"
        })
    
    @task(10)  # 权重为10（最常执行）
    def browse_homepage(self):
        """浏览首页"""
        self.client.get("/product/home/banner", name="首页Banner")
        self.client.get("/product/hot", params={"page": 1}, name="热门商品")
    
    @task(7)   # 权重为7
    def search_product(self):
        """搜索商品"""
        keywords = ["手机", "耳机", "数码", "Apple", "充电宝"]
        keyword = random.choice(keywords)
        self.client.get("/product/search", 
                        params={"keyword": keyword},
                        name=f"搜索/{keyword}")
    
    @task(5)   # 权重为5
    def view_product_detail(self):
        """查看商品详情"""
        product_ids = range(10000, 10100)
        pid = random.choice(product_ids)
        self.client.get(f"/product/{pid}/detail", name=f"商品详情/{pid}")
        self.client.get(f"/product/{pid}/specs", name=f"商品规格/{pid}")
        self.client.get(f"/product/{pid}/comments", name=f"商品评论/{pid}")
    
    @task(4)   # 权重为4
    def add_to_cart(self):
        """加入购物车"""
        pid = random.randint(10000, 10050)
        spec_id = random.randint(20000, 20100)
        self.client.post("/cart/add", json={
            "product_id": pid,
            "spec_id": spec_id,
            "quantity": random.randint(1, 3)
        }, name="加购")
    
    @task(2)   # 权重为2（下单频率较低）
    def view_cart(self):
        """查看购物车"""
        self.client.get("/cart/list", name="购物车列表")
        self.client.get("/cart/summary", name="购物车汇总")
    
    @task(1)   # 权重为1（最低频）
    def get_user_profile(self):
        """获取个人信息"""
        self.client.get("/user/info", name="用户信息")
        self.client.get("/user/address/list", name="地址列表")


class HeavyUser(NormalUser):
    """
    重度用户 - 更频繁的操作
    用于高并发压力测试
    """
    wait_time = between(0.5, 2)
    
    @task(15)
    def rapid_search(self):
        """高频搜索"""
        keywords = ["手机", "AirPods", "iPad", "MacBook", "手表"]
        self.client.get("/product/search", 
                        params={"keyword": random.choice(keywords)},
                        name="快速搜索")


class CheckoutUser(HttpUser):
    """
    下单用户 - 模拟完整购买流程
    """
    wait_time = between(2, 6)
    
    @task
    def full_checkout_flow(self):
        """完整下单流程（到支付）"""
        # 1. 搜索商品
        self.client.get("/product/search", params={"keyword": "手机"}, name="搜索手机")
        
        # 2. 查看详情
        pid = random.randint(10000, 10020)
        self.client.get(f"/product/{pid}/detail", name=f"商品详情/{pid}")
        
        # 3. 加购
        spec_id = random.randint(20000, 20050)
        self.client.post("/cart/add", json={
            "product_id": pid,
            "spec_id": spec_id,
            "quantity": 1
        }, name="加购")
        
        # 4. 购物车
        self.client.get("/cart/list", name="购物车")
        
        # 5. 创建订单
        self.client.post("/order/create", json={
            "address_id": 80001,
            "items": [{"cart_item_id": 50001, "spec_id": 20001, "quantity": 1}],
            "remark": "性能测试订单"
        }, name="创建订单")


# ===================== 测试配置 =====================

if __name__ == "__main__":
    # 命令行直接运行模式
    import sys
    
    print("=" * 60)
    print("云鹿商城 API 性能测试")
    print("=" * 60)
    print("\n使用方式:")
    print("  1. 启动 Locust Web UI: locust -f locustfile.py --host=<API地址>")
    print("  2. 无头模式运行:     locust -f locustfile.py --host=<API地址> --headless -u 10 -t 60")
    print("  3. 分布式运行:       locust -f locustfile.py --master --worker")
    print("\n默认 Host: https://api-dev.yunlu.com")
    print("Web UI 地址: http://localhost:8089\n")
