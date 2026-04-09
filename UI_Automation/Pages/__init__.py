# Pages 包初始化 - 导出所有页面对象
from UI_Automation.Pages.base_page import BasePage
from UI_Automation.Pages.login_page import LoginPage
from UI_Automation.Pages.home_page import HomePage
from UI_Automation.Pages.category_page import CategoryPage
from UI_Automation.Pages.product_detail_page import ProductDetailPage
from UI_Automation.Pages.cart_page import CartPage
from UI_Automation.Pages.order_page import OrderPage

__all__ = [
    "BasePage",
    "LoginPage", 
    "HomePage",
    "CategoryPage",
    "ProductDetailPage",
    "CartPage",
    "OrderPage",
]
