#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志工具模块

提供统一的日志记录功能，支持不同级别的日志输出，
格式化和多种输出方式（控制台、文件）。
"""

import os
import sys
import logging
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler


# 默认日志级别
DEFAULT_LOG_LEVEL = logging.INFO

# 默认日志格式
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 默认日志文件路径
DEFAULT_LOG_PATH = os.path.join(os.getcwd(), 'logs', 'autoregfile.log')


def get_logger(name: str, 
               level: Optional[int] = None, 
               log_format: Optional[str] = None,
               log_file: Optional[str] = None,
               file_handler_enabled: bool = False,
               console_handler_enabled: bool = True,
               max_bytes: int = 10485760,  # 10MB
               backup_count: int = 5) -> logging.Logger:
    """
    获取一个配置好的日志记录器

    Args:
        name: 日志记录器名称
        level: 日志级别，默认为INFO
        log_format: 日志格式字符串
        log_file: 日志文件路径
        file_handler_enabled: 是否启用文件日志处理器
        console_handler_enabled: 是否启用控制台日志处理器
        max_bytes: 单个日志文件最大字节数
        backup_count: 备份日志文件数量

    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 获取日志记录器
    logger = logging.getLogger(name)
    
    # 设置日志级别
    if level is None:
        level = _get_log_level_from_env()
    logger.setLevel(level)
    
    # 如果记录器已经配置了处理器，直接返回
    if logger.handlers:
        return logger
    
    # 配置日志格式
    if log_format is None:
        log_format = DEFAULT_LOG_FORMAT
    formatter = logging.Formatter(log_format)
    
    # 添加控制台处理器
    if console_handler_enabled:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # 添加文件处理器
    if file_handler_enabled:
        if log_file is None:
            log_file = DEFAULT_LOG_PATH
        
        # 确保日志目录存在
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # 创建轮转文件处理器
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def _get_log_level_from_env() -> int:
    """
    从环境变量获取日志级别

    Returns:
        int: 日志级别常量
    """
    level_map = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    
    # 从环境变量获取日志级别
    env_level = os.environ.get('AUTOREGFILE_LOG_LEVEL', '').lower()
    
    # 返回对应的日志级别，如果未设置或无效则返回默认级别
    return level_map.get(env_level, DEFAULT_LOG_LEVEL)


class LogConfig:
    """
    日志配置类
    
    用于集中管理日志配置，实现跨模块的一致性日志配置。
    """
    
    def __init__(self):
        """初始化日志配置"""
        self.level = _get_log_level_from_env()
        self.format = DEFAULT_LOG_FORMAT
        self.file_path = DEFAULT_LOG_PATH
        self.file_handler_enabled = False
        self.console_handler_enabled = True
        self.max_bytes = 10485760  # 10MB
        self.backup_count = 5
    
    def configure_logger(self, name: str) -> logging.Logger:
        """
        使用当前配置创建一个日志记录器
        
        Args:
            name: 日志记录器名称
            
        Returns:
            logging.Logger: 配置好的日志记录器
        """
        return get_logger(
            name=name,
            level=self.level,
            log_format=self.format,
            log_file=self.file_path,
            file_handler_enabled=self.file_handler_enabled,
            console_handler_enabled=self.console_handler_enabled,
            max_bytes=self.max_bytes,
            backup_count=self.backup_count
        )
    
    def set_level(self, level: int) -> None:
        """设置日志级别"""
        self.level = level
    
    def set_format(self, format_str: str) -> None:
        """设置日志格式"""
        self.format = format_str
    
    def enable_file_handler(self, enabled: bool = True) -> None:
        """启用或禁用文件处理器"""
        self.file_handler_enabled = enabled
    
    def enable_console_handler(self, enabled: bool = True) -> None:
        """启用或禁用控制台处理器"""
        self.console_handler_enabled = enabled
    
    def set_file_path(self, path: str) -> None:
        """设置日志文件路径"""
        self.file_path = path


# 创建一个全局日志配置实例
global_log_config = LogConfig()


def configure_global_logging(
    level: Optional[int] = None,
    log_format: Optional[str] = None,
    log_file: Optional[str] = None,
    file_handler_enabled: Optional[bool] = None,
    console_handler_enabled: Optional[bool] = None
) -> None:
    """
    配置全局日志设置
    
    Args:
        level: 日志级别
        log_format: 日志格式字符串
        log_file: 日志文件路径
        file_handler_enabled: 是否启用文件日志处理器
        console_handler_enabled: 是否启用控制台日志处理器
    """
    if level is not None:
        global_log_config.set_level(level)
    
    if log_format is not None:
        global_log_config.set_format(log_format)
    
    if log_file is not None:
        global_log_config.set_file_path(log_file)
    
    if file_handler_enabled is not None:
        global_log_config.enable_file_handler(file_handler_enabled)
    
    if console_handler_enabled is not None:
        global_log_config.enable_console_handler(console_handler_enabled)


def get_configured_logger(name: str) -> logging.Logger:
    """
    获取使用全局配置的日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    return global_log_config.configure_logger(name)


if __name__ == "__main__":
    # 简单的测试代码
    logger = get_configured_logger("autoregfile")
    logger.debug("这是一条调试消息")
    logger.info("这是一条信息消息")
    logger.warning("这是一条警告消息")
    logger.error("这是一条错误消息")
    logger.critical("这是一条严重错误消息")
    
    try:
        1 / 0
    except Exception as e:
        logger.exception("捕获到一个异常") 