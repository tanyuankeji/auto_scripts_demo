#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
解析器基类模块

定义配置文件解析的基本接口和通用功能，为不同格式的配置解析提供统一框架。
"""

import os
import abc
from typing import Dict, List, Any, Optional, Union, Set

from ..utils import get_logger


class ParserBase(metaclass=abc.ABCMeta):
    """
    解析器基类
    
    为不同格式的配置文件解析器提供统一的接口和基本功能
    """
    
    def __init__(self):
        """初始化解析器基类"""
        self.logger = get_logger(self.__class__.__name__)
        self.config = {
            "module_name": "default_regfile",
            "bus_protocol": "custom",
            "addr_width": 8,
            "data_width": 32,
            "registers": []
        }
        self._valid_reg_types = self._get_valid_reg_types()
        self._required_fields = {"name", "address"}
    
    def _get_valid_reg_types(self) -> Set[str]:
        """
        获取有效的寄存器类型列表
        
        Returns:
            Set[str]: 有效的寄存器类型集合
        """
        # 这里需要导入reg_type模块，但为了避免循环引用，放在方法内导入
        try:
            from ..core.regtype import get_reg_type_manager
            reg_types = set(get_reg_type_manager().list_all_types())
            
            # 添加别名映射
            for reg_type in list(reg_types):
                type_info = get_reg_type_manager().get_type_info(reg_type)
                if type_info and type_info.aliases:
                    reg_types.update(type_info.aliases)
            
            self.logger.debug(f"已加载 {len(reg_types)} 个有效的寄存器类型")
            return reg_types
            
        except ImportError:
            self.logger.warning("无法导入reg_type模块，将使用默认寄存器类型")
            # 默认支持的寄存器类型
            return {
                "RW", "RO", "WO", "RC", "RS", "W1S", "W1C", "WP", "W1P", "WO1",
                "ReadWrite", "ReadOnly", "WriteOnly", "ReadClean", "ReadSet",
                "Write1Set", "Write1Clear", "WritePulse", "Write1Pulse", "WriteOnce",
                "WRITEONLY_REG", "WRITE1SET_REG", "READ_WRITE", "READ_ONLY", "WRITE_ONLY"
            }
    
    @abc.abstractmethod
    def parse(self, config_file: str) -> Dict[str, Any]:
        """
        解析配置文件
        
        Args:
            config_file: 配置文件路径
            
        Returns:
            Dict[str, Any]: 解析后的配置字典
        """
        raise NotImplementedError("子类必须实现parse方法")
    
    def validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证配置是否有效
        
        Args:
            config: 待验证的配置字典
            
        Returns:
            Dict[str, Any]: 验证并修复后的配置字典
        """
        # 深拷贝配置，避免修改原始数据
        validated_config = config.copy()
        
        # 验证并修复全局配置
        self._validate_global_config(validated_config)
        
        # 验证并修复寄存器配置
        if "registers" in validated_config:
            validated_registers = []
            for reg in validated_config["registers"]:
                validated_reg = self._validate_register(reg)
                if validated_reg:
                    validated_registers.append(validated_reg)
            
            validated_config["registers"] = validated_registers
        else:
            self.logger.warning("配置中未找到寄存器列表")
            validated_config["registers"] = []
        
        return validated_config
    
    def _validate_global_config(self, config: Dict[str, Any]) -> None:
        """
        验证并修复全局配置
        
        Args:
            config: 配置字典
        """
        # 检查并设置默认模块名
        if "module_name" not in config or not config["module_name"]:
            self.logger.warning("未指定模块名，使用默认名称'default_regfile'")
            config["module_name"] = "default_regfile"
        
        # 检查并设置默认总线协议
        if "bus_protocol" not in config or not config["bus_protocol"]:
            self.logger.warning("未指定总线协议，使用默认协议'custom'")
            config["bus_protocol"] = "custom"
        
        # 检查并设置地址宽度
        if "addr_width" not in config:
            self.logger.warning("未指定地址宽度，使用默认值8")
            config["addr_width"] = 8
        else:
            try:
                config["addr_width"] = int(config["addr_width"])
            except (ValueError, TypeError):
                self.logger.warning(f"地址宽度值无效: {config['addr_width']}，使用默认值8")
                config["addr_width"] = 8
        
        # 检查并设置数据宽度
        if "data_width" not in config:
            self.logger.warning("未指定数据宽度，使用默认值32")
            config["data_width"] = 32
        else:
            try:
                config["data_width"] = int(config["data_width"])
            except (ValueError, TypeError):
                self.logger.warning(f"数据宽度值无效: {config['data_width']}，使用默认值32")
                config["data_width"] = 32
    
    def _validate_register(self, reg: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        验证并修复单个寄存器配置
        
        Args:
            reg: 寄存器配置字典
            
        Returns:
            Optional[Dict[str, Any]]: 验证并修复后的寄存器配置，如果无效则返回None
        """
        # 检查必要字段
        for field in self._required_fields:
            if field not in reg or not reg[field]:
                self.logger.error(f"寄存器缺少必要字段: {field}")
                return None
        
        # 验证并修复寄存器类型
        if "type" in reg:
            if reg["type"] not in self._valid_reg_types:
                self.logger.warning(f"寄存器 {reg['name']} 的类型 {reg['type']} 无效，使用默认类型 'RW'")
                reg["type"] = "RW"
        else:
            self.logger.debug(f"寄存器 {reg['name']} 未指定类型，使用默认类型 'RW'")
            reg["type"] = "RW"
        
        # 处理寄存器地址
        try:
            if isinstance(reg["address"], str):
                # 处理十六进制地址
                if reg["address"].startswith("0x") or reg["address"].startswith("0X"):
                    reg["address"] = int(reg["address"], 16)
                # 处理二进制地址
                elif reg["address"].startswith("0b") or reg["address"].startswith("0B"):
                    reg["address"] = int(reg["address"], 2)
                # 处理十进制地址
                else:
                    reg["address"] = int(reg["address"])
            else:
                reg["address"] = int(reg["address"])
        except (ValueError, TypeError):
            self.logger.error(f"寄存器 {reg['name']} 的地址格式无效: {reg['address']}")
            return None
        
        # 验证并修复字段配置（如果有）
        if "fields" in reg and reg["fields"]:
            validated_fields = []
            for field in reg["fields"]:
                validated_field = self._validate_field(field, reg["name"])
                if validated_field:
                    validated_fields.append(validated_field)
            
            reg["fields"] = validated_fields
        
        return reg
    
    def _validate_field(self, field: Dict[str, Any], reg_name: str) -> Optional[Dict[str, Any]]:
        """
        验证并修复寄存器字段配置
        
        Args:
            field: 字段配置字典
            reg_name: 所属寄存器名称
            
        Returns:
            Optional[Dict[str, Any]]: 验证并修复后的字段配置，如果无效则返回None
        """
        # 检查字段名称
        if "name" not in field or not field["name"]:
            self.logger.error(f"寄存器 {reg_name} 的字段缺少名称")
            return None
        
        # 检查并验证位范围
        if "bit_range" not in field:
            self.logger.error(f"寄存器 {reg_name} 的字段 {field['name']} 缺少bit_range")
            return None
        
        # 处理字段类型（如果有）
        if "type" in field and field["type"] not in self._valid_reg_types:
            self.logger.warning(f"寄存器 {reg_name} 的字段 {field['name']} 的类型 {field['type']} 无效，将使用寄存器类型")
            field.pop("type")
        
        return field
    
    @staticmethod
    def get_parser_for_file(config_file: str) -> str:
        """
        根据文件扩展名确定适用的解析器
        
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


class ParserFactory:
    """
    解析器工厂类
    
    管理和创建不同类型的配置文件解析器
    """
    
    _parsers = {}
    
    @classmethod
    def register_parser(cls, parser_type: str, parser_class) -> None:
        """
        注册解析器类
        
        Args:
            parser_type: 解析器类型名称
            parser_class: 解析器类
        """
        cls._parsers[parser_type] = parser_class
    
    @classmethod
    def get_parser(cls, parser_type: str) -> Optional[ParserBase]:
        """
        获取指定类型的解析器实例
        
        Args:
            parser_type: 解析器类型名称
            
        Returns:
            Optional[ParserBase]: 解析器实例，如果类型不存在则返回None
        """
        parser_class = cls._parsers.get(parser_type)
        if parser_class:
            return parser_class()
        return None
    
    @classmethod
    def parse_file(cls, config_file: str) -> Optional[Dict[str, Any]]:
        """
        根据文件类型解析配置文件
        
        Args:
            config_file: 配置文件路径
            
        Returns:
            Optional[Dict[str, Any]]: 解析后的配置字典，如果解析失败则返回None
        """
        parser_type = ParserBase.get_parser_for_file(config_file)
        if parser_type == "unknown":
            return None
        
        parser = cls.get_parser(parser_type)
        if parser:
            return parser.parse(config_file)
        return None
    
    @classmethod
    def list_supported_types(cls) -> List[str]:
        """
        列出所有支持的解析器类型
        
        Returns:
            List[str]: 支持的解析器类型列表
        """
        return list(cls._parsers.keys()) 