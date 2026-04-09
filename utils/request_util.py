"""
HTTP 请求封装工具

基于 requests.Session 实现：
- 统一的请求/响应日志
- 自动错误处理
- 重试机制
- 超时控制
- 响应断言辅助
"""
import time
import json
from typing import Any, Dict, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils.log_util import get_logger

logger = get_logger("RequestUtil")


class RequestUtil:
    """
    HTTP 请求工具类
    
    特性：
    - Session 复用（连接池）
    - 自动重试机制
    - 请求/响应完整日志
    - JSON 自动解析
    - 统一异常处理
    """
    
    def __init__(
        self,
        base_url: str = "",
        timeout: int = 30,
        max_retries: int = 3,
        headers: Optional[Dict] = None
    ):
        """
        初始化请求工具
        
        Args:
            base_url: API 基础地址
            timeout: 请求超时时间(秒)
            max_retries: 最大重试次数
            headers: 默认请求头
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        
        # 创建 Session（连接池复用）
        self.session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=100
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 设置默认请求头
        default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "YunluTestFramework/1.0"
        }
        if headers:
            default_headers.update(headers)
        self.session.headers.update(default_headers)
        
        logger.info(f"RequestUtil 初始化: base_url={base_url}, timeout={timeout}s")
    
    def request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """
        发送 HTTP 请求（核心方法）
        
        Args:
            method: HTTP 方法 (GET/POST/PUT/DELETE/PATCH)
            endpoint: API 端点 (如 /user/login)
            **kwargs: requests.request 的其他参数
            
        Returns:
            Response 对象
        """
        url = f"{self.base_url}{endpoint}" if endpoint.startswith("/") \
            else f"{self.base_url}/{endpoint}"
        
        # 设置默认超时
        kwargs.setdefault("timeout", self.timeout)
        
        # 记录请求数据
        request_data = {
            "method": method.upper(),
            "url": url,
            "headers": kwargs.get("headers", {}),
        }
        if "json" in kwargs:
            request_data["body"] = kwargs["json"]
        elif "params" in kwargs:
            request_data["params"] = kwargs["params"]
        
        logger.debug(f"📤 请求发送: {method.upper()} {url}")
        if "json" in kwargs:
            logger.debug(f"   Body: {json.dumps(kwargs['json'], ensure_ascii=False)}")
        
        start_time = time.time()
        
        try:
            response = self.session.request(method.upper(), url, **kwargs)
            
            # 计算耗时
            elapsed = time.time() - start_time
            
            # 日志记录
            logger.info(
                f"📥 响应接收: {method.upper()} {url} | "
                f"状态码={response.status_code} | 耗时={elapsed:.3f}s"
            )
            
            # 尝试记录响应体（截断过长内容）
            try:
                resp_json = response.json()
                resp_str = json.dumps(resp_json, ensure_ascii=False)
                if len(resp_str) > 500:
                    logger.debug(f"   Response: {resp_str[:500]}... (truncated)")
                else:
                    logger.debug(f"   Response: {resp_str}")
            except Exception:
                text_preview = response.text[:200] if response.text else "(empty)"
                logger.debug(f"   Response(text): {text_preview}")
            
            return response
            
        except requests.exceptions.Timeout:
            logger.error(f"❌ 请求超时: {method.upper()} {url} (>{self.timeout}s)")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"❌ 连接失败: {method.upper()} {url} | {e}")
            raise
        except Exception as e:
            logger.error(f"❌ 请求异常: {method.upper()} {url} | {type(e).__name__}: {e}")
            raise
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """GET 请求"""
        return self.request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """POST 请求"""
        return self.request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """PUT 请求"""
        return self.request("PUT", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE 请求"""
        return self.request("DELETE", endpoint, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """PATCH 请求"""
        return self.request("PATCH", endpoint, **kwargs)
    
    # ==================== 辅助方法 ====================
    
    def assert_response(
        self,
        response: requests.Response,
        expected_status: int = 200,
        expected_code: int = 0
    ) -> Dict:
        """
        断言响应结果
        
        Args:
            response: Response 对象
            expected_status: 预期 HTTP 状态码
            expected_code: 预期业务状态码
            
        Returns:
            响应的 JSON 数据
        """
        # 断言 HTTP 状态码
        assert response.status_code == expected_status, \
            f"HTTP 状态码不匹配: 预期 {expected_status}, 实际 {response.status_code}"
        
        result = response.json()
        
        # 断言业务状态码
        actual_code = result.get("code")
        assert actual_code == expected_code, \
            f"业务状态码不匹配: 预期 {expected_code}, 实际 {actual_code}, msg={result.get('msg')}"
        
        return result
    
    def close(self):
        """关闭 Session 连接池"""
        self.session.close()
        logger.info("RequestUtil 连接已关闭")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
