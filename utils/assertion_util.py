"""
断言封装工具 - 提供统一的断言方法
支持 Allure 附加、自定义错误消息
"""
import json
import allure


class AssertUtil:
    """
    断言工具类
    
    功能：
    - 统一的断言风格
    - 自动附加到 Allure 报告
    - 详细的失败信息
    - 支持多种数据类型断言
    """
    
    @staticmethod
    def assert_equals(actual, expected, message: str = ""):
        """值相等断言"""
        with allure.step(f"断言相等: {message}"):
            allure.attach(
                f"预期: {expected}\n实际: {actual}",
                name="断言详情",
                attachment_type=allure.attachment_type.TEXT
            )
            assert actual == expected, \
                f"断言失败 [{message}]: 预期 '{expected}', 实际 '{actual}'"
    
    @staticmethod
    def assert_not_equals(actual, not_expected, message: str = ""):
        """值不相等断言"""
        with allure.step(f"断言不相等: {message}"):
            assert actual != not_expected, \
                f"断言失败 [{message}]: 不应等于 '{not_expected}'"
    
    @staticmethod
    def assert_contains(text: str, substring: str, message: str = ""):
        """包含字符串断言"""
        with allure.step(f"断言包含: {message}"):
            assert substring in text, \
                f"断言失败 [{message}]: '{text}' 不包含 '{substring}'"
    
    @staticmethod
    def assert_true(condition: bool, message: str = "条件应为 True"):
        """True 断言"""
        with allure.step(f"断言为真: {message}"):
            assert condition, f"断言失败: {message}"
    
    @staticmethod
    def assert_false(condition: bool, message: str = "条件应为 False"):
        """False 断言"""
        with allure.step(f"断言为假: {message}"):
            assert not condition, f"断言失败: {message}"
    
    @staticmethod
    def assert_none(value, message: str = "应为 None"):
        """None 断言"""
        with allure.step(f"断言为空: {message}"):
            assert value is None, f"断言失败 [{message}]: 预期 None, 实际 {value}"
    
    @staticmethod
    def assert_not_none(value, message: str = "不应为 None"):
        """非 None 断言"""
        with allure.step(f"断言非空: {message}"):
            assert value is not None, f"断言失败 [{message}]: 值不应为空"
    
    @staticmethod
    def assert_greater(actual, threshold, message: str = ""):
        """大于断言"""
        with allure.step(f"断言大于: {message}"):
            assert actual > threshold, \
                f"断言失败 [{message}]: {actual} 应大于 {threshold}"
    
    @staticmethod
    def assert_greater_equal(actual, threshold, message: str = ""):
        """大于等于断言"""
        with allure.step(f"断言大于等于: {message}"):
            assert actual >= threshold, \
                f"断言失败 [{message}]: {actual} 应 >= {threshold}"
    
    @staticmethod
    def assert_list_length(lst: list, expected_len: int, message: str = ""):
        """列表长度断言"""
        with allure.step(f"断言列表长度: {message}"):
            actual_len = len(lst)
            assert actual_len == expected_len, \
                f"断言失败 [{message}]: 列表长度预期 {expected_len}, 实际 {actual_len}"
    
    @staticmethod
    def assert_dict_contains_key(dct: dict, key: str, message: str = ""):
        """字典包含键断言"""
        with allure.step(f"断言字典包含键: {key}"):
            assert key in dct, \
                f"断言失败 [{message}]: 字典不包含键 '{key}', 现有键: {list(dct.keys())}"
    
    @staticmethod
    def assert_response_code(response_data: dict, expected_code: int = 0):
        """
        业务响应码断言（通用）
        
        Args:
            response_data: API 返回的 JSON 数据
            expected_code: 预期的业务状态码，默认 0 表示成功
        """
        with allure.step("校验业务响应码"):
            actual_code = response_data.get("code")
            msg = response_data.get("msg", "")
            
            allure.attach(
                json.dumps(response_data, ensure_ascii=False, indent=2),
                name="响应体",
                attachment_type=allure.attachment_type.JSON
            )
            
            assert actual_code == expected_code, \
                f"业务码不匹配: 预期 {expected_code}, 实际 {actual_code}, 消息: {msg}"