"""用户模块 API 封装"""
from API_Automation.api.base_api import BaseAPI


class UserAPI(BaseAPI):
    """用户相关接口"""
    
    # ===== 登录注册 =====
    
    def login_by_phone(
        self, 
        phone: str, 
        code: str, 
        token=None
    ) -> dict:
        """手机号 + 验证码登录"""
        return self.post(
            "/user/login",
            token=token,
            json={
                "phone": phone,
                "code": code,
                "login_type": "sms_code"
            }
        )
    
    def login_by_password(
        self, 
        phone: str, 
        password: str, 
        token=None
    ) -> dict:
        """密码登录"""
        return self.post(
            "/user/login/password",
            token=token,
            json={
                "phone": phone,
                "password": password
            }
        )
    
    def send_verification_code(self, phone: str, token=None) -> dict:
        """发送验证码"""
        return self.post(
            "/user/sms/code/send",
            token=token,
            json={"phone": phone, "scene": "login"}
        )
    
    def register(
        self, 
        phone: str, 
        code: str, 
        password: str,
        invite_code: str = "",
        token=None
    ) -> dict:
        """用户注册"""
        return self.post(
            "/user/register",
            token=token,
            json={
                "phone": phone,
                "code": code,
                "password": password,
                "invite_code": invite_code
            }
        )
    
    def logout(self, token: str) -> dict:
        """退出登录"""
        return self.post("/user/logout", token=token)
    
    # ===== 用户信息 =====
    
    def get_user_info(self, token: str) -> dict:
        """获取当前用户信息"""
        return self.get("/user/info", token=token)
    
    def update_profile(
        self, 
        nickname: str = "", 
        avatar: str = "",
        gender: int = 0,
        token: str = None
    ) -> dict:
        """更新个人资料"""
        data = {}
        if nickname:
            data["nickname"] = nickname
        if avatar:
            data["avatar"] = avatar
        if gender is not None:
            data["gender"] = gender
        
        return self.put("/user/profile", token=token, json=data)
    
    # ===== 地址管理 =====
    
    def add_address(
        self,
        name: str,
        phone: str,
        province: str,
        city: str,
        district: str,
        detail: str,
        is_default: bool = False,
        token: str = None
    ) -> dict:
        """添加收货地址"""
        return self.post(
            "/user/address/add",
            token=token,
            json={
                "receiver_name": name,
                "receiver_phone": phone,
                "province": province,
                "city": city,
                "district": district,
                "detail_address": detail,
                "is_default": is_default
            }
        )
    
    def get_address_list(self, token: str) -> dict:
        """获取地址列表"""
        return self.get("/user/address/list", token=token)
    
    def delete_address(
        self, 
        address_id: int, 
        token: str
    ) -> dict:
        """删除地址"""
        return self.delete(
            f"/user/address/{address_id}",
            token=token
        )
