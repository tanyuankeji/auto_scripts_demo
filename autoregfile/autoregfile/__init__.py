#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
寄存器文件生成器包

用于自动生成硬件寄存器文件的工具集。
"""

__version__ = "1.0.0"
__author__ = "IC自动化工具组"
__description__ = "硬件寄存器文件自动生成工具"

# 导入主要接口
from .register_factory import RegisterFactory, get_register_factory
from .core.data_model import RegType

# 向后兼容函数
def generate_regfile(config_file, output_file, bus_protocol=None, template_dirs=None, debug=False):
    """
    生成寄存器文件（向后兼容函数）
    
    Args:
        config_file: 配置文件路径
        output_file: 输出文件路径
        bus_protocol: 总线协议
        template_dirs: 模板目录列表
        debug: 是否启用调试模式
        
    Returns:
        bool: 是否成功生成
    """
    factory = get_register_factory(debug)
    
    if template_dirs:
        if isinstance(template_dirs, str):
            factory.add_template_dir(template_dirs)
        else:
            for template_dir in template_dirs:
                factory.add_template_dir(template_dir)
    
    return factory.generate_regfile(config_file, output_file, bus_protocol)

def list_protocols():
    """
    列出支持的总线协议（向后兼容函数）
    
    Returns:
        List[str]: 支持的总线协议列表
    """
    factory = get_register_factory()
    return factory.list_supported_protocols()

def list_templates(category=None):
    """
    列出可用的模板（向后兼容函数）
    
    Args:
        category: 模板类别
        
    Returns:
        List[str]: 模板列表
    """
    from .core.template_manager import get_template_manager
    template_manager = get_template_manager()
    return template_manager.list_templates(category)

__all__ = [
    # 版本相关
    '__version__', '__author__', '__description__',
    
    # 主要接口
    'RegisterFactory', 'RegType', 'get_register_factory',
    
    # 向后兼容函数
    'generate_regfile', 'list_protocols', 'list_templates'
] 