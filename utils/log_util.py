"""
日志管理工具 - 基于 loguru
提供统一的日志格式、文件输出、级别控制
"""
import os
import sys
from loguru import logger
from datetime import datetime


class LogUtil:
    """
    日志工具类
    功能：
    - 控制台彩色输出
    - 文件按日期轮转
    - 不同级别日志分离
    - 自动压缩旧日志
    """
    
    _initialized = False
    
    @classmethod
    def init(cls, log_dir: str = None, level: str = "DEBUG"):
        """
        初始化日志系统
        
        Args:
            log_dir: 日志文件目录，默认 Reports/logs
            log_level: 日志级别 DEBUG/INFO/WARNING/ERROR
        """
        if cls._initialized:
            return
        
        # 移除默认 handler
        logger.remove()
        
        # 日志目录
        if log_dir is None:
            log_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                "Reports", "logs"
            )
        os.makedirs(log_dir, exist_ok=True)
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 1. 控制台输出（带颜色）
        logger.add(
            sys.stdout,
            format="<green>{time:HH:mm:ss.SSS}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                   "<level>{message}</level>",
            level=level,
            colorize=True
        )
        
        # 2. 全量日志文件（DEBUG 级别以上）
        logger.add(
            os.path.join(log_dir, f"{today}_all.log"),
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
            level="DEBUG",
            rotation="00:00",
            retention="7 days",
            compression="gz",
            encoding="utf-8"
        )
        
        # 3. 错误日志文件（ERROR 级别以上）
        logger.add(
            os.path.join(log_dir, f"{today}_error.log"),
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
            level="ERROR",
            rotation="00:00",
            retention="30 days",
            compression="gz",
            encoding="utf-8"
        )
        
        cls._initialized = True
        
        # 测试启动日志
        logger.info("=" * 60)
        logger.info("日志系统初始化完成")
        logger.info(f"日志目录: {log_dir}")
        logger.info(f"日志级别: {level}")
        logger.info("=" * 60)
    
    @classmethod
    def get_logger(cls, name: str = None) -> logger:
        """获取 Logger 实例"""
        if not cls._initialized:
            cls.init()
        return logger.bind(name=name) if name else logger


# 导出便捷函数
def get_logger(name: str = None) -> LogUtil.get_logger(name):
    """获取 Logger 的快捷方式"""
    return LogUtil.get_logger(name)


# 初始化日志系统
LogUtil.init()
log = LogUtil.get_logger(__name__)
