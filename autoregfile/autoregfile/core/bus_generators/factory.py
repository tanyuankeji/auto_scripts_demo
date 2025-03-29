#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
总线生成器工厂模块

此模块提供了总线生成器工厂类，用于创建和管理不同类型的总线生成器。
"""

import os
import sys
import importlib
import pkgutil
from typing import Dict, Any, List, Optional, Type, Callable, Union, Set
from pathlib import Path

from ...utils import get_logger
from .base_generator import BaseBusGenerator


class BusGeneratorFactory:
    """
    总线生成器工厂类
    
    用于注册、创建和管理不同类型的总线生成器。
    支持通过装饰器注册新的总线协议生成器。
    """
    
    # 保存注册的生成器类
    _generators: Dict[str, Type[BaseBusGenerator]] = {}
    
    # 追踪是否已加载内置生成器
    _loaded_builtin_generators = False
    
    @classmethod
    def register_protocol(cls, protocol_name: str) -> Callable:
        """
        注册总线协议生成器的装饰器
        
        Args:
            protocol_name: 总线协议名称
            
        Returns:
            装饰器函数
        """
        def decorator(generator_class: Type[BaseBusGenerator]) -> Type[BaseBusGenerator]:
            # 确保生成器类是BaseBusGenerator的子类
            if not issubclass(generator_class, BaseBusGenerator):
                raise TypeError(f"总线生成器类 {generator_class.__name__} 必须继承自 BaseBusGenerator")
            
            # 标准化协议名称为小写
            protocol = protocol_name.lower()
            
            # 注册生成器类
            if protocol in cls._generators:
                logger = get_logger("BusGeneratorFactory")
                logger.warning(f"总线协议 '{protocol}' 已被注册，将被覆盖")
            
            cls._generators[protocol] = generator_class
            return generator_class
            
        return decorator
    
    @classmethod
    def _load_builtin_generators(cls) -> None:
        """加载内置的总线生成器"""
        if cls._loaded_builtin_generators:
            return
            
        logger = get_logger("BusGeneratorFactory")
        
        # 获取当前目录
        current_dir = os.path.dirname(__file__)
        
        # 导入当前包中所有模块
        for _, name, is_pkg in pkgutil.iter_modules([current_dir]):
            if not is_pkg and name != "factory" and name != "base_generator":
                try:
                    importlib.import_module(f"..core.bus_generators.{name}", package="autoregfile.core.bus_generators")
                    logger.debug(f"加载内置总线生成器模块: {name}")
                except ImportError as e:
                    logger.error(f"导入内置总线生成器模块 {name} 失败: {str(e)}")
        
        cls._loaded_builtin_generators = True
    
    @classmethod
    def _load_external_generators(cls, external_dirs: Optional[List[str]] = None) -> None:
        """
        加载外部总线生成器
        
        Args:
            external_dirs: 外部总线生成器目录列表
        """
        if not external_dirs:
            return
            
        logger = get_logger("BusGeneratorFactory")
        
        # 保存当前sys.path
        old_path = sys.path.copy()
        
        try:
            for ext_dir in external_dirs:
                if not os.path.isdir(ext_dir):
                    logger.warning(f"外部总线生成器目录不存在: {ext_dir}")
                    continue
                    
                # 添加目录到sys.path
                if ext_dir not in sys.path:
                    sys.path.insert(0, ext_dir)
                
                # 尝试导入所有.py文件
                for file in os.listdir(ext_dir):
                    if file.endswith(".py") and not file.startswith("_"):
                        module_name = file[:-3]  # 移除.py扩展名
                        try:
                            importlib.import_module(module_name)
                            logger.debug(f"加载外部总线生成器模块: {module_name}")
                        except ImportError as e:
                            logger.error(f"导入外部总线生成器模块 {module_name} 失败: {str(e)}")
        
        finally:
            # 恢复原始sys.path
            sys.path = old_path
    
    @classmethod
    def create_generator(cls, bus_protocol: str, config: Dict[str, Any], 
                        template_dirs: Optional[List[str]] = None,
                        external_generator_dirs: Optional[List[str]] = None) -> Optional[BaseBusGenerator]:
        """
        创建总线生成器实例
        
        Args:
            bus_protocol: 总线协议名称
            config: 配置字典
            template_dirs: 模板目录列表
            external_generator_dirs: 外部总线生成器目录列表
            
        Returns:
            总线生成器实例，如果未找到则返回None
        """
        logger = get_logger("BusGeneratorFactory")
        
        # 加载内置生成器
        cls._load_builtin_generators()
        
        # 加载外部生成器
        cls._load_external_generators(external_generator_dirs)
        
        # 标准化协议名称为小写
        protocol = bus_protocol.lower()
        
        # 查找生成器类
        generator_class = cls._generators.get(protocol)
        
        if generator_class:
            # 使用注册的生成器类
            logger.info(f"使用已注册的总线生成器: {generator_class.__name__} 用于协议 '{protocol}'")
            return generator_class(config, template_dirs)
        
        # 如果没有注册的生成器，检查配置中是否有自定义模板
        custom_template = None
        bus_options = config.get("bus_options", {})
        
        if protocol in bus_options and "template" in bus_options[protocol]:
            custom_template = bus_options[protocol]["template"]
        
        if custom_template:
            # 动态导入CustomBusGenerator，避免循环导入
            try:
                from .custom_generator import CustomBusGenerator
                # 使用自定义总线生成器
                logger.info(f"找不到已注册的总线生成器，使用自定义生成器用于协议 '{protocol}'")
                return CustomBusGenerator(config, template_dirs)
            except ImportError as e:
                logger.error(f"导入自定义总线生成器失败: {str(e)}")
                return None
        
        # 未找到合适的生成器
        logger.error(f"未找到总线协议 '{protocol}' 的生成器")
        return None
    
    @classmethod
    def list_supported_protocols(cls) -> List[str]:
        """
        列出所有支持的总线协议
        
        Returns:
            支持的总线协议列表
        """
        # 加载内置生成器
        cls._load_builtin_generators()
        
        # 返回排序后的协议列表
        return sorted(list(cls._generators.keys()))


# 注册装饰器
def register_bus_generator(protocol_name: str):
    """
    总线生成器注册装饰器
    
    使用此装饰器可以简化总线生成器的注册过程。
    
    Example:
        @register_bus_generator("apb")
        class APBBusGenerator(BaseBusGenerator):
            pass
    
    Args:
        protocol_name: 总线协议名称
        
    Returns:
        装饰器函数
    """
    return BusGeneratorFactory.register_protocol(protocol_name) 