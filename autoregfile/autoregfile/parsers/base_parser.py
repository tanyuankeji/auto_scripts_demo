#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置解析器基类

定义配置解析的通用接口。
"""

from typing import Dict, Any, List, Optional, Type
import os
import importlib

from ..core.address_planner import get_address_planner


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
            "auto_address": False,  # 是否自动分配地址
        }
        
        for key, value in defaults.items():
            if key not in config:
                config[key] = value
        
        # 获取地址规划器
        address_planner = get_address_planner()
        
        # 验证寄存器列表
        if "registers" not in config or not config["registers"]:
            config["registers"] = []
        
        # 创建寄存器名称到索引的映射，用于后续锁定关系处理
        reg_name_to_index = {}
        for i, reg in enumerate(config["registers"]):
            # 检查必需字段
            if "name" not in reg:
                raise ValueError(f"寄存器 #{i+1} 缺少名称")
            
            # 注意：如果自动分配地址，这里不检查地址字段
            if not config["auto_address"] and "address" not in reg:
                raise ValueError(f"寄存器 '{reg['name']}' 缺少地址，且未启用自动地址分配")
            
            # 设置默认值
            if "width" not in reg:
                reg["width"] = config["data_width"]
                
            if "type" not in reg:
                reg["type"] = config["default_reg_type"]
                
            if "reset_value" not in reg:
                reg["reset_value"] = config["reset_value"]
                
            if "description" not in reg:
                reg["description"] = f"寄存器 {reg['name']}"
            
            # 添加锁定关系字段
            if "locked_by" not in reg:
                reg["locked_by"] = []
                
            # 记录寄存器名称到索引的映射
            reg_name_to_index[reg["name"]] = i
        
        # 处理字段定义
        if "fields" not in config or not config["fields"]:
            config["fields"] = []
        
        # 处理锁定关系
        if "lock_relations" in config and config["lock_relations"]:
            for lock_rel in config["lock_relations"]:
                if "locker" not in lock_rel or "locked" not in lock_rel:
                    continue
                    
                locker_name = lock_rel["locker"]
                locked_name = lock_rel["locked"]
                
                # 验证锁定关系中的寄存器是否存在
                if locker_name not in reg_name_to_index:
                    raise ValueError(f"锁定关系中的锁定寄存器 '{locker_name}' 不存在")
                    
                if locked_name not in reg_name_to_index:
                    raise ValueError(f"锁定关系中的被锁定寄存器 '{locked_name}' 不存在")
                
                # 添加锁定关系
                locked_idx = reg_name_to_index[locked_name]
                config["registers"][locked_idx]["locked_by"].append(locker_name)
        
        # 自动分配地址（如果启用）
        if config["auto_address"]:
            config = address_planner.auto_assign_addresses(config, config["module_name"])
        
        # 验证地址规划
        errors = address_planner.validate_addresses(config)
        if errors:
            for error in errors:
                print(f"警告: {error}")
        
        # 添加内存映射
        config["memory_map"] = address_planner.get_memory_map_markdown()
        
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