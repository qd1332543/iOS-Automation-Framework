"""商品模块 API 封装"""
from API_Automation.api.base_api import BaseAPI


class ProductAPI(BaseAPI):
    """商品相关接口"""
    
    # ===== 商品列表与搜索 =====
    
    def get_home_banner(self, token=None) -> dict:
        """获取首页 Banner 数据"""
        return self.get("/product/home/banner", token=token)
    
    def get_hot_products(
        self, 
        page: int = 1, 
        page_size: int = 20,
        token=None
    ) -> dict:
        """获取热门商品列表"""
        return self.get(
            "/product/hot",
            token=token,
            params={"page": page, "page_size": page_size}
        )
    
    def search_products(
        self,
        keyword: str,
        category_id: int = None,
        sort: str = "default",  # default/price_asc/price_desc/sales
        page: int = 1,
        page_size: int = 20,
        token=None
    ) -> dict:
        """搜索商品"""
        params = {
            "keyword": keyword,
            "sort": sort,
            "page": page,
            "page_size": page_size
        }
        if category_id:
            params["category_id"] = category_id
        
        return self.get(
            "/product/search",
            token=token,
            params=params
        )
    
    # ===== 分类 =====
    
    def get_category_list(self, parent_id: int = 0, token=None) -> dict:
        """获取分类列表"""
        return self.get(
            "/product/category/list",
            token=token,
            params={"parent_id": parent_id}
        )
    
    def get_category_products(
        self,
        category_id: int,
        page: int = 1,
        page_size: int = 20,
        sort: str = "default",
        token=None
    ) -> dict:
        """获取分类下商品列表"""
        return self.get(
            f"/product/category/{category_id}/products",
            token=token,
            params={"page": page, "page_size": page_size, "sort": sort}
        )
    
    # ===== 商品详情 =====
    
    def get_product_detail(
        self, 
        product_id: int, 
        token=None
    ) -> dict:
        """获取商品详情"""
        return self.get(f"/product/{product_id}/detail", token=token)
    
    def get_product_specs(
        self, 
        product_id: int, 
        token=None
    ) -> dict:
        """获取商品规格选项"""
        return self.get(f"/product/{product_id}/specs", token=token)
    
    def get_product_comments(
        self,
        product_id: int,
        page: int = 1,
        page_size: int = 20,
        token=None
    ) -> dict:
        """获取商品评论"""
        return self.get(
            f"/product/{product_id}/comments",
            token=token,
            params={"page": page, "page_size": page_size}
        )
    
    # ===== 收藏 =====
    
    def collect_product(
        self, 
        product_id: int, 
        token: str
    ) -> dict:
        """收藏商品"""
        return self.post(
            "/user/collect/add",
            token=token,
            json={"product_id": product_id}
        )
    
    def uncollect_product(
        self, 
        product_id: int, 
        token: str
    ) -> dict:
        """取消收藏"""
        return self.post(
            "/user/collect/remove",
            token=token,
            json={"product_id": product_id}
        )
    
    def get_collect_list(
        self, 
        page: int = 1, 
        token: str = None
    ) -> dict:
        """获取收藏列表"""
        return self.get(
            "/user/collect/list",
            token=token,
            params={"page": page}
        )
