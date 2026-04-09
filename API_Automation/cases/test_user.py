"""
用户模块接口测试用例

覆盖场景：
- 登录（验证码登录 / 密码登录）
- 注册
- 发送验证码
- 获取/修改用户信息
- 地址管理 CRUD
"""
import allure
import pytest

import yaml
from API_Automation.api.user_api import UserAPI
from utils.assertion_util import AssertUtil


@allure.feature("用户模块")
@allure.story("登录注册")
class TestUserLogin:
    """用户登录注册接口测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, request_util):
        """每个测试方法前创建 API 实例"""
        self.user_api = UserAPI(request_util)
        self.assertion = AssertUtil()
    
    @allure.title("验证码登录 - 正常账号")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_by_code_success(self, user_test_data):
        """使用正确手机号和验证码登录成功"""
        cases = user_test_data["login_cases"]
        case = next(c for c in cases if "正确手机号" in c["name"])
        
        with allure.step(f"调用登录接口: 手机号 {case['phone'][:3]}****{case['phone'][-4:]}"):
            result = self.user_api.login_by_phone(
                phone=case["phone"],
                code=case["code"]
            )
        
        with allure.step("校验响应码为 0"):
            self.assertion.assert_response_code(result)
        
        with allure.step("校验返回 token"):
            assert result.get("data", {}).get("token"), "未返回 Token"
            
            allure.attach(
                f"Token: {result['data']['token'][:20]}...",
                name="Token信息",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @allure.title("密码登录 - 正确账号")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_by_password_success(self, user_test_data):
        cases = user_test_data["login_cases"]
        case = next(c for c in cases if "密码" in c.get("login_type", ""))
        
        with allure.step("密码登录"):
            result = self.user_api.login_by_password(
                phone=case["phone"],
                password=case["password"]
            )
        
        self.assertion.assert_response_code(result)
        assert result.get("data", {}).get("token")
    
    @allure.title("手机号为空 - 参数校验")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_empty_phone(self, user_test_data):
        cases = user_test_data["login_cases"]
        case = next(c for c in cases if "手机号为空" in c["name"])
        
        with allure.step("手机号为空登录"):
            result = self.user_api.login_by_phone(
                phone=case["phone"],
                code=case["code"]
            )
        
        assert result["code"] == case["expected_code"]
    
    @allure.title("验证码错误 - 业务校验")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_wrong_code(self, user_test_data):
        cases = user_test_data["login_cases"]
        case = next(c for c in cases if "验证码错误" in c["name"])
        
        with allure.step("输入错误验证码"):
            result = self.user_api.login_by_phone(
                phone=case["phone"],
                code=case["code"]
            )
        
        assert result["code"] == case["expected_code"]
    
    @allure.title("手机号格式异常 - 多种边界值")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize(
        "phone, expected_code",
        [
            ("1380013", 1001),           # 不足11位
            ("abcdefghijk", 1001),      # 非数字
            ("138-0013-8000", 1001),   # 含特殊字符
            ("138001380001", 1001),     # 超过11位
            ("0", 1001),               # 单个数字
        ],
        ids=["不足11位", "非数字", "含特殊字符", "超过11位", "单个数字"]
    )
    def test_login_invalid_phone_format(
        self, 
        phone: str, 
        expected_code: int,
        user_test_data
    ):
        """参数化测试：各种非法手机号格式"""
        with allure.step(f"测试手机号格式: {phone}"):
            result = self.user_api.login_by_phone(phone=phone, code="123456")
            assert result["code"] == expected_code


@allure.feature("用户模块")
@allue.story("用户信息")
class TestUserInfo:
    """用户信息接口测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, request_util, login_token):
        self.user_api = UserAPI(request_util)
        self.token = login_token
    
    @allue.title("获取当前用户信息")
    @allue.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_user_info(self):
        with allure.step("获取用户详情"):
            result = self.user_api.get_user_info(self.token)
        
        AssertUtil().assert_response_code(result)
        
        user_data = result.get("data", {})
        with allure.step("校验关键字段存在"):
            assert "user_id" in user_data or "id" in user_data
            assert "nickname" in user_data or "phone" in user_data
            
            allure.attach(
                str(user_data),
                name="用户信息",
                attachment_type=allure.attachment_type.JSON
            )
    
    @allue.title("修改昵称")
    @allue.severity(allure.severity_level.NORMAL)
    def test_update_nickname(self):
        new_name = f"AutoTest_{__import__('time').strftime('%H%M%S')}"
        
        with allure.step(f"修改昵称为: {new_name}"):
            result = self.user_api.update_profile(nickname=new_name, token=self.token)
        
        AssertUtil().assert_response_code(result)
        
        # 验证修改生效
        with allure.step("重新获取信息确认修改"):
            info = self.user_api.get_user_info(self.token)
            data = info.get("data", {})
            actual_name = data.get("nickname", "")
            assert new_name == actual_name, f"昵称未更新成功: 预期 {new_name}, 实际 {actual_name}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
