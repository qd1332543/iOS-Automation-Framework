"""
Base API - 接口自动化基础类

封装通用的 HTTP 请求方法：
- 统一错误处理
- 自动 Token 管理
- 请求日志
- 响应断言
"""
from typing import Any, Dict, Optional

from utils.request_util import RequestUtil
from utils.assertion_util import AssertUtil
from utils.log_util import get_logger

logger = get_logger("BaseAPI")


class BaseAPI:
    """
    API 基础类
    
    所有模块 API 的父类，提供：
    - 统一的 HTTP 方法封装
    - Token 注入
    - 标准化响应处理
    """
    
    def __init__(self, request_util: RequestUtil):
        self.request = request_util
        self.assertion = AssertUtil()
        self.module_name = self.__class__.__name__
        logger.info(f"🔌 API 模块初始化: {self.module_name}")
    
    def _get_headers(
        self, 
        token: str = None,
        extra_headers: Dict = None
    ) -> Dict[str, str]:
        """构建请求头"""
        headers = {"Content-Type": "application/json"}
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        if extra_headers:
            headers.update(extra_headers)
        
        return headers
    
    def get(self, endpoint: str, token=None, **kwargs) -> Dict:
        """GET 请求"""
        kwargs.setdefault("headers", self._get_headers(token))
        logger.debug(f"[{self.module_name}] GET {endpoint}")
        response = self.request.get(endpoint, **kwargs)
        return response.json()
    
    def post(self, endpoint: str, token=None, **kwargs) -> Dict:
        """POST 请求"""
        kwargs.setdefault("headers", self._get_headers(token))
        logger.debug(f"[{self.module_name}] POST {endpoint}")
        if "json" in kwargs:
            logger.debug(f"   Body: {kwargs['json']}")
        response = self.request.post(endpoint, **kwargs)
        return response.json()
    
    def put(self, endpoint: str, token=None, **kwargs) -> Dict:
        """PUT 请求"""
        kwargs.setdefault("headers", self._get_headers(token))
        response = self.request.put(endpoint, **kwargs)
        return response.json()
    
    def delete(self, endpoint: str, token=None, **kwargs) -> Dict:
        """DELETE 请求"""
        kwargs.setdefault("headers", self._get_headers(token))
        response = self.request.delete(endpoint, **kwargs)
        return response.json()
    
    def assert_success(self, response_data: Dict, msg=""):
        """断言接口返回成功（业务码为0）"""
        self.assertion.assert_response_code(response_data)
