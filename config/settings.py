"""
全局配置管理模块
支持多环境切换、环境变量覆盖
"""
import os
import yaml
from typing import Any, Dict, Optional


class Settings:
    """
    全局配置管理器（单例模式）
    支持从 YAML 文件和环境变量加载配置
    """
    
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._config:
            self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "config", "environments.yaml"
        )
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        with open(config_path, "r", encoding="utf-8") as f:
            all_configs = yaml.safe_load(f)
        
        # 通过环境变量选择当前环境，默认 dev
        env_name = os.getenv("TEST_ENV", "dev")
        self._config = all_configs.get(env_name, all_configs.get("dev", {}))
        self._config["env_name"] = env_name
    
    @property
    def api_base_url(self) -> str:
        return self._config.get("api", {}).get("base_url", "")
    
    @property
    def api_timeout(self) -> int:
        return self._config.get("api", {}).get("timeout", 30)
    
    @property
    def app_capabilities(self) -> Dict[str, Any]:
        return self._config.get("app", {})
    
    @property
    def test_account(self) -> Dict[str, str]:
        return self._config.get("test_account", {})
    
    @property
    def database(self) -> Dict[str, str]:
        return self._config.get("database", {})
    
    @property
    def current_env(self) -> str:
        return self._config.get("env_name", "dev")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项，支持点号分隔的嵌套访问"""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def reload(self):
        """重新加载配置（用于运行时切换环境）"""
        self._config.clear()
        self._load_config()


# 全局单例实例
settings = Settings()
