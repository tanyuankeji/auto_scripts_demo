#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置解析器基类

定义配置解析的通用接口。
"""

from typing import Dict, Any, List, Optional, Type
import os
import importlib


class ConfigParser:
    """配置解析器基类"""
    
    @staticmethod
    def parse(config_source: str) -> Dict[str, Any]:
        """
        解析配置
        
        参数:
            config_source: 配置源（文件路径或配置字符串）
            
        返回:
            解析后的配置字典
        """
        raise NotImplementedError("子类必须实现此方法")
    
    @classmethod
    def validate_config(cls, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证并标准化配置
        
        参数:
            config: 解析后的配置字典
            
        返回:
            验证和标准化后的配置字典
        """
        # 基本字段验证
        required_fields = ["module_name"]
        for field in required_fields:
            if field not in config:
                raise ValueError(f"缺少必需字段: {field}")
        
        # 设置默认值
        defaults = {
            "data_width": 32,
            "addr_width": 8,
            "num_write_ports": 1,
            "num_read_ports": 1,
            "sync_reset": False,
            "reset_value": "0",
            "byte_enable": True,
            "default_reg_type": "ReadWrite",
            "implementation": "instance",
        }
        
        for key, value in defaults.items():
            if key not in config:
                config[key] = value
        
        # 验证寄存器列表
        if "registers" not in config or not config["registers"]:
            config["registers"] = []
        
        for i, reg in enumerate(config["registers"]):
            # 检查必需字段
            if "name" not in reg:
                raise ValueError(f"寄存器 #{i+1} 缺少名称")
            
            if "address" not in reg:
                raise ValueError(f"寄存器 '{reg['name']}' 缺少地址")
            
            # 设置默认值
            if "width" not in reg:
                reg["width"] = config["data_width"]
                
            if "type" not in reg:
                reg["type"] = config["default_reg_type"]
                
            if "reset_value" not in reg:
                reg["reset_value"] = config["reset_value"]
                
            if "description" not in reg:
                reg["description"] = f"寄存器 {reg['name']}"
        
        return config


def detect_parser(config_source: str) -> ConfigParser:
    """
    根据配置源自动检测适合的解析器
    
    参数:
        config_source: 配置源
        
    返回:
        合适的解析器实例
    """
    # 动态导入解析器类
    from .json_parser import JsonParser
    from .yaml_parser import YamlParser
    from .excel_parser import ExcelParser
    
    if os.path.isfile(config_source):
        _, ext = os.path.splitext(config_source)
        ext = ext.lower()
        
        if ext in ['.json']:
            return JsonParser()
        elif ext in ['.yaml', '.yml']:
            return YamlParser()
        elif ext in ['.xlsx', '.xls']:
            return ExcelParser()
    
    # 对于字符串配置，尝试判断是否为JSON或YAML
    try:
        import json
        json.loads(config_source)
        return JsonParser()
    except:
        try:
            import yaml
            yaml.safe_load(config_source)
            return YamlParser()
        except:
            pass
    
    raise ValueError(f"无法自动检测配置源类型: {config_source}") 