#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
寄存器工厂模块

提供生成寄存器文件的主要接口，是系统的核心类。
"""

import os
import time
import logging
from typing import Dict, Any, List, Optional, Union, Tuple

from .utils import get_logger, configure_global_logging
from .parsers import ParserFactory, ParserBase
from .core.bus_generators.factory import BusGeneratorFactory


class RegisterFactory:
    """
    寄存器工厂类
    
    提供简单的接口来生成寄存器文件，支持多种配置格式和总线协议。
    """
    
    def __init__(self, debug: bool = False, log_file: Optional[str] = None):
        """
        初始化寄存器工厂
        
        Args:
            debug: 是否启用调试模式
            log_file: 日志文件路径，None表示不记录到文件
        """
        # 配置日志
        log_level = logging.DEBUG if debug else logging.INFO
        configure_global_logging(
            level=log_level,
            log_file=log_file,
            file_handler_enabled=log_file is not None
        )
        
        self.logger = get_logger("RegisterFactory")
        self.debug = debug
        self.template_dirs = []
        
        # 添加默认模板目录
        module_dir = os.path.dirname(__file__)
        default_template_dir = os.path.join(module_dir, 'templates')
        self.add_template_dir(default_template_dir)
        
        self.logger.info("寄存器工厂初始化完成")
    
    def add_template_dir(self, template_dir: str) -> None:
        """
        添加模板目录
        
        Args:
            template_dir: 模板目录路径
        """
        if os.path.isdir(template_dir):
            if template_dir not in self.template_dirs:
                self.template_dirs.append(template_dir)
                self.logger.debug(f"添加模板目录: {template_dir}")
        else:
            self.logger.warning(f"模板目录不存在: {template_dir}")
    
    def generate_regfile(self, config_file: str, output_file: str, 
                       bus_protocol: Optional[str] = None, 
                       enable_debug_info: bool = False) -> bool:
        """
        生成寄存器文件
        
        Args:
            config_file: 配置文件路径
            output_file: 输出文件路径
            bus_protocol: 总线协议，None表示使用配置文件中指定的协议
            enable_debug_info: 是否在生成的寄存器文件中包含调试信息
            
        Returns:
            bool: 是否成功生成
        """
        self.logger.info(f"开始生成寄存器文件，配置文件: {config_file}，输出文件: {output_file}")
        start_time = time.time()
        
        try:
            # 解析配置文件
            config = self._parse_config_file(config_file)
            if not config:
                self.logger.error("解析配置文件失败")
                return False
            
            # 如果指定了总线协议，覆盖配置中的协议
            if bus_protocol:
                config["bus_protocol"] = bus_protocol
            
            # 设置调试信息选项
            config["enable_debug_info"] = enable_debug_info
            
            # 获取总线协议
            protocol = config.get("bus_protocol", "custom")
            self.logger.info(f"使用总线协议: {protocol}")
            
            # 创建总线生成器
            try:
                generator = BusGeneratorFactory.create_generator(
                    protocol, config, self.template_dirs
                )
            except ValueError as e:
                self.logger.error(f"创建总线生成器失败: {str(e)}")
                return False
            
            # 生成寄存器文件
            success = generator.generate(output_file, enable_debug_info=enable_debug_info)
            
            if success:
                elapsed_time = time.time() - start_time
                self.logger.info(f"寄存器文件生成成功，耗时 {elapsed_time:.2f} 秒")
                return True
            else:
                self.logger.error("寄存器文件生成失败")
                return False
            
        except Exception as e:
            self.logger.error(f"生成寄存器文件时出错: {str(e)}", exc_info=True)
            return False
    
    def _parse_config_file(self, config_file: str) -> Dict[str, Any]:
        """
        解析配置文件
        
        Args:
            config_file: 配置文件路径
            
        Returns:
            Dict[str, Any]: 解析后的配置字典，如果解析失败则返回空字典
        """
        self.logger.info(f"解析配置文件: {config_file}")
        
        # 检查文件是否存在
        if not os.path.exists(config_file):
            self.logger.error(f"配置文件不存在: {config_file}")
            return {}
        
        # 根据文件扩展名确定解析器类型
        parser_type = self._get_parser_type_for_file(config_file)
        
        # 获取解析器
        parser = ParserFactory.get_parser(parser_type)
        if not parser:
            self.logger.error(f"不支持的配置文件格式: {config_file}")
            return {}
        
        # 解析配置文件
        config = parser.parse(config_file)
        
        self.logger.info(f"配置文件解析完成，包含 {len(config.get('registers', []))} 个寄存器")
        return config
    
    def _get_parser_type_for_file(self, config_file: str) -> str:
        """
        根据文件扩展名确定适用的解析器类型
        
        Args:
            config_file: 配置文件路径
            
        Returns:
            str: 适用的解析器类型名称
        """
        _, ext = os.path.splitext(config_file)
        ext = ext.lower()
        
        if ext == '.xls' or ext == '.xlsx':
            return "excel"
        elif ext == '.json':
            return "json"
        elif ext == '.yaml' or ext == '.yml':
            return "yaml"
        elif ext == '.csv':
            return "csv"
        else:
            return "unknown"
    
    def list_supported_protocols(self) -> List[str]:
        """
        列出支持的总线协议
        
        Returns:
            List[str]: 支持的总线协议列表
        """
        return BusGeneratorFactory.list_supported_protocols()
    
    def list_supported_config_formats(self) -> List[str]:
        """
        列出支持的配置文件格式
        
        Returns:
            List[str]: 支持的配置文件格式列表
        """
        return ParserFactory.list_supported_types()


# 创建全局寄存器工厂实例
_global_register_factory = None

def get_register_factory(debug: bool = False, log_file: Optional[str] = None) -> RegisterFactory:
    """
    获取全局寄存器工厂实例
    
    Args:
        debug: 是否启用调试模式
        log_file: 日志文件路径
        
    Returns:
        RegisterFactory: 寄存器工厂实例
    """
    global _global_register_factory
    if _global_register_factory is None:
        _global_register_factory = RegisterFactory(debug, log_file)
    return _global_register_factory 